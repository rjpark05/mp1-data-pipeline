"""
Data Processing Pipeline - CLI Template

DS 3500 - MP1
git
    python pipeline.py --input data.csv --output clean.csv
    python pipeline.py --input data.csv --output results.json --format json --verbose
"""

import argparse
import logging
import sys
from pathlib import Path
from data_loaders import load_data
from pprint import pprint
from data_processor import process_data, create_cleaning_report 


logger = logging.getLogger(__name__)


def setup_logging(verbose=False):
    """Configure logging for the pipeline."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
        datefmt="%H:%M:%S",
    )


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Data processing pipeline")
    parser.add_argument("--input", "-i", required=True, help="Path to the input file")
    parser.add_argument( "--config", "-c", required=True, help="Path to the YAML configuration file")
    parser.add_argument("--output", "-o", required=True, help="Path to the output file")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")
    return parser.parse_args()


def validate_input(filepath):
    """Check whether the input path exists and is a file."""
    if not Path(filepath).is_file():
        logger.error("Input file not found: %s", filepath)
        return False
    logger.info("Input file validated: %s", filepath)
    return True



def main():
    """Main pipeline function."""
    args = parse_arguments()
    setup_logging(args.verbose)

    logger.debug(
        "Arguments parsed: input=%s, config=%s, output=%s",
        args.input, args.config, args.output
    )

    if not validate_input(args.input):
        sys.exit(1)

    if not validate_input(args.config):
        sys.exit(1)
    
    try:
        data = load_data(args.input)
        config = load_data(args.config)
    except ValueError:
        sys.exit(1)

    df_before = data.copy()

    try: 
        df_after = process_data(data, config)
    except ValueError:
        sys.exit(1)

    report = create_cleaning_report(df_before, df_after)
    pprint(report, sort_dicts=False)
    logger.info(
        "Processing complete: %d -> %d rows",
        report["rows_before"], report ["rows_after"],
    )

    df_after.to_csv(args.output, index = False)
    logger.info("Saved cleaned data to %s", args.output)


if __name__ == "__main__":
    main()
