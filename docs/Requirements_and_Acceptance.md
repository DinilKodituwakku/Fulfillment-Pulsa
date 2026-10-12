# Fulfilment Pulse - Requirements and acceptance

Planning revision: 12 October 2026. Based on the restored [project specification](../Fulfilment_Pulse_Assignment_Specs.md). This checklist describes the proposed solution, not verified completion or an assessment rubric. Add run records, queries or screenshots before marking requirements complete.

## 1. Intended outcome

Users can inspect fictional Melbourne order activity by day, hour and zone alongside daily public weather. The workflow is repeatable and traceable: Databricks processing, ADLS Gen2 Bronze/Silver, Fabric OneLake Gold and Power BI reporting.

The first release includes one historical report page and an ordered batch workflow. Real retail systems, private customer data, streaming, traffic, live alerts and machine learning are outside this release.

## 2. Functional requirements

| ID | Requirement | Acceptance evidence |
| --- | --- | --- |
| FR-01 | Register every weather source, station, unit, date coverage, download date and usage terms. | Source register matches the actual inputs used in Databricks. |
| FR-02 | Save a synthetic order generator with fixed seed, parameters and date range. | Repeated runs with identical settings produce identical business records. |
| FR-03 | Define explicit delivery-zone mapping. | Each accepted zone maps to one zone record; measure-specific station assumptions are recorded. |
| FR-04 | Preserve raw inputs and create Bronze Delta tables with explicit schemas. | Input row counts, source and ingestion batch are traceable. |
| FR-05 | Parse and validate Silver records. | Valid records satisfy DQ-01 through DQ-06; rejected records retain original values and reasons. |
| FR-06 | Build daily, date/hour and date/zone order aggregates. | Each summary independently reconciles to accepted Silver orders and item sums. |
| FR-07 | Build daily weather and shared date/zone dimensions. | Documented keys are unique; stations, units and missing flags remain available. |
| FR-08 | Publish validated Gold Delta tables to Fabric OneLake. | All destination tables are readable in Fabric and associated with a completed publication batch. |
| FR-09 | Build an explicit Power BI semantic model over Fabric Gold. | Connection mode, relationships and measures are saved and documented. |
| FR-10 | Deliver the report specified in section 5. | Export or screenshots plus independently checked totals and filters. |
| FR-11 | Run ingestion, validation, aggregation and publication in dependency order. | Successful job evidence and a failed-stage recovery example. |
| FR-12 | Update the semantic model only from a complete, reconciled publication. | Displayed publication time identifies a successful batch; partial-batch exposure is controlled and tested. |

## 3. Quality and operational requirements

| ID | Requirement | Acceptance evidence |
| --- | --- | --- |
| DQ-01 | Accepted order IDs must be nonblank and unique. | Duplicate and missing-ID counts plus explicit rejection/deduplication rules. |
| DQ-02 | Parse order timestamps and derive Australia/Melbourne reporting dates/hours. | Invalid and out-of-period values are rejected; timezone and daylight-saving assumptions documented. |
| DQ-03 | Item counts must be positive integers. | Invalid, zero, negative and fractional values rejected with reasons. |
| DQ-04 | Accepted zones must exist in the mapping. | Unknown zones quarantined; zone keys unique. |
| DQ-05 | Weather keys distinguish date, station and measure. | Accepted keys unique and separate station provenance retained. |
| DQ-06 | Missing weather stays null and flagged. | Blank input remains missing in Silver, Gold and visuals, rather than becoming zero. |
| DQ-07 | Weather/order joins preserve totals and disclose date alignment. | Overlap, unmatched dates and before/after reconciliation recorded; no row multiplication. |
| DQ-08 | Account for every input record. | Accepted, quarantined and deduplicated dispositions explain all input rows. |
| NFR-01 | Rerunning unchanged inputs must not duplicate records or change business totals. | Compare two successful runs; ingestion metadata can differ. |
| NFR-02 | Save code, notebook exports, configuration and setup instructions in Git. | Another person can locate and repeat the sample workflow. |
| NFR-03 | Store credentials outside Git and document required permissions. | Nonsecret references to secret storage and platform roles. |
| NFR-04 | Record run status, timing, row counts, rejection counts and reconciliation. | Run log identifies the successful batch or failed stage. |
| NFR-05 | Prevent overlapping writers and inconsistent report publication. | Single-writer configuration and partial-publication recovery demonstrated. |
| NFR-06 | Verify compute, storage, capacity and report permissions before building. | Small Databricks-to-OneLake write/read succeeds; intended viewer opens the report. |
| NFR-07 | Label simulated data and limit claims. | Report, tables and documentation distinguish synthetic orders from observed weather. |

No production uptime or latency SLA is defined. Record observed batch duration and report usability during the demonstration.

## 4. Data contracts and Gold tables

| Input | Required fields / key | Rules |
| --- | --- | --- |
| Orders | `order_id`, `order_timestamp`, `delivery_zone`, `item_count`, `is_synthetic`; key: order ID | Positive integer items; synthetic flag true; Melbourne local timestamp interpretation. |
| Optional existing attributes | `promised_window`, `fulfilment_stage`, `basket_category`, `simulated_delay_flag` | Simulated attributes; not required dashboard measures. |
| Weather | `observation_date`, `station_id`, `measure`, `value`, `unit`, `is_missing`; key: date + station + measure | Station ID is a string retaining leading zeroes; retain source quality and accumulation-period fields. |
| Mapping | `delivery_zone`, station reference(s), `mapping_assumption`; key: zone | Explain broad geographic coverage and separate stations by measure where needed. |
| Lineage | Source file/URL, ingestion timestamp, batch ID | Trace every input and output. |
| Quarantine | Original record, source, batch and reason | Retain rejected values for investigation. |

Confirm how observation dates and accumulation periods relate to calendar-day orders before comparing weather and demand. Daily observations do not support hourly weather explanations.

| Gold table | Grain | Main outputs |
| --- | --- | --- |
| `gold_orders_daily` | Local date | Order count, total item count, synthetic flag |
| `gold_orders_hourly` | Local date + hour 0-23 | Order count, total item count, synthetic flag |
| `gold_orders_by_zone` | Local date + zone | Order count, total item count, synthetic flag |
| `gold_weather_daily` | Observation date + station + measure | Value, unit, missing flag |
| `gold_dim_date` | Date | Calendar attributes covering the report period |
| `gold_dim_zone` | Zone | Zone label and mapping limitations |

Associate Gold with a publication batch. Each order aggregate represents the same orders independently; do not add totals across the three tables.

## 5. Power BI report

Page title: **Fulfilment Pulse - Historical overview**.

| Element | Source / behaviour |
| --- | --- |
| Date slicer | Shared date dimension filters all order and weather visuals. |
| Total orders | Sum of daily order counts for selected dates. |
| Total items | Sum of daily item totals for selected dates. |
| Orders by day | Chronological daily trend. |
| Orders by hour | Sum selected dates by hour; sort 0-23. |
| Orders by delivery zone | Date-filtered zone comparison. |
| Maximum temperature | Separate weather chart filtered to measure and station, showing degree-C unit and missing gaps. |
| Rainfall | Separate weather chart filtered to measure and station, showing millimetres and missing gaps. |
| Explanation and freshness | Synthetic-data label, analysis period, weather limitations and last successful publication time. |

Use single-direction one-to-many dimension relationships; no fact-to-fact relationships. A zone slicer is not required because the daily/hourly aggregates contain no zone field. Change the fact grain before expecting a zone slicer to filter those visuals.

Proposed measures, using the planned schema:

```dax
Total Orders = SUM(gold_orders_daily[order_count])
Total Items = SUM(gold_orders_daily[item_count])
Hourly Orders = SUM(gold_orders_hourly[order_count])
Zone Orders = SUM(gold_orders_by_zone[order_count])
```

Choose Direct Lake when supported; document Import via the Lakehouse SQL analytics endpoint as the fallback. Verify refresh and automatic-update behaviour for the selected mode, including protection against partial publication. See [Microsoft Direct Lake overview](https://learn.microsoft.com/en-us/fabric/fundamentals/direct-lake-overview).

## 6. Acceptance scenarios

| ID | Scenario | Expected result |
| --- | --- | --- |
| AT-01 | Load the historical 30-order sample, if used. | Dispositions account for all 30; accepted totals match validation results. |
| AT-02 | Supply duplicate ID, bad date, invalid count and unknown zone in a disposable test input. | Each follows documented rejection/deduplication rules without incorrect Gold increases. |
| AT-03 | Supply blank weather. | Null and missing flag survive through the report. |
| AT-04 | Build order aggregates. | Each independently matches accepted Silver counts and item totals. |
| AT-05 | Rerun unchanged inputs. | Business records and totals stay unchanged. |
| AT-06 | Filter report dates. | Cards and charts match independently queried values for selected dates. |
| AT-07 | Fail one publication step. | Batch is failed, not presented as complete; full rerun restores consistency. |
| AT-08 | Inspect station labels and source metadata. | They match actual published weather sources. |
| AT-09 | Open the report as the intended viewer. | Access, labels, filters and publication time work. |

## 7. Deliverables checklist

- [ ] Source register and data dictionary.
- [ ] Reproducible synthetic generator and mapping.
- [ ] Platform feasibility check.
- [ ] Bronze/Silver/quarantine notebook exports.
- [ ] Gold transformation/publication notebook exports.
- [ ] Reconciliation and repeat-run evidence.
- [ ] Job configuration and recovery instructions.
- [ ] Fabric Lakehouse setup and compatible Delta settings.
- [ ] Power BI model/report and connection instructions.
- [ ] Acceptance evidence and final limitations review.

Actual cloud access, weather files/stations, date overlap, model mode and sharing permissions remain verification gates. Existing notebook presence alone does not satisfy these checks.
