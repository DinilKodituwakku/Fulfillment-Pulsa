# Fulfilment Pulse

A learning and portfolio project combining fictional Melbourne orders and public historical weather. The planned workflow uses Azure Databricks for ingestion and transformation, ADLS Gen2 for Bronze/Silver, Microsoft Fabric OneLake for Gold, and Power BI for reporting.

## Planning documents

| Document | Purpose |
| --- | --- |
| [Project specification](Fulfilment_Pulse_Assignment_Specs.md) | Scope, architecture, table design and deliverables |
| [Requirements and acceptance](docs/Requirements_and_Acceptance.md) | Numbered requirements and completion evidence |
| [Implementation blueprint](Fulfilment_Pulse_Fabric_Master_Blueprint.md) | Platform responsibilities and build sequence |
| [Data assumptions and limitations](Data_Assumptions_and_Limitations.md) | Data origins, station differences and interpretation limits |
| [Recovery and working instructions](docs/Git_Recovery_Notes.md) | How to keep using the recovery Git folder on main |
| [Historical Fabric-only plan](docs/archive/Fulfilment_Pulse_Fabric_Only_Blueprint.md) | Archived earlier design; superseded by the current specification |

## Working baseline

Use the recovered Databricks Git folder on `main` for ongoing work. The notebook files already present on this branch are working material. Documentation restoration does not reorganise or replace those notebooks. Platform deployment and report execution have not been verified by inspecting this repository.

The original sample has 30 synthetic orders covering 1-6 January 2026 and six broad Melbourne zones. Source CSVs are not currently tracked on this branch; source descriptions restored from the earlier branch describe the historical sample and must be checked against the data actually used in Databricks.

## Minimum release

1. Retain original sources and ingest Bronze with lineage metadata.
2. Validate Silver and quarantine rejected records with reasons.
3. Build daily, date/hour and date/zone summaries and publish Gold to Fabric.
4. Create a Power BI semantic model and one-page historical report.
5. Demonstrate reconciliation, repeatable runs and failure recovery.

Keep synthetic orders visibly labelled. Daily weather is approximate Melbourne context, not precise zone coverage or hourly weather evidence. Streaming, live alerts and machine learning are later extensions.
