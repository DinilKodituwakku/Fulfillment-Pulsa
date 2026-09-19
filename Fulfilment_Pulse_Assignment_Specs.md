# Fulfilment Pulse — Assignment Specs

## 1. Project objective

Build a Microsoft Fabric learning project that combines public historical weather data with fictional retail-order data to create a clear operational dashboard and a staged analytics solution. The project should demonstrate how data engineering, reporting, quality checks and simple forecasting can be combined in a practical Microsoft data platform workflow.

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
- Fabric Lakehouse storage
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

1. Load public historical weather data into a supported data platform workflow.
2. Generate fictional orders using Python with a fixed seed for reproducibility.
3. Store raw inputs in Bronze.
4. Clean and validate the data in Silver.
5. Produce summary tables in Gold for reporting.
6. Build a Power BI dashboard with one page that answers the main questions.
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

### Bronze

Raw inputs only:

- bronze_orders
- bronze_weather
- bronze_zone_mapping

### Silver

Validated and cleaned tables:

- silver_orders
- silver_weather
- silver_zone_mapping
- silver_quarantined_records

### Gold

Reporting-ready aggregates:

- gold_orders_daily
- gold_orders_hourly
- gold_orders_by_zone

When geographic and time alignment are sound, add an analysis table for weather and order comparison.

## 9. Technical architecture

```text
Public weather + fictional orders + area mapping
                    |
                    v
              Microsoft Fabric
      -------------------------------
      | Bronze: raw source data     |
      | Silver: cleaning + checks   |
      | Gold: summary reporting     |
      -------------------------------
                    |
                    v
             Power BI dashboard
```

### Planned tools

- Microsoft Fabric
- OneLake
- Fabric Lakehouse
- Python
- PySpark
- Spark SQL
- Fabric notebooks
- Delta tables
- Fabric Data Factory pipelines
- Power BI
- Git and GitHub

## 10. Data strategy and assumptions

- Use South-East Melbourne as the prototype area.
- Explain how weather locations represent delivery zones.
- Preserve timestamps and transformation details.
- Use consistent time handling and document daylight-saving assumptions.
- Match the analysis to the source’s time resolution.
- Keep synthetic data clearly labelled.

## 11. Project phases and completion criteria

### Phase 1: Access and planning

Complete when:

- Fabric access and workspace feasibility are understood
- weather source is selected and documented
- order model and fields are defined

### Phase 2: Small datasets

Complete when:

- weather data is inspected
- fictional order data can be generated in Python
- columns and assumptions are documented

### Phase 3: Original storage

Complete when:

- Bronze tables exist
- origin metadata is recorded or inherited
- inputs are stored in the lakehouse

### Phase 4: Cleaning and validation

Complete when:

- Silver tables are created
- quality checks pass for valid records
- invalid records are quarantined with reasons

### Phase 5: Summary generation

Complete when:

- daily, hourly and zone summaries are reproducible
- Gold tables reconcile with the cleaned data

### Phase 6: First report

Complete when:

- one dashboard page answers the five core questions
- report filters and explanatory labels are present

### Phase 7: Automation

Complete when:

- repeatable pipeline steps are in place
- reruns do not silently duplicate records
- failures are visible

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
- Bronze inputs are stored and explain source information.
- Silver tables pass documented quality checks.
- Gold tables are reproducibly generated.
- A Power BI report answers the required questions.
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
|-- notebooks/
|   |-- 01_load_bronze.ipynb
|   |-- 02_clean_silver.ipynb
|   `-- 03_build_gold.ipynb
|-- schemas/
|-- tests/
|-- power-bi/
`-- sample-data/
```

## 15. Deliverables

- project README
- source code for synthetic order generation and weather collection
- notebook exports for bronze, silver and gold stages
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

This assignment is a first-version Microsoft Fabric analytics prototype for a fictional fulfilment scenario. It should demonstrate data loading, cleaning, quality checks, summarisation and dashboarding using public weather plus synthetic retail orders. The primary goal is a clear, repeatable and well-documented example that can sit in a portfolio and be extended later.
