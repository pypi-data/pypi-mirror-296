import os
import re
import sys
import argparse
from collections import OrderedDict

# Add parent directory of the project to the Python path if not already present
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_dir not in sys.path:
    sys.path.append(project_dir)

# Attempt to import configuration and preprocessor libraries with fallbacks
try:
    from MediLink import MediLink_ConfigLoader
except ImportError:
    import MediLink_ConfigLoader

try:
    import MediBot_Preprocessor_lib
except ImportError:
    from MediBot import MediBot_Preprocessor_lib

import MediBot_Crosswalk_Library

def preprocess_csv_data(csv_data, crosswalk, identified_fields=None):
    """
    Preprocess CSV data by adding columns, filtering rows, sorting, deduplicating,
    combining fields, applying replacements, updating insurance and diagnosis codes,
    and validating insurance policy numbers.
    """
    try:
        # Initialize empty columns
        columns_to_add = ['Ins1 Insurance ID', 'Default Diagnosis #1', 'Procedure Code', 'Minutes', 'Amount']
        MediLink_ConfigLoader.log("Initializing empty columns in CSV data...", level="INFO")
        MediBot_Preprocessor_lib.add_columns(csv_data, columns_to_add)

        # Filter rows
        MediLink_ConfigLoader.log("Filtering out rows with missing Patient IDs and specific Primary Insurances...", level="INFO")
        MediBot_Preprocessor_lib.filter_rows(csv_data)

        # Convert 'Surgery Date' to datetime
        MediBot_Preprocessor_lib.convert_surgery_date(csv_data)

        # Sort and deduplicate records
        MediLink_ConfigLoader.log("Sorting and deduplicating patient records...", level="INFO")
        MediBot_Preprocessor_lib.sort_and_deduplicate(csv_data)
        # TODO: Handle multiple surgery dates by creating a secondary dataset or flagging records

        # Combine name and address fields
        MediLink_ConfigLoader.log("Constructing Patient Name and Address for Medisoft...", level="INFO")
        MediBot_Preprocessor_lib.combine_fields(csv_data)

        # Apply replacements
        MediLink_ConfigLoader.log("Applying mandatory replacements per Crosswalk...", level="INFO")
        MediBot_Preprocessor_lib.apply_replacements(csv_data, crosswalk)

        # Update Insurance IDs
        MediLink_ConfigLoader.log("Populating 'Ins1 Insurance ID' based on Crosswalk...", level="INFO")
        MediBot_Preprocessor_lib.update_insurance_ids(csv_data, crosswalk)

        # Update Diagnosis Codes
        MediLink_ConfigLoader.log("Populating 'Default Diagnosis #1' based on Surgery Schedule and Crosswalk...", level="INFO")
        MediLink_ConfigLoader.log("Parsing Surgery Schedules...", level="INFO")
        print("Parsing Surgery Schedules...") # Print this because it takes a long time.
        MediBot_Preprocessor_lib.update_diagnosis_codes(csv_data)

        # Update Procedure Codes
        MediLink_ConfigLoader.log("Populating 'Procedure Code' based on Crosswalk...", level="INFO")
        MediBot_Preprocessor_lib.update_procedure_codes(csv_data)

    except Exception as e:
        error_message = "An error occurred while pre-processing CSV data. Please repair the CSV directly and try again: {}".format(e)
        MediLink_ConfigLoader.log(error_message, level="ERROR")
        print(error_message)

def check_existing_patients(selected_patient_ids, MAPAT_MED_PATH):
    """
    Check for existing patients in the MAPAT.med file and separate them from those to process.
    """
    existing_patients = []
    patients_to_process = set(selected_patient_ids)

    try:
        with open(MAPAT_MED_PATH, 'r') as file:
            next(file)  # Skip header row
            for line in file:
                if line.startswith("0"):  # '0' indicates an active record
                    patient_id = line[194:202].strip()  # Extract Patient ID (Columns 195-202)
                    patient_name = line[9:39].strip()  # Extract Patient Name (Columns 10-39)

                    if patient_id in patients_to_process:
                        existing_patients.append((patient_id, patient_name))
                        patients_to_process.remove(patient_id)

    except FileNotFoundError:
        MediLink_ConfigLoader.log("MAPAT.med was not found at the specified location in the config file.", level="ERROR")
        MediLink_ConfigLoader.log("Skipping existing patient check and continuing...", level="WARNING")

    return existing_patients, list(patients_to_process)

def intake_scan(csv_headers, field_mapping, config):
    """
    Map CSV headers to Medisoft fields based on the provided field mapping.
    """
    identified_fields = OrderedDict()
    missing_fields_warnings = []
    required_fields = config.get("required_fields", [])

    # Map headers to Medisoft fields
    for medisoft_field, patterns in field_mapping.items():
        for pattern in patterns:
            matched_headers = [header for header in csv_headers if re.search(pattern, header, re.IGNORECASE)]
            if matched_headers:
                identified_fields[matched_headers[0]] = medisoft_field
                break
        else:
            if medisoft_field in required_fields:
                warning = "WARNING: No matching CSV header found for Medisoft field '{}'".format(medisoft_field)
                missing_fields_warnings.append(warning)

    # Check if CSV is blank or has only headers
    if not csv_headers or all(header.strip() == "" for header in csv_headers):
        warning = "WARNING: The CSV appears to be blank or contains only headers without data."
        missing_fields_warnings.append(warning)

    # Log missing fields warnings
    if missing_fields_warnings:
        MediLink_ConfigLoader.log("\nSome required fields could not be matched:", level="WARNING")
        for warning in missing_fields_warnings:
            MediLink_ConfigLoader.log(warning, level="WARNING")

    return identified_fields

def validate_insurance_policy_numbers(csv_data, identified_fields):
    """
    Validate that all Insurance Policy Numbers are alphanumeric.
    """
    warnings = []
    # Find the header for 'Insurance Policy Number'
    policy_field = None
    for header, field in identified_fields.items():
        if 'Insurance Policy Number' in field:
            policy_field = header
            break

    if not policy_field:
        warning = "WARNING: 'Insurance Policy Number' field is missing."
        warnings.append(warning)
        return warnings

    # Validate each policy number
    for row_num, row in enumerate(csv_data, start=2):  # Starting at 2 to account for header
        policy_number = row.get(policy_field, "")
        if policy_number and not re.match("^[a-zA-Z0-9]*$", policy_number):
            warning = "WARNING: Row {}: Insurance Policy Number '{}' contains invalid characters.".format(row_num, policy_number)
            warnings.append(warning)

    return warnings

def main():
    """
    Parse command-line arguments and execute corresponding tasks.
    """
    parser = argparse.ArgumentParser(description='Run MediLink Data Management Tasks')
    parser.add_argument('--update-crosswalk', action='store_true',
                        help='Run the crosswalk update independently')
    parser.add_argument('--init-crosswalk', action='store_true',
                        help='Initialize the crosswalk using historical data from MAPAT and Carol\'s CSV')
    parser.add_argument('--load-csv', action='store_true',
                        help='Load and process CSV data')
    parser.add_argument('--preprocess-csv', action='store_true',
                        help='Preprocess CSV data based on specific rules')
    parser.add_argument('--open-csv', action='store_true',
                        help='Open CSV for manual editing')

    args = parser.parse_args()

    # Load configuration and crosswalk data
    try:
        config, crosswalk = MediLink_ConfigLoader.load_configuration()
    except Exception as e:
        MediLink_ConfigLoader.log("Failed to load configuration: {}".format(e), level="ERROR")
        sys.exit(1)

    # If no arguments are provided, display help and exit
    if not any(vars(args).values()):
        parser.print_help()
        return

    # Execute tasks based on provided arguments
    if args.update_crosswalk:
        MediLink_ConfigLoader.log("Updating the crosswalk...", level="INFO")
        try:
            MediBot_Crosswalk_Library.crosswalk_update(config, crosswalk)
            MediLink_ConfigLoader.log("Crosswalk updated successfully.", level="INFO")
        except Exception as e:
            MediLink_ConfigLoader.log("Failed to update crosswalk: {}".format(e), level="ERROR")

    if args.init_crosswalk:
        MediLink_ConfigLoader.log("Initializing the crosswalk from MAPAT and Carol's CSV...", level="INFO")
        try:
            MediBot_Crosswalk_Library.initialize_crosswalk_from_mapat()
            MediLink_ConfigLoader.log("Crosswalk initialized successfully.", level="INFO")
        except Exception as e:
            MediLink_ConfigLoader.log("Failed to initialize crosswalk: {}".format(e), level="ERROR")

    csv_data = None
    identified_fields = OrderedDict()
    if args.load_csv or args.preprocess_csv or args.open_csv:
        try:
            MediLink_ConfigLoader.log("Loading CSV data...", level="INFO")
            csv_file_path = config.get('CSV_FILE_PATH')
            if not csv_file_path:
                raise ValueError("CSV_FILE_PATH is not defined in the configuration.")
            csv_data = MediBot_Preprocessor_lib.load_csv_data(csv_file_path)
            MediLink_ConfigLoader.log("Loaded {} records from the CSV.".format(len(csv_data)), level="INFO")
        except Exception as e:
            MediLink_ConfigLoader.log("Failed to load CSV data: {}".format(e), level="ERROR")
            sys.exit(1)

    if args.preprocess_csv:
        try:
            MediLink_ConfigLoader.log("Starting CSV preprocessing...", level="INFO")
            field_mapping = config.get('field_mapping', {})
            if not field_mapping:
                raise ValueError("Field mapping is not defined in the configuration.")

            if csv_data:
                csv_headers = list(csv_data[0].keys())
            else:
                csv_headers = []

            identified_fields = intake_scan(csv_headers, field_mapping, config)
            preprocess_csv_data(csv_data, crosswalk, identified_fields)
            MediLink_ConfigLoader.log("CSV preprocessing completed successfully.", level="INFO")
        except Exception as e:
            MediLink_ConfigLoader.log("Failed during CSV preprocessing: {}".format(e), level="ERROR")

    if args.open_csv:
        try:
            MediLink_ConfigLoader.log("Opening CSV for editing...", level="INFO")
            csv_file_path = config.get('CSV_FILE_PATH')
            if not csv_file_path:
                raise ValueError("CSV_FILE_PATH is not defined in the configuration.")
            MediBot_Preprocessor_lib.open_csv_for_editing(csv_file_path)
            MediLink_ConfigLoader.log("CSV opened for editing successfully.", level="INFO")
        except Exception as e:
            MediLink_ConfigLoader.log("Failed to open CSV for editing: {}".format(e), level="ERROR")

if __name__ == '__main__':
    main()