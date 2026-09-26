# Fulfilment Pulse — Assignment Specs

## 1. Project objective

Build an Azure Databricks, Microsoft Fabric and Power BI learning project that combines public historical weather data with fictional retail-order data to create a clear operational dashboard and a staged analytics solution. The project should demonstrate how data engineering, reporting, quality checks and simple forecasting can be combined in a practical workflow: Databricks for ingestion and transformation, Fabric for Gold storage and serving, and Power BI for dashboarding.

This is a synthetic prototype designed for portfolio learning and demonstration. It is not an operational retailer system and does not use real customer or employee data.

## 2. Business context

The project explores how fulfilment teams could understand demand, delivery-pressure signals and external conditions using a fictional dataset. The goal is to create a story that is realistic enough to be useful in a learning portfolio, while staying clearly labelled as synthetic.

The project should help answer questions such as:

- How much fictional order activity is happening?
- Which days and hours are busiest?
- Which delivery zones show more activity?
- What weather conditions existed during the same period?
- Which records or zones may have elevated risk or disruption?

## 3. Intended users

- Team leader / manager
- Fulfilment team
- Delivery team
- Analyst
- Data engineer
- Data scientist

These users need a system that explains the data, exposes known assumptions and supports investigation rather than automatic business decisions.

## 4. Scope

### In scope for the first version

- One public historical weather source
- Small fictional order dataset
- Delivery-area mapping table
- Azure Databricks ingestion and transformation notebooks and jobs
- Bronze and Silver Delta storage in Azure Data Lake Storage Gen2 (ADLS Gen2)
- Microsoft Fabric Lakehouse / OneLake storage for Gold tables
- Bronze, Silver and Gold layers
- Python, PySpark and SQL processing
- Basic data-quality checks
- One Power BI report page
- Project documentation in GitHub

### Out of scope for the first version

- Real customer or employee records
- Private employer data or internal systems
- Production deployment
- Real-time streaming as a first-version requirement
- Complex ML deployment
- Website or public-facing app
- Branding or real retailer claims

## 5. Functional requirements

### Core functionality

1. Ingest public historical weather files, fictional orders and area mapping using Azure Databricks.
2. Generate fictional orders using Python with a fixed seed for reproducibility.
3. Store raw inputs and source metadata in Bronze Delta tables managed through Databricks.
4. Clean and validate the data in Silver using Databricks PySpark or SQL.
5. Calculate reporting tables in Databricks and publish them as Gold Delta tables in a Fabric Lakehouse.
6. Create a Power BI semantic model over Fabric Gold tables and build a one-page report that answers the main questions.
7. Record assumptions, data sources and limitations clearly.

### Reporting requirements

The first dashboard should contain at least:

- Total orders
- Orders by day
- Orders by hour
- Orders by delivery zone
- Historical weather chart

The report must include:

- date filters
- a synthetic-data label
- explanation of the analysis period
- clear notes about limitations and assumptions

## 6. Data requirements

### Weather data

- Historical public weather observations
- Must be documented with source, coverage and time resolution
- Must clearly state unit conventions
- Missing values must not be silently treated as zero

### Fictional order data

Minimum fields:

- order_id
- order_timestamp
- delivery_zone
- item_count
- is_synthetic

Recommended additional fields for later phases:

- promised_window
- fulfilment_stage
- basket_category
- simulated_delay_flag

### Area mapping

- Delivery zone name
- Weather station or location reference
- Any relevant mapping assumptions

## 7. Data-quality requirements

The solution must check that:

- Order IDs are present and unique
- Order timestamps are valid and within the intended date range
- Item counts are positive whole numbers
- Delivery zones exist in the mapping table
- Weather values use documented units
- Missing weather is flagged and not silently converted to zero
- Data joins do not multiply rows unexpectedly
- Summary totals reconcile to valid row counts

Invalid rows must be stored in a quarantine table with a reason.

## 8. Bronze, Silver and Gold layer design

### Bronze — ingested by Databricks, stored in ADLS Gen2

Preserve source files and create raw Delta tables:

- bronze_orders
- bronze_weather
- bronze_zone_mapping

Record source file or URL, ingestion timestamp, batch identifier, and weather station and measure metadata. Use explicit schemas. Keep raw values available for tracing validation failures.

### Silver — transformed by Databricks, stored in ADLS Gen2

Validated and cleaned Delta tables:

- silver_orders
- silver_weather
- silver_zone_mapping
- silver_quarantined_records

Use the quality rules in section 7. Quarantine records with their original values, source, batch identifier and rejection reason. Preserve missing weather observations with explicit quality flags. Use Australia/Melbourne for local reporting dates and hours, and document daylight-saving handling.

Weather keys must distinguish observation date, station and measure. Temperature and rainfall from different stations must retain separate provenance. Do not imply that the current broad delivery zones have precise station coverage.

### Gold — calculated by Databricks, stored and served in Fabric

Databricks owns the transformation logic and writes the final Delta tables into the Fabric Lakehouse Tables area in OneLake. Fabric is the reporting source of truth for Gold; a shortcut to externally stored Gold is not the default design.

| Table | Grain and purpose |
| --- | --- |
| gold_orders_daily | One row per local order date; order count and total item count. |
| gold_orders_hourly | One row per local order date and hour (0–23); order count and total item count. Retain date so date filters work. |
| gold_orders_by_zone | One row per local order date and delivery zone; order count and total item count. |
| gold_weather_daily | One row per observation date, station and measure; value, unit and missing-value flag for historical weather charts. |
| gold_dim_date | One row per date covering the report period; shared date filters. |
| gold_dim_zone | One row per delivery zone; descriptive grouping and mapping limitations. |

Include the synthetic-data flag in order outputs. Gold order totals must reconcile to accepted Silver orders. Do not sum the same order counts across the three aggregate tables.

Only add a daily weather/order comparison table after verifying overlapping dates, station metadata and observation-period alignment. Aggregate orders before joining daily weather; do not use daily weather to explain hourly patterns. Keep unmatched dates visible or document any restricted comparison period.

## 9. Technical architecture

```text
Public weather files + fictional orders + area mapping
                         |
                         v
                 Azure Databricks
          Ingest -> Bronze -> validate -> Silver
          Bronze/Silver Delta tables in ADLS Gen2
                         |
             Databricks Gold transformations
                         |
               Publish validated Delta tables
                         v
              Microsoft Fabric Lakehouse
                   Gold in OneLake
                         |
                         v
                Power BI semantic model
                         |
                         v
                One-page Power BI report
```

### Platform responsibilities

- **Azure Databricks:** source ingestion, Bronze/Silver processing, quarantine, Gold calculations, reconciliation and publication. Use Python, PySpark and Spark SQL notebooks coordinated by a Databricks job.
- **ADLS Gen2:** durable Bronze/Silver Delta storage and source-file retention, with Databricks access configured through Unity Catalog.
- **Microsoft Fabric:** Gold Lakehouse storage in OneLake and access for reporting through its Lakehouse and SQL analytics endpoint. Fabric notebooks and Data Factory pipelines are optional later additions, not duplicate transformation pipelines for version one.
- **Power BI:** semantic relationships, measures, filters and visual presentation over Fabric Gold data.
- **Git/GitHub:** versioned code, notebook exports, job configuration and documentation. Keep credentials out of the repository.

### Databricks-to-Fabric handoff

1. Create the Fabric workspace and Gold Lakehouse, and confirm the chosen Databricks compute can access OneLake.
2. Configure Microsoft Entra service-principal authentication, the required Fabric workspace permissions and network access. Store credentials in Databricks secrets or Azure Key Vault.
3. For standard/job compute, use the supported Spark ABFS/OAuth integration to write Delta tables to OneLake. Copy the destination table path from Fabric, including its schema segment where applicable. Serverless compute requires a different supported authentication/write approach; do not assume the standard Spark configuration works there.
4. Validate Gold outputs before publishing. For this small historical sample, replace each complete Gold table on a successful rerun instead of appending duplicate aggregates. Record the publication batch identifier and completion status.
5. Use Databricks as the sole writer for these table paths and use Delta features compatible with Fabric readers. Verify that published tables appear in the Lakehouse and can be queried through the SQL analytics endpoint.
6. Refresh or frame the Power BI semantic model only after every Gold table is published and reconciliation succeeds. Individual Delta commits do not provide a transaction across all Gold tables. Prevent overlapping publication jobs; on partial failure, mark the batch failed and rerun the full publication before exposing it as complete.

### Power BI connection and model

- Create an explicit semantic model over the Fabric Gold tables. Use Direct Lake where the available Fabric capacity and table configuration support it. For this small sample, Import from the Fabric Lakehouse SQL analytics endpoint is an acceptable documented fallback.
- Connect the report to this semantic model. Keep ingestion, cleaning and business aggregates in Databricks rather than duplicating them in Power Query.
- Relate gold_dim_date one-to-many to the date column of each aggregate/weather table, using single-direction filtering. Relate gold_dim_zone to gold_orders_by_zone. Do not join aggregate fact tables directly to one another.
- Define Total Orders from gold_orders_daily; use the matching aggregate for hourly and zone visuals. A date slicer must filter all relevant visuals. Version one does not require a zone slicer to filter the daily/hourly tables, whose grain lacks zone.
- Plot weather measures separately with their station and units visible. Missing weather must remain missing in visuals.
- Verify refresh behavior, report access and required author/viewer licences. Display the analysis period, synthetic-data label and last successful publication time.

### Setup prerequisites and reference documentation

Confirm Azure Databricks workspace/compute, ADLS Gen2 access, a Fabric workspace with suitable capacity, a Gold Lakehouse, and Power BI authoring/sharing permissions. Record chosen runtime, storage paths and configuration without secrets. Do not assume Databricks Free Edition or a Fabric trial supports the full integration.

Implementation references:

- [Microsoft: Integrate OneLake with Azure Databricks](https://learn.microsoft.com/en-us/fabric/onelake/onelake-azure-databricks)
- [Microsoft: Delta Lake interoperability in Fabric](https://learn.microsoft.com/en-us/fabric/fundamentals/delta-lake-interoperability)
- [Microsoft: Direct Lake overview](https://learn.microsoft.com/en-us/fabric/fundamentals/direct-lake-overview)

## 10. Data strategy and assumptions

- Use the existing broad Melbourne delivery zones as the prototype area; describe weather as an approximate Melbourne proxy, consistent with Data_Assumptions_and_Limitations.md.
- Explain how weather locations represent delivery zones.
- Preserve timestamps and transformation details.
- Use consistent time handling and document daylight-saving assumptions.
- Match the analysis to the source’s time resolution.
- Keep synthetic data clearly labelled.

## 11. Project phases and completion criteria

Data exploration is considered complete for this planning revision, based on the project owner's assessment. Preserve the existing exploration notebook and Data_Assumptions_and_Limitations.md as inputs to implementation. Source metadata and date-alignment checks remain implementation gates.

### Phase 1: Access and planning

Complete when:

- Databricks, ADLS Gen2, Fabric capacity and Power BI access are confirmed
- a small Databricks-to-OneLake Delta write and Fabric read are verified
- weather source is selected and documented
- order model and fields are defined

### Phase 2: Small datasets

Complete when:

- weather data is inspected
- fictional order data can be generated in Python
- columns and assumptions are documented

### Phase 3: Original storage

Complete when:

- Databricks ingestion creates Bronze Delta tables in ADLS Gen2
- origin metadata is recorded or inherited
- raw source files and repeatable ingestion metadata are retained

### Phase 4: Cleaning and validation

Complete when:

- Databricks transformations create Silver Delta tables in ADLS Gen2
- quality checks pass for valid records
- invalid records are quarantined with reasons

### Phase 5: Summary generation

Complete when:

- daily, hourly and zone summaries are reproducible
- Databricks publishes Gold Delta tables to the Fabric Lakehouse
- Gold tables reconcile with Silver and are readable through Fabric

### Phase 6: First report

Complete when:

- a Power BI semantic model connects to Fabric Gold using the documented connection mode
- one report page answers the five core questions
- report filters and explanatory labels are present

### Phase 7: Automation

Complete when:

- a Databricks job runs ingestion, validation, Gold transformation and publication in dependency order
- Power BI refresh/framing occurs only after successful Gold publication
- reruns do not silently duplicate records
- failures, rejected-row counts, reconciliation results and publication status are visible

## 12. Later stages (not required for first version)

- current-weather ingestion
- traffic or disruption feeds
- simulated active orders and alerts
- basic risk rules
- model experiments
- additional report pages
- public case-study material

These are future enhancements and should not be treated as part of the minimum assignment completion.

## 13. Acceptance criteria

The assignment is complete when all of the following are true:

- A permitted historical weather source is documented.
- Fictional orders can be regenerated using stored Python code.
- Databricks ingests Bronze inputs into ADLS Gen2 with source information.
- Databricks Silver tables pass documented quality checks and invalid rows are quarantined.
- Databricks reproducibly generates Gold and publishes it as Delta tables in Fabric OneLake.
- Rerunning the same inputs does not duplicate records or change reconciled totals.
- A Power BI report reads Fabric Gold through a semantic model and answers the required questions.
- Date filters work across order and weather visuals, with station, unit and missing-data handling verified.
- Code and notebook exports are saved in GitHub.
- Synthetic data is clearly labelled.
- The repository contains a README or equivalent documentation explaining setup and assumptions.

## 14. Repository expectations

Suggested structure:

```text
fulfilment-pulse/
|-- README.md
|-- .gitignore
|-- requirements.txt
|-- docs/
|   |-- project-plan.md
|   |-- data-sources.md
|   |-- data-dictionary.md
|   |-- assumptions-and-limitations.md
|   `-- architecture.md
|-- src/
|   |-- generate_orders.py
|   `-- collect_weather.py
|-- notebooks/databricks/
|   |-- 01_load_bronze.ipynb
|   |-- 02_clean_silver.ipynb
|   |-- 03_build_gold.ipynb
|   `-- 04_publish_gold_to_fabric.ipynb
|-- jobs/
|   `-- fulfilment_pipeline.json
|-- fabric/
|   `-- lakehouse-setup.md
|-- schemas/
|-- tests/
|-- power-bi/
`-- sample-data/
```

## 15. Deliverables

- project README
- source code for synthetic order generation and weather collection
- Databricks notebook exports for Bronze, Silver, Gold transformation and Fabric publication
- Databricks job configuration and Fabric Lakehouse setup instructions
- Power BI semantic model, connection mode and refresh instructions
- schema or dictionary documentation
- quality-check documentation
- Power BI report or exported report assets
- project plan and assumptions notes

## 16. Constraints and principles

- Do not use real retail or customer data.
- Do not claim that simulated outcomes reflect real operational performance.
- Do not assume a free account or trial automatically provides sufficient Fabric capacity.
- Keep the first version understandable, reproducible and clearly labelled as synthetic.
- Prefer simple working solutions over more complex tooling that is not needed.

## 17. Summary

This assignment is a first-version Azure Databricks, Microsoft Fabric and Power BI analytics prototype for a fictional fulfilment scenario. It should demonstrate ingestion, cleaning and transformation in Databricks, Gold storage and serving in Fabric, and dashboarding in Power BI using public weather plus synthetic retail orders. The primary goal is a clear, repeatable and well-documented example that can sit in a portfolio and be extended later.

