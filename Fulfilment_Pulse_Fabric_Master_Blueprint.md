# Fulfilment Pulse - Databricks, Fabric and Power BI blueprint

Updated: 12 October 2026. Follows the restored [specification](Fulfilment_Pulse_Assignment_Specs.md) and [requirements checklist](docs/Requirements_and_Acceptance.md). The recovered Databricks folder on `main` is the working folder for ongoing development.

## Planning baseline

Databricks owns ingestion, cleaning, quarantine and Gold calculations. ADLS Gen2 stores Bronze/Silver. Fabric Lakehouse / OneLake stores and serves Gold. Power BI owns relationships, measures and the historical report page. Platform access and successful execution remain to be verified.

The [older Fabric-only blueprint](docs/archive/Fulfilment_Pulse_Fabric_Only_Blueprint.md) was recovered from Git as historical material. Its architecture is superseded by the current specification.

```text
Weather CSVs + fictional orders + zone mapping
                     |
              Azure Databricks
      Bronze -> Silver -> Gold calculations
      Bronze/Silver Delta stored in ADLS Gen2
                     |
             Validated publication
                     |
         Fabric Lakehouse / OneLake Gold
                     |
           Power BI semantic model
                     |
          One-page historical report
```

## Build sequence

| Step | Work | Exit condition |
| --- | --- | --- |
| 1 | Verify compute, storage, Fabric capacity and reporting access. | Small OneLake Delta write and Fabric read succeeds. |
| 2 | Finalise source register, schema, generator and mapping. | Actual stations, units, dates and accumulation periods documented. |
| 3 | Load raw inputs and Bronze with lineage. | Inputs and row counts traceable. |
| 4 | Validate Silver and quarantine. | Quality checks and input disposition reconcile. |
| 5 | Calculate all six specified Gold tables. | Keys unique and aggregates independently reconcile to Silver. |
| 6 | Publish Gold to Fabric. | Every destination readable and batch marked complete. |
| 7 | Build Power BI model and report. | Totals, date filters, labels and missing-weather behaviour verified. |
| 8 | Automate ordered tasks and document recovery. | Successful run and failure/rerun evidence saved. |

## Integration decisions

Choose the OneLake write method for the actual Databricks compute. Microsoft documents Spark ABFS/OAuth for standard/job clusters and MSAL plus Python `deltalake` for serverless. Check prerequisites and copy the destination paths from Fabric. See [OneLake and Azure Databricks](https://learn.microsoft.com/en-us/fabric/onelake/onelake-azure-databricks).

Use secret storage, one writer per destination and Delta features supported by Fabric readers. See [Delta interoperability](https://learn.microsoft.com/en-us/fabric/fundamentals/delta-lake-interoperability). For this small historical sample, replace complete aggregates on successful reruns instead of appending duplicates.

Multi-table publication is not atomic. Prevent overlapping publication jobs, record status and test partial failure. Control model updates, including automatic updates, so a partial batch is not presented as a completed run. Choose Direct Lake or a documented Import fallback after checking the environment and [refresh behaviour](https://learn.microsoft.com/en-us/fabric/fundamentals/direct-lake-overview).

## Working rules

Keep the recovered Git folder on `main`; follow the [working instructions](docs/Git_Recovery_Notes.md) to bring in reviewed documentation. Validate source files against the historical assumptions before joining weather and orders. Finish the historical workflow before adding streaming, traffic, alerts or machine learning.
