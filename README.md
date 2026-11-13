# Fulfilment Pulse

An analytics portfolio project that follows synthetic Melbourne orders and historical weather through **Azure Databricks, Microsoft Fabric OneLake and a Power BI report built within Fabric**.

The project demonstrates data exploration, SQL and Python transformations, reporting tables, automated notebook execution and interactive reporting.

**[Explore the project and video walkthroughs](https://dinilswork.vercel.app/fulfilment-pulse/)** · **[View my portfolio](https://dinilswork.vercel.app/)**

## Project purpose

Understand order activity by date, hour and delivery zone, with historical weather providing additional Melbourne context.

The report answers:

- How many orders and items were recorded?
- How does order activity vary by day and hour?
- How are orders distributed across delivery zones?
- What weather readings are available for the selected dates?

## Data overview

The order sample contains **30 synthetic orders and 133 items**, covering **1–6 January 2026** across **six delivery zones**.

Temperature and rainfall come from historical weather datasets. They provide regional context rather than precise conditions at each delivery location.

## How the pipeline works

```text
Order and weather CSV files
            ↓
Azure Databricks
Bronze → Silver → Gold
            ↓
Publish Gold Delta tables to Fabric OneLake
            ↓
Semantic model with date and zone relationships
            ↓
Power BI report within Microsoft Fabric
```

A Databricks job runs the configured notebooks in dependency order. Publishing to Fabric uses a Microsoft Entra application identity, with credentials retrieved from Databricks secrets.

## Main notebooks

| Notebook | Purpose |
|---|---|
| [Data exploration](Data%20exploration.ipynb) | Explore the source data, missing values, date coverage and order patterns. |
| [Bronze and Silver preparation](fulfilment_pulsa_bronze_and_silver.ipynb) | Ingest source data, inspect records and prepare fields for analysis. |
| [Gold reporting tables](fulfillment_gold.ipynb) | Build daily, hourly and delivery-zone summaries, weather data and dimensions. |
| [Publish Gold to Fabric](04_Gold_to_fabric.ipynb) | Authenticate and write the listed Gold tables to the Fabric lakehouse. |

The Fabric publishing notebook lists five tables. The date dimension was published separately during setup.

## Gold tables

| Table | Purpose |
|---|---|
| `gold_daily_orders` | Summarise order and item totals by date. |
| `gold_hourly_orders` | Summarise order activity by date and hour. |
| `gold_orders_by_zone` | Compare order and item totals by date and delivery zone. |
| `gold_daily_weather` | Store weather observations with their dates, stations, measures and units. |
| `gold_dim_date` | Provide shared calendar attributes for consistent date filtering. |
| `gold_dim_zone` | Describe delivery zones and document mapping assumptions. |

The three order summary tables represent the same underlying orders at different levels of detail. Their totals should not be added together.

## Report

The Power BI report was created inside Microsoft Fabric and includes:

- Total orders and total items.
- Daily order and item charts.
- Hourly order activity.
- Orders by delivery zone.
- Separate rainfall and maximum-temperature visuals.
- A date slicer connected through the semantic model.

The website preserves recorded walkthroughs of the implementation and report. Its sample explorer uses static project totals and does not connect to a live Fabric workspace.

## What I learned

- **Dates affect joins and filtering.** Daily weather joins required converting order timestamps to dates while retaining the hour for hourly analysis.
- **Authentication and permissions are separate.** Valid application credentials were not enough—the application also needed access to the Fabric workspace.
- **Schema changes affect downstream reports.** Renaming a column required aligning the Databricks table, published Delta schema and semantic model.
- **Jobs simplify repeatable execution.** Running the configured workflow was easier than manually running each notebook.
- **Reports need validation.** I checked report totals against the underlying tables and tested date filtering across visuals.

## Running the project

This repository contains notebook exports and project documentation. Reproducing the cloud workflow requires your own Databricks and Fabric environments.

1. Review the source requirements and data assumptions.
2. Configure source file locations and destination tables for your environment.
3. Run the ingestion and Silver preparation steps, followed by Gold.
4. Configure your own Entra application, Databricks secrets and Fabric permissions.
5. Update the publishing destination to your Fabric workspace and lakehouse.
6. Publish the reporting tables and create the semantic relationships and report.
7. Configure a Databricks job with the required notebook dependencies.

Workspace paths and identifiers in the notebooks are environment-specific. Credentials should remain in secret storage and must not be committed to Git.

## Limitations

- Orders are synthetic and represent a small six-day sample.
- Weather readings are approximate Melbourne context, not zone-specific or hourly conditions.
- Missing weather readings are not equivalent to zero rainfall.
- This sample cannot establish that weather affects order demand.
- This is a learning and portfolio project, not a production service.

## Documentation and future improvements

- [Project specification](Fulfilment_Pulse_Assignment_Specs.md)
- [Data assumptions and limitations](Data_Assumptions_and_Limitations.md)
- [Requirements and acceptance checklist](docs/Requirements_and_Acceptance.md)

Some planning documents describe a broader intended solution. They should not be read as confirmation that every proposed feature is implemented.

Future improvements include stronger automated validation, rejected-record handling, publication tracking and clearer setup configuration.
