# Fulfilment Pulse — Fabric Master Project Blueprint

Updated: 11 September 2026

## 1. The project in one sentence

Build a Microsoft Fabric data project that combines public weather information and fictional retail orders to create useful dashboards, then gradually add current conditions, simulated risk alerts and predictions.

## 2. Current status and decisions

- We are planning the project. This document does not claim that infrastructure, datasets or dashboards have been built.
- Microsoft Fabric is the main data platform.
- Databricks is removed from the implementation plan.
- Fabric Data Factory replaces the planned separate Azure Data Factory service.
- OneLake and a Fabric Lakehouse replace the need for a separate Azure Data Lake Storage account in the first version.
- Python, SQL, Spark/PySpark, Git and GitHub remain core skills.
- Power BI remains the reporting tool.
- We will build the historical version first.
- The live-data technology will be chosen later, based on the available source and required update speed. Event Hubs is not a first-version requirement.
- Fabric access and the identity of the expiring trial still need to be confirmed.

## 3. Independence statement

Fulfilment Pulse is an independently developed learning prototype using public and synthetic data. It is not affiliated with Woolworths and does not represent Woolworths data, systems, processes or operational performance.

Synthetic means fictional data generated for the project. We will clearly label it in tables, reports and demonstrations.

## 4. Why build it?

Retail fulfilment involves orders, products, delivery areas and changing conditions. This project explores how data can help someone understand activity and identify areas that may need attention.

The project also provides practical portfolio experience with the Microsoft data stack and the skills used in data engineering.

The creator's frontline eCommerce experience supplies the motivation and business context. No internal employer information is needed or permitted in the project.

## 5. What the finished system could do

1. Explain historical activity: how many fictional orders arrived and when.
2. Show current external conditions: weather, and traffic if a suitable source is available.
3. Flag simulated pressure: which fictional delivery areas or orders may need investigation.
4. Test predictions: whether a model improves on a simple baseline within the simulation.
5. Explain its own reliability: when data last updated and whether checks passed.

These capabilities will arrive in separate releases, not all at once.

## 6. Intended users

| User | Question the project could help answer |
| --- | --- |
| Team leader or line manager | How is order activity changing? |
| Fulfilment team | Which fictional areas show increasing pressure? |
| Delivery team | Which simulated deliveries are exposed to external disruption? |
| Analyst | Which tables and measures explain the dashboard? |
| Data engineer | Did the pipeline run successfully, and is the data trustworthy? |
| Data scientist | Do additional features improve predictions within the simulation? |

The system supports investigation. It does not automatically make staffing, customer or safety decisions.

## 7. Scope

### First version

- One public historical weather source.
- A small fictional order dataset.
- A delivery-area mapping table.
- Fabric Lakehouse storage.
- Bronze, Silver and Gold data layers.
- Python, PySpark and SQL processing.
- Basic data-quality checks.
- One Power BI report page.
- Code and plain-English documentation in GitHub.

### Later releases

- Automated loading and processing.
- Incremental loading: process new or changed records rather than everything again.
- Current weather updates.
- Traffic information if an appropriate source is available.
- Simulated active orders and fulfilment events.
- Simple risk rules and alerts.
- Machine-learning experiments.
- Synthetic inventory and product-pressure analysis.
- Additional report pages.
- Automated tests and deployment workflows.
- Public case study, website and recorded demonstration.

### Excluded

- Real customer, employee or internal Woolworths data.
- Employer credentials, screenshots, internal documents or private processes.
- Individual employee scoring.
- Actual delivery routes or live retail inventory.
- Production deployment into a real retailer.
- Claims that simulated outcomes prove real retail effects.
- Unauthorised branding or logos.

## 8. Technology and what each tool does

| Technology | Simple meaning | Project role |
| --- | --- | --- |
| Microsoft Fabric | The main online workspace | Connect storage, processing, pipelines and reporting |
| OneLake | Fabric's underlying data storage | Hold project files and tables |
| Fabric Lakehouse | An organised place for files and analytical tables | Store Bronze, Silver and Gold data |
| Python | A programming language | Generate fictional orders and collect external data |
| Spark | A data-processing engine | Process and combine datasets |
| PySpark | Python used with Spark | Clean data and create tables in Fabric notebooks |
| SQL | A language for working with tables | Query data and calculate reporting summaries |
| Fabric notebooks | Pages where code and explanations run together | Hold Python, PySpark and Spark SQL work |
| Delta tables | Tables stored in a format designed for reliable updates | Store processed lakehouse data |
| Fabric Data Factory pipelines | A way to run tasks in order | Load data and schedule notebooks |
| Power BI | A reporting tool | Build charts, measures and report pages |
| Git | A system that tracks file changes | Keep code history |
| GitHub | An online home for the Git repository | Share code and documentation |
| pytest / GitHub Actions | Testing and automation tools | Add repeatable code checks as the project grows |
| scikit-learn / gradient-boosted models | Machine-learning libraries | Later baseline and model experiments |
| MLflow | A tool for recording model experiments | Later record datasets, settings and results |

SQL work will initially use Spark SQL in notebooks where tables need to be created or transformed. The lakehouse SQL analytics endpoint can support querying and reporting; we will not assume it behaves like a fully writable warehouse.

## 9. Technical structure

```text
Public historical weather + fictional orders + area mapping
                           |
                           v
                  MICROSOFT FABRIC
        +------------------------------------------+
        | Load files manually first                |
        | Automate with a pipeline later           |
        |                    |                     |
        |                    v                     |
        | BRONZE: original records                 |
        |                    |                     |
        | Python / PySpark: validate and clean     |
        |                    |                     |
        |                    v                     |
        | SILVER: trusted detail                   |
        |                    |                     |
        | Spark SQL: join and summarise            |
        |                    |                     |
        |                    v                     |
        | GOLD: reporting tables                   |
        |                    |                     |
        | Power BI model: relationships + measures |
        +--------------------|---------------------+
                             v
                    Power BI dashboard

GitHub holds the code, notebook exports, schemas and documentation.
The lakehouse holds the main datasets.
```

## 10. Our working method

For every stage:

1. Explain what the stage is meant to achieve.
2. Build a small working example.
3. Check the output against clear expectations.
4. Save the code and a short explanation.
5. Move on once the stage works.

We will start manually so the process is understandable. Automation comes after the underlying steps work.

We will not add a technology simply to make the tool list longer.

## 11. Data strategy

### First datasets

| Dataset | Example fields | Origin |
| --- | --- | --- |
| Historical weather | Observation time, station/location, temperature, rainfall | Public source, still to be selected |
| Fictional orders | Order ID, order time, delivery zone, item count | Python generator |
| Area mapping | Delivery zone, weather station/location | Documented project mapping |

Candidate weather sources include Bureau of Meteorology observations or another authorised historical provider. We must verify access, permissions, coverage and time resolution before selecting one.

ABS retail data can be added later for broader context. It is not a substitute for local order-level data.

### Geographic and time alignment

- Use South-East Melbourne as the prototype area.
- Clearly explain how a weather location represents each fictional delivery zone.
- Use consistent timestamps and account for Melbourne daylight saving.
- Match the analysis to the source's time resolution. Daily observations cannot support claims about hourly weather changes.
- Preserve original timestamps and record transformations.

### Origin metadata

Datasets should contain or inherit:

- `data_origin`
- `source_system`
- `source_record_id`
- `source_timestamp`, where available
- `ingestion_timestamp`
- `pipeline_run_id`
- `schema_version`
- `is_synthetic`

Public weather remains public data; combining it with fictional orders does not make those orders real.

## 12. Fictional order design

Start with:

| Field | Meaning |
| --- | --- |
| `order_id` | Unique fictional order reference |
| `order_timestamp` | When the fictional order was placed |
| `delivery_zone` | Fictional delivery-area assignment |
| `item_count` | Number of items in the order |
| `is_synthetic` | Always true for generated orders |

Example:

```text
Order ID: ORD-001
Order time: 10 September 2026, 2:30 pm Melbourne time
Delivery zone: Berwick
Item count: 18
Synthetic: true
```

The generator will have a fixed random seed so a dataset can be reproduced. Document the number of records, date range and assumptions used.

Later fields may include promised windows, fulfilment stages, basket categories and simulated delivery outcomes. Customer names and addresses are unnecessary.

## 13. Bronze, Silver and Gold

| Layer | Plain meaning | Initial contents |
| --- | --- | --- |
| Bronze | Keep the originals | Weather files, generated order files, mapping input |
| Silver | Clean and check | Valid orders, standardised weather, validated mappings |
| Gold | Prepare useful answers | Orders by day, hour and delivery area |

Suggested initial table names:

```text
bronze_orders
bronze_weather
bronze_zone_mapping

silver_orders
silver_weather
silver_zone_mapping
silver_quarantined_records

gold_orders_daily
gold_orders_hourly
gold_orders_by_zone
```

Add a weather/order analysis table when the geographic and time matching is sound. Keep the table design simple; separate lakehouses or elaborate environments are not first-version requirements.

## 14. Data-quality checks

Check that:

- Order IDs are present and unique.
- Order times can be read and fall within the intended dataset range.
- Item counts are positive whole numbers.
- Delivery zones exist in the mapping table.
- Weather values use documented units.
- Missing weather is labelled rather than silently treated as zero.
- Joins do not accidentally multiply order rows.
- Summary totals reconcile with the valid order records.

Invalid records go into a quarantine table with a reason. Quarantine means keeping bad records separately so we can inspect them.

Record how many rows arrived, passed, failed and appeared in the outputs.

## 15. First Power BI report

Start with one page containing:

| Visual | Question answered |
| --- | --- |
| Total orders | How much fictional activity is in the dataset? |
| Orders by day | Which days were busiest? |
| Orders by hour | What times were busiest? |
| Orders by delivery zone | Where did the fictional orders come from? |
| Historical weather chart | What were the observed conditions? |

Include date filters, a synthetic-data label and a clear explanation of the source period.

Weather displayed beside synthetic demand does not establish a real customer response to weather.

Later report pages can cover current conditions, delivery risk, product pressure, model performance and pipeline health.

## 16. Full roadmap and completion points

| Stage | How we do it | Finished when |
| --- | --- | --- |
| 1. Access and data planning | Confirm Fabric access; select historical source; define order fields | Access and source feasibility are understood |
| 2. Small datasets | Inspect weather; generate fictional orders in Python | Files exist and columns are explained |
| 3. Original storage | Create the Fabric Lakehouse and load Bronze | Inputs are stored with origin information |
| 4. Cleaning | Run PySpark transformations and checks | Silver tables pass checks; failures are retained separately |
| 5. Summaries | Use Spark SQL to calculate daily, hourly and zone totals | Three Gold tables reconcile with Silver |
| 6. First report | Build the Power BI model and one report page | The five initial questions can be answered |
| 7. Automation | Use Fabric pipelines to run the working loading and notebook steps | A repeatable refresh succeeds and failures are visible |
| 8. Current conditions | Add one authorised current-data source | Recent observations and freshness are visible |
| 9. Risk rules | Join conditions to simulated active orders and apply documented rules | Alerts can be explained and tested |
| 10. Machine learning | Compare baselines and models on held-out simulated data | Results and limitations are recorded |
| 11. Portfolio release | Polish reports, documentation and a recorded demo; add a website later | Someone else can understand and inspect the project |

Stages 1–6 are the first complete version. Later stages are upgrades.

## 17. First-version completion checklist

- [ ] One permitted historical source has been selected and documented.
- [ ] Fictional orders can be regenerated from saved Python code.
- [ ] Original inputs are stored in Bronze.
- [ ] Silver data passes documented quality checks.
- [ ] Three Gold tables are reproducibly generated.
- [ ] Power BI answers the five initial questions.
- [ ] Code and notebook exports are saved in GitHub.
- [ ] The README explains data origins, assumptions and how to repeat the work.
- [ ] Synthetic data is clearly labelled.

No live streaming, machine learning or website is required to finish this version.

## 18. Automation plan

Once manual processing works, create a Fabric Data Factory pipeline:

```text
Load new input
      -> Clean and validate notebook
      -> Build summary notebook
      -> Verify output and record run status
      -> Refresh reporting as required by the chosen connection mode
```

Add retries where appropriate and make failed steps visible. Re-running a load must not silently duplicate records.

Choose a schedule that fits the source's update frequency. Frequent polling does not make a daily source real-time.

## 19. Current data and streaming: later design

Begin with one current-weather source, collected on a sensible schedule.

If the source and use case justify continuous event processing, evaluate Fabric Real-Time Intelligence and Eventstreams against supported connectors, cost and required latency. Do not select the final live architecture before checking these constraints.

Possible logical flow:

```text
Authorised external source
      -> Collector or supported connector
      -> Raw event storage
      -> Validation and deduplication
      -> Current-condition table
      -> Simulated risk calculation
      -> Dashboard
```

Requirements when event processing is introduced:

- Unique event IDs.
- Source/event time and ingestion time.
- Schema versions.
- Deduplication.
- Documented handling of late events.
- Stale-data indicators.
- Original-event retention where source terms permit.
- Replay and recovery checks.

Historical records remain available. New conditions update current views and predictions rather than rewriting the past without an audit trail.

## 20. Traffic feasibility

Traffic is optional until a suitable source is verified.

Road-disruption records do not necessarily contain travel times. We cannot assume a disruption feed provides normal travel minutes or current journey duration.

If travel-time data is unavailable, use supported disruption features such as location, type and reported severity, or label travel-time values explicitly as simulated.

Historical normal-versus-current traffic comparisons require compatible data for the same place and time context.

## 21. Simple risk rules before machine learning

Begin with understandable rules. For example, a documented simulation could raise a fictional order's risk when its assigned area has a relevant disruption and the simulated order has little time remaining.

Every alert should show:

- The affected fictional order or zone.
- The rule or model that produced it.
- The supporting conditions.
- When it was calculated.
- Whether the input is stale or missing.
- That it is an investigation signal in a prototype.

Rule thresholds will be project assumptions, not claimed retail operating standards.

## 22. Research questions and hypotheses

The central question is whether external conditions can make this prototype's simulated risk estimates more responsive than order information alone.

Later experiments can ask:

1. Do external features improve prediction of simulated delays?
2. Is deviation from a normal baseline more useful than a raw value, when suitable data exists?
3. Do changes in weather add information beyond its current level?
4. Do combinations of signals help within the simulation?
5. Does more frequent processing detect a scenario earlier than scheduled reporting?
6. Does a trained model outperform simple rules?
7. Is a more complex model worth its extra effort?

These are hypotheses to test, not results already established.

## 23. Machine-learning plan

### First use case: simulated delivery delay

Target: whether a fictional delivery is delayed.

Possible features include order time, zone, item count, promised window, observed weather and documented simulated backlog. Traffic features depend on source availability.

Compare:

1. A simple majority-class or rule baseline.
2. Logistic regression.
3. A tree-based model such as a random forest or gradient boosting.
4. A neural network only if a comparison has a clear purpose.

Evaluate precision, recall, F1, PR-AUC, calibration and inference time as appropriate. Explain what the metrics mean in the report.

### Later use case: simulated demand forecasting

Predict fictional order counts for a future interval. Compare a historical-average baseline with a regression or forecasting model. Use MAE and RMSE, and inspect disruption scenarios separately.

### Honest evaluation

- Split training and testing by time where appropriate.
- Use only information available at the prediction moment.
- Keep final outcomes out of the input features.
- Test multiple simulation settings, including settings not used during training.
- Compare with the generator's known rules where useful.
- Record that synthetic results cannot establish real operational value.

If weather is programmed to cause delays, a model learning that relationship is learning the simulation. It is not proving the same relationship in a retailer.

Record dataset versions, features, settings, metrics and code versions using MLflow or an equivalent experiment record supported in the chosen environment.

## 24. Controlled demonstrations

| Scenario | What we check |
| --- | --- |
| Normal conditions | The system produces the expected stable output |
| Changing weather | The relevant feature and documented rule update |
| Traffic disruption, if supported | Only mapped areas are affected |
| Combined conditions | The simulation follows its documented assumptions |
| Duplicate record | Counts do not increase incorrectly |
| Missing or malformed data | The record is rejected, flagged or quarantined |
| Late event | The documented late-event behaviour occurs |
| Source outage | Freshness is visible and old data is not presented as current |
| Failed processing step | The run reports failure and can recover without duplication |

Measure end-to-end delay through the dashboard when demonstrating timeliness, not only the time taken by the processing code.

## 25. GitHub and repository structure

GitHub stores the instructions for making the results: code, notebook exports, schemas, tests and documentation. Main datasets belong in the lakehouse. Tiny permitted sample files may be included for demonstration.

Start with a small structure and add folders when needed:

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

Later add pipeline definitions or exports, model work, website code and GitHub Actions workflows. Direct Fabric-to-Git integration is optional and depends on access and configuration; saving exports is enough to start.

Never commit credentials or confidential data.

## 26. Testing and deployment

Introduce meaningful tests as reusable code develops:

- Generator output obeys the schema.
- Cleaning handles known bad inputs.
- Aggregation totals are correct.
- Re-running ingestion does not duplicate records.
- Invalid inputs are retained with reasons.

GitHub Actions can later run supported code tests automatically. Fabric execution checks may require a configured Fabric environment and should not be assumed to run locally unchanged.

Deployment automation is a later improvement. First document how to recreate the working project manually, then automate supported steps and document recovery.

## 27. Access, cost and trial plan

Fabric lakehouses, notebooks and other non-Power BI workloads require suitable Fabric capacity. A free user account or Power BI licence alone should not be assumed to provide that compute.

Before cloud implementation:

1. Identify whether the expiring trial is Azure/Databricks or Fabric.
2. Check the available Fabric workspace, permissions and capacity.
3. Record the trial end date, if applicable.
4. Keep code, notebook exports and reproducible sample inputs outside the trial workspace.
5. Agree on any paid capacity before incurring charges.

Microsoft documents that non-Power BI items are affected when a Fabric trial expires and that workspaces need reassignment to supported paid capacity to retain their operation. Check the current retention rules before expiry.

If Fabric access is unavailable, we can continue data inspection, generation and documentation locally. That is preparation for the Fabric build, not a claim that the Fabric pipeline is running.

## 28. Risks and controls

| Risk | Practical response |
| --- | --- |
| Too much work at once | Finish the historical dashboard before adding live features |
| Trial expiry or cost | Verify access early and preserve reproducible work outside the workspace |
| Poor source alignment | Document geography, time resolution and join rules |
| Synthetic results mistaken for reality | Label outputs and explain generator assumptions |
| Model merely learns generator rules | Test alternative scenarios and limit claims |
| Bad joins inflate order counts | Check row counts and reconcile summaries |
| Source becomes unavailable | Show freshness and use permitted saved inputs for reproducible demonstrations |
| Secrets enter GitHub | Use appropriate secret storage and scanning |
| Dashboard seems authoritative | Show assumptions and frame alerts as simulated investigation signals |

## 29. Final deliverables

### First version

- Source register and synthetic-data specification.
- Working Fabric Lakehouse.
- Bronze, Silver and Gold data.
- Python, PySpark and SQL notebooks or scripts.
- Documented quality checks.
- One Power BI report page.
- GitHub repository with repeatable instructions.
- Architecture diagram and limitations.

### Full later portfolio

- Automated Fabric pipelines.
- Current-data integration.
- Simulated alerts and scenario demonstrations.
- Model comparisons and experiment records.
- Expanded Power BI report.
- Pipeline health and freshness reporting.
- Automated code checks.
- Technical case study.
- Manager-facing presentation.
- Recorded demonstration.
- Optional public website with the independence statement.

## 30. Immediate next actions

1. Confirm which trial is ending and whether Fabric capacity is available.
2. Choose one historical weather dataset with appropriate access and coverage.
3. Open a small sample and explain its columns.
4. Agree on the date range and a few fictional delivery zones.
5. Generate a small fictional order dataset.
6. Begin the first-version build, one stage at a time.

The immediate objective is to understand the data and establish a workable Fabric environment. We do not need to build live streaming or machine learning now.

## 31. Official references

- Fabric processing and pipeline orchestration: https://learn.microsoft.com/en-us/fabric/fundamentals/prepare-transform-data
- Fabric notebook options: https://learn.microsoft.com/en-us/fabric/data-engineering/fabric-notebook-selection-guide
- Fabric licensing: https://learn.microsoft.com/en-us/fabric/enterprise/licenses
- Fabric trial and expiry: https://learn.microsoft.com/en-us/fabric/get-started/fabric-trial

These references support the platform direction. Source selection, account access, live connectors and detailed deployment settings still require validation during implementation.
