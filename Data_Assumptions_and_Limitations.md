# Data Assumptions and Limitations

## Purpose

This project combines public historical weather observations with fictional fulfilment orders to demonstrate a data analytics workflow for Melbourne. The order records are synthetic. The project is a learning and portfolio prototype, not a representation of a real retailer or delivery operation.

This note records the assumptions used to explore the data and the limits that should be kept in mind when interpreting results.

## Data currently in the project

**Restoration context (12 October 2026):** The following describes the earlier documented sample restored from commit `e087d99`. Source CSVs are not currently tracked on this `main` branch. Verify station IDs, date coverage and actual inputs in the recovered Databricks folder before relying on these descriptions. Earlier local rainfall changes used station `086338`, while the baseline below records `086232`; resolve source selection explicitly. See [working instructions](docs/Git_Recovery_Notes.md).

|Dataset|Current contents|Notes|
|-|-|-|
|Fictional orders|30 records dated 1-6 January 2026|Includes six broad Melbourne delivery-zone labels and simulated order attributes. Every row is labelled synthetic.|
|Temperature|Bureau of Meteorology station number 086338|Daily maximum-temperature observations. Confirm the official station location and the usable date coverage before analysis.|
|Rainfall|Bureau of Meteorology station number 086232|Daily rainfall observations. Confirm the official station location and the usable date coverage before analysis.|

The temperature and rainfall files have different station numbers. They should not be described as measurements from the same location unless the station metadata confirms that interpretation.

## Data download and URL

https://www.bom.gov.au/climate/data/

**procedure: Rainfall**



1. Select Rainfall in "Data about" section under Text search and Type of data Daily/
2. Select weather station to be Melbourne.
3. add matching town to be 'Melbourne, VIC, 37.84°S, 144.98°E.
4. Nearest Burea stations select "086338 Melbourne (Olympic Park) VIC (1.6km away).
5. selected select year as "2026".
6. select get data.
7. You will be directed to another page and on the top right above the dable select "all years of data".



**procedure: Temperature**



1. Select Temperature in "Data about" section under Text search and Type of data Daily
2. Select weather station to be Melbourne.
3. add matching town to be 'Melbourne, VIC, 37.84°S, 144.98°E
4. Nearest Burea stations select "086338 Melbourne (Olympic Park) VIC (1.6km away)
5. selected select year as "2026"
6. select get data
7. You will be directed to another page and on the top right above the dable select "all years of data"





## Assumptions

1. **Orders are fictional.** The order records, delivery zones, item counts, fulfilment stages, basket categories, and simulated delay flags are created for demonstration. They are not actual retail or delivery records.
2. **Weather represents inner Melbourne approximately.** For this prototype, the weather observations are treated as general inner-Melbourne conditions. They are not assumed to describe the exact conditions in every delivery zone. Verify the official station metadata and record the source links before publishing the project.
3. **Delivery zones are broad labels.** The six zone names are used to group fictional orders. They do not currently provide precise boundaries, addresses, or coordinates.
4. **Order timestamps are Melbourne local time.** The CSV timestamps do not include a time-zone offset. Treat them as Melbourne local time unless the data-generation process specifies otherwise. Document daylight-saving handling if timestamps are converted or compared across seasons.
5. **Weather and orders are compared at daily level.** The weather data is daily, so order records should be aggregated by date before comparison. Daily weather cannot explain changes between individual order hours.
6. **The current sample is illustrative.** The 30 orders cover only six days. They are enough to demonstrate loading, grouping, validation, and reporting steps, but not to represent long-term demand patterns.
7. **Missing observations remain missing.** A blank weather value is not equivalent to zero rainfall or zero temperature. Preserve and flag missing values during cleaning.

## Limitations

* The order data is synthetic, so patterns in it do not establish how real Melbourne customers or fulfilment teams behave.
* Six days of orders are too little to support reliable claims about weekly, seasonal, or annual patterns.
* One weather station per measure cannot represent weather variation across all Melbourne delivery zones.
* The station IDs differ between the temperature and rainfall files. Their locations and date coverage must be checked before combining the measures as one local weather record.
* There is no precise zone-to-weather-station mapping in the current data. Zone-specific weather effects cannot be assessed from these files.
* A relationship between weather and simulated order activity does not prove that weather caused a change in demand or delays.
* The simulated delay flag is not an observed delivery outcome and should not be presented as a real service-performance measure.
* Other possible influences, such as promotions, public holidays, traffic, inventory, staffing, and delivery capacity, are not represented in the current order data.
* The source URL, download date, and applicable terms for the weather files should be recorded alongside the project before public release.

## Interpretation guidance

The current data can demonstrate how to inspect weather and order files, check data quality, aggregate orders by date or zone, and build a prototype reporting workflow. It can support a small illustrative comparison of daily Melbourne-proxy weather and fictional order totals after confirming matching dates.

Do not claim that the analysis predicts real fulfilment outcomes, measures actual demand, or shows that weather caused delays. Describe results as observations from this synthetic sample and identify the assumptions above.

## Checks before joining the datasets

* Confirm the official locations and metadata for weather stations 086338 and 086232.
* Confirm valid dates and missing observations in both weather files.
* Identify the dates shared by the order and weather datasets.
* Confirm and document the timezone interpretation of order timestamps.
* Aggregate orders to daily totals for comparison with daily weather.
* Check that any join preserves the expected row counts and does not duplicate orders.

## Related project documents

* [Assignment specifications](Fulfilment_Pulse_Assignment_Specs.md)
* [Fabric master blueprint](Fulfilment_Pulse_Fabric_Master_Blueprint.md)

