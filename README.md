# MP1 Data Pipeline

At a high level, the pipeline takes a dataset in, and outputs a cleaned one that reads more consistently, doing things such as removing text where numbers should be, awkward blanks, and odd outliers in numeric columns. pipeline.py at the project root coordinates the whole run, with modules in src/, settings in config/config.yaml, test data in fixtures/, and the generated results in output/. At a more granular level, pipeline.py parses the command-line arguments, utils.py sets up logging and checks taht the input and config files exist, and then load_data() from data_loaders.py loads the data. This function takes in various file types, (.json, .yaml, .csv) and returns the matching python object based on what was inputted (.json -> python dict/list, .yaml -> python object, .csv -> DataFrame). From here, the data gets validated in data_validator.py which removes rows with non numeric ratings, and checks that the required columns exist, raising a ValueError if one is missing. Validation comes prior to processing as when finding outliers via the IQR formula, it could break on text. Next, data_processor.py follows the setting in config.yaml to remove any duplicate rows with missing values, and rating outlies found with the IQR formula and builds the cleaning report that compares data before and after. Lastly data_output.py saves the cleaned data as a CSV in output/.

## Example:
python pipeline.py --input fixtures/sample_data.csv --output output/clean.csv --config config/config.yaml --verbose

## output: 

14:35:43 DEBUG    __main__ — Arguments parsed: input=fixtures/sample_data.csv, config=config/config.yaml, output=output/clean.csv
14:35:43 INFO     src.utils — Input file validated: fixtures/sample_data.csv
14:35:43 INFO     src.utils — Input file validated: config/config.yaml
14:35:43 INFO     src.data_loaders — Loaded CSV file: fixtures/sample_data.csv (100 rows)
14:35:43 INFO     src.data_loaders — Loaded YAML file: config/config.yaml
14:35:43 WARNING  src.data_validator — Removed 2 rows with invalid numeric values in rating
14:35:43 DEBUG    src.data_validator — Validation: 100 -> 98 rows
14:35:43 INFO     __main__ — Validation complete: 100 -> 98 rows
14:35:43 DEBUG    src.data_processor — remove_duplicates: 98 → 96 rows
14:35:43 DEBUG    src.data_processor — handle_missing: 96 → 94 rows
14:35:43 DEBUG    src.data_processor — rating: method=iqr, threshold=1.5, lower=43.625, upper=106.625, removed=2
14:35:43 INFO     __main__ — Processing complete: 98 -> 92 rows
14:35:43 DEBUG    src.data_output — Saved 92 rows to output/clean.csv
14:35:43 INFO     __main__ — Saved cleaned data to output/clean.csv

Cleaning report:
{'rows_before': 98,
 'rows_after': 92,
 'rows_removed': 6,
 'columns_before': 5,
 'columns_after': 5,
 'columns_removed': 0}