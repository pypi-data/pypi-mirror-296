from collections import OrderedDict, defaultdict
from datetime import datetime, timedelta
import os
import csv
import sys
import importlib

# Add parent directory of the project to the Python path if not already present
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_dir not in sys.path:
    sys.path.append(project_dir)

def import_with_fallback(primary, fallback, alias=None):
    try:
        module = importlib.import_module(primary)
    except ImportError:
        module = importlib.import_module(fallback)
    if alias:
        globals()[alias] = module
    return module

# Import MediLink modules with fallback
MediLink_ConfigLoader = import_with_fallback('MediLink_ConfigLoader', 'MediLink.MediLink_ConfigLoader')
MediLink_DataMgmt = import_with_fallback('MediLink_DataMgmt', 'MediLink.MediLink_DataMgmt')

# Import MediBot modules with fallback and assign specific attributes
MediBot_UI = import_with_fallback('MediBot_UI', 'MediBot.MediBot_UI')
MediBot_docx_decoder = import_with_fallback('MediBot_docx_decoder', 'MediBot.MediBot_docx_decoder')

app_control = MediBot_UI.app_control
parse_docx = MediBot_docx_decoder.parse_docx

class InitializationError(Exception):
    def __init__(self, message):
        super(InitializationError, self).__init__(message)

def initialize(config):
    """Initialize global configurations from the provided config."""
    global AHK_EXECUTABLE, CSV_FILE_PATH, field_mapping, page_end_markers
    required_keys = {
        'AHK_EXECUTABLE': '',
        'CSV_FILE_PATH': '',
        'field_mapping': OrderedDict(),
        'page_end_markers': []
    }
    for key, default in required_keys.items():
        try:
            value = config.get(key, default)
            globals()[key] = OrderedDict(value) if key == 'field_mapping' else value
        except AttributeError:
            raise InitializationError("Error: '{}' not found in config.".format(key))

def open_csv_for_editing(csv_file_path):
    """Open the CSV file with its associated application."""
    try:
        os.system('start "" "{}"'.format(csv_file_path))
        print("After saving the revised CSV, please re-run MediBot.")
    except Exception as e:
        print("Failed to open CSV file:", e)

def load_csv_data(csv_file_path):
    """Load and return CSV data as a list of dictionaries."""
    if not os.path.exists(csv_file_path):
        print("***Error: CSV file '{}' not found.".format(csv_file_path))
        print("Hint: Check if CSV file is located in the expected directory or specify a different path in config file.")
        print("Please correct the issue and re-run MediBot.")
        sys.exit(1)
    try:
        with open(csv_file_path, 'r') as csvfile:
            return list(csv.DictReader(csvfile))
    except IOError as e:
        print("Error reading CSV file: {}. Please check the file path and permissions.".format(e))
        sys.exit(1)

def add_columns(csv_data, column_headers):
    """Add one or more columns to each row in CSV data."""
    headers = [column_headers] if isinstance(column_headers, str) else column_headers
    if not isinstance(headers, list):
        raise ValueError("column_headers should be a list or a string")
    for row in csv_data:
        row.update({header: '' for header in headers})

def filter_rows(csv_data):
    """Filter out rows with empty Patient ID or excluded Primary Insurance."""
    # TODO This should go to the crosswalk.
    excluded_insurance = set(['AETNA', 'AETNA MEDICARE', 'HUMANA MED HMO'])
    csv_data[:] = [
        row for row in csv_data 
        if row.get('Patient ID', '').strip() and 
           row.get('Primary Insurance', '').strip() not in excluded_insurance
    ]

def convert_surgery_date(csv_data):
    """
    Convert 'Surgery Date' from string to datetime object.
    Handles multiple date formats and logs errors for invalid dates.
    """
    date_formats = [
        '%m/%d/%Y',  # e.g., 12/31/2023
        '%m-%d-%Y',  # e.g., 12-31-2023
        '%Y-%m-%d',  # e.g., 2023-12-31
        '%B %d, %Y', # e.g., December 31, 2023
        '%d %B %Y',  # e.g., 31 December 2023
        # Add more formats as needed
    ]
    
    for row_num, row in enumerate(csv_data, start=2):  # Starting at 2 to account for header
        date_str = row.get('Surgery Date', '').strip()
        if not date_str:
            MediLink_ConfigLoader.log(
                "Row {}: 'Surgery Date' is missing.".format(row_num), 
                level="WARNING"
            )
            row['Surgery Date'] = datetime.min
            continue
        
        converted = False
        for fmt in date_formats:
            try:
                row['Surgery Date'] = datetime.strptime(date_str, fmt)
                converted = True
                break
            except ValueError:
                continue
        
        if not converted:
            try:
                # Attempt parsing with dateutil if available
                from dateutil import parser
                row['Surgery Date'] = parser.parse(date_str)
                converted = True
            except (ImportError, ValueError):
                pass
        
        if not converted:
            MediLink_ConfigLoader.log(
                "Row {}: Invalid 'Surgery Date' format '{}'. Setting to datetime.min.".format(row_num, date_str), 
                level="ERROR"
            )
            row['Surgery Date'] = datetime.min  # Assign a minimum datetime value for sorting purposes

def sort_and_deduplicate(csv_data):
    # TODO we need to figure out a new logic here for doing second-eye charges. I don't know what the flow should be yet.
    csv_data.sort(key=lambda x: (x['Surgery Date'], x.get('Patient Last', '').strip()))
    unique_patients = {}
    for row in csv_data:
        patient_id = row.get('Patient ID')
        if patient_id not in unique_patients or row['Surgery Date'] < unique_patients[patient_id]['Surgery Date']:
            unique_patients[patient_id] = row
    csv_data[:] = list(unique_patients.values())
    # TODO Sorting, now that we're going to have the Surgery Schedules available, should (or shouldn't?? 
    # maybe we should build in the option as liek a 'setting' in the config) be ordered as the patients show up on the schedule.
    # If we don't have that surgery schedule yet for some reason, we should default to the current ordering strategy.
    csv_data.sort(key=lambda x: (x['Surgery Date'], x.get('Patient Last', '').strip()))

def combine_fields(csv_data):
    """Combine first, middle, and last names, and address fields into single fields."""
    for row in csv_data:
        row['Surgery Date'] = row['Surgery Date'].strftime('%m/%d/%Y')
        middle = row.get('Patient Middle', '').strip()
        middle = middle[0] if len(middle) > 1 else middle
        row['Patient Name'] = "{}, {} {}".format(
            row.get('Patient Last', '').strip(), 
            row.get('Patient First', '').strip(),
            middle
        ).strip()
        row['Patient Street'] = "{} {}".format(
            row.get('Patient Address1', '').strip(),
            row.get('Patient Address2', '').strip()
        ).strip()

def apply_replacements(csv_data, crosswalk):
    """Apply CSV replacements based on the crosswalk."""
    replacements = crosswalk.get('csv_replacements', {})
    target_fields = ['Patient SSN', 'Primary Insurance', 'Ins1 Payer ID']
    for row in csv_data:
        for old, new in replacements.items():
            for field in target_fields:
                if row.get(field, '') == old:
                    row[field] = new

def update_insurance_ids(csv_data, crosswalk):
    """Update Insurance IDs in CSV data based on the crosswalk."""
    for row in csv_data:
        ins1_payer_id = row.get('Ins1 Payer ID', '').strip()
        if ins1_payer_id:
            payer_info = crosswalk.get('payer_id', {}).get(ins1_payer_id)
            if payer_info:
                medisoft_ids = [int(id_) for id_ in payer_info.get('medisoft_id', []) if id_]
                if medisoft_ids:
                    # TODO Enhance insurance ID assignment by matching 'Primary Insurance' with MAINS data:
                    # 1. Extract the insurance name from the current row:
                    #    insurance_name = row.get('Primary Insurance', '').strip()
                    # 2. Retrieve associated insurance names from MAINS using the current medisoft_ids:
                    #    associated_insurances = [id_to_insurance[mid] for mid in medisoft_ids if mid in id_to_insurance]
                    # 3. Utilize approximate string matching (e.g., difflib.get_close_matches) to find the closest match:
                    #    matched_insurance = difflib.get_close_matches(insurance_name, associated_insurances, n=1, cutoff=0.8)
                    # 4. If a close match is found:
                    #       a. Identify the corresponding medisoft_id for the matched insurance name
                    #       b. Assign the matched medisoft_id to 'Ins1 Insurance ID':
                    #          row['Ins1 Insurance ID'] = matched_medisoft_id
                    # 5. If no suitable match is found:
                    #       a. Fallback to the first medisoft_id in the list:
                    #          row['Ins1 Insurance ID'] = medisoft_ids[0]
                    # 6. Ensure that the fallback assignment is always executed to maintain production stability
                    # 7. Optimize performance by loading MAINS data once during initialization and reusing it across function calls
                    #    (Consider using global variables or passing mappings as function parameters)
                    row['Ins1 Insurance ID'] = medisoft_ids[0] 
                    # MediLink_ConfigLoader.log("Ins1 Insurance ID '{}' used for Payer ID {} in crosswalk.".format(row.get('Ins1 Insurance ID', ''), ins1_payer_id))
            else:
                MediLink_ConfigLoader.log(
                    "Ins1 Payer ID '{}' not found in the crosswalk.".format(ins1_payer_id)
                )
                crosswalk.setdefault('payer_id', {})[ins1_payer_id] = {
                    'medisoft_id': [],
                    'medisoft_medicare_id': [],
                    'endpoint': 'OPTUMEDI'  # BUG HARDCODE DEFAULTS
                }

def update_procedure_codes(csv_data):
    """Update 'Procedure Code' in CSV data based on diagnosis codes."""
    # TODO Move hardcoded mappings to crosswalk.json
    medisoft_to_diagnosis = {
        "25811": "H25.811",
        "25812": "H25.812",
        "2512": "H25.12",
        "2511": "H25.11", 
        "529XA": "T85.29XA",
        "4301": "H43.01",
        "4302": "H43.02",
        "011X2": "H40.11X2",
        "051X3": "H40.51X3",
        "5398A": "T85.398A"
    }  # BUG with 2511 truncation

    procedure_to_diagnosis = {
        "00142": ["H25.811", "H25.812", "H25.12", "H25.11", "T85.29XA"],
        "00145": ["H43.01", "H43.02"],
        "00140": ["H40.11X2", "H40.51X3"]
    }

    diagnosis_to_procedure = {diag: proc for proc, diags in procedure_to_diagnosis.items() for diag in diags}
    updated_count = 0

    for row_num, row in enumerate(csv_data, start=1):
        try:
            medisoft_code = row.get('Default Diagnosis #1', '').strip()
            diagnosis_code = medisoft_to_diagnosis.get(medisoft_code)
            if diagnosis_code:
                procedure_code = diagnosis_to_procedure.get(diagnosis_code, "Unknown")
                row['Procedure Code'] = procedure_code
                if procedure_code != "Unknown":
                    updated_count += 1
            else:
                row['Procedure Code'] = "Unknown"
        except Exception as e:
            MediLink_ConfigLoader.log(
                "In update_procedure_codes, Error processing row {}: {}".format(row_num, e), 
                level="ERROR"
            )

    MediLink_ConfigLoader.log("Total {} 'Procedure Code' rows updated.".format(updated_count), level="INFO")

def update_diagnosis_codes(csv_data):
    """
    Update 'Default Diagnosis #1' in CSV data based on DOCX files.
    """
    try:
        config, _ = MediLink_ConfigLoader.load_configuration()
        local_storage_path = config['MediLink_Config']['local_storage_path']
        all_patient_data = {}

        # Determine date range based on surgery dates
        surgery_dates = [
            row.get('Surgery Date') for row in csv_data 
            if row.get('Surgery Date') and row.get('Surgery Date') != datetime.min
        ]

        if surgery_dates:
            # Ensure all surgery_dates are datetime objects
            surgery_dates = [date for date in surgery_dates if isinstance(date, datetime)]
            if not surgery_dates:
                raise ValueError("No valid 'Surgery Date' entries found after conversion.")

            earliest_date = min(surgery_dates)
            latest_date = max(surgery_dates)
            margin_days = 5  # Define a margin of 5 days
            lower_bound_date = earliest_date - timedelta(days=margin_days)
            upper_bound_date = latest_date + timedelta(days=margin_days)
            MediLink_ConfigLoader.log("Computed surgery date range from {} to {} with a margin of {} days.".format(
                lower_bound_date.strftime("%m-%d-%Y"),
                upper_bound_date.strftime("%m-%d-%Y"),
                margin_days
            ), level="INFO")
            use_dynamic_cutoff = True
        else:
            # Default to 45-day cutoff if surgery dates are unavailable
            threshold_date = datetime.now() - timedelta(days=45)
            MediLink_ConfigLoader.log("No valid surgery dates found. Using default 45-day cutoff.", level="WARNING")
            use_dynamic_cutoff = False

        for filename in os.listdir(local_storage_path):
            if filename.endswith(".docx"):
                filepath = os.path.join(local_storage_path, filename)
                file_mod_time = datetime.fromtimestamp(os.path.getmtime(filepath))

                # Determine if the DOCX file should be processed
                if use_dynamic_cutoff:
                    if lower_bound_date <= file_mod_time <= upper_bound_date:
                        process_file = True
                    else:
                        process_file = False
                else:
                    if file_mod_time >= threshold_date:
                        process_file = True
                    else:
                        process_file = False

                if process_file:
                    MediLink_ConfigLoader.log("Processing DOCX file: {}".format(filepath), level="INFO")
                    try:
                        patient_data = parse_docx(filepath)  # Ensure parse_docx is defined elsewhere
                        for patient_id, service_dates in patient_data.items():
                            all_patient_data.setdefault(patient_id, {}).update(service_dates)
                    except Exception as e:
                        MediLink_ConfigLoader.log(
                            "Error parsing DOCX file {}: {}".format(filepath, e), 
                            level="ERROR"
                        )
                else:
                    if use_dynamic_cutoff:
                        MediLink_ConfigLoader.log(
                            "Skipping DOCX file (outside surgery date range): {}".format(filepath), 
                            level="INFO"
                        )
                    else:
                        MediLink_ConfigLoader.log(
                            "Skipping DOCX file (older than 45 days): {}".format(filepath), 
                            level="INFO"
                        )

        MediLink_ConfigLoader.log("All patient data collected from DOCX files: {}".format(all_patient_data), level="INFO")
        diagnosis_to_medisoft = {
            "H25.811": "25811",
            "H25.812": "25812",
            "H25.12": "2512",
            "H25.11": "2511",
            "T85.29XA": "529XA",
            "H43.01": "4301",
            "H43.02": "4302",
            "H40.11X2": "011X2",
            "H40.51X3": "051X3",
            "T85.398A": "5398A"
        }  # BUG with 2511 truncation

        updated_count = 0

        for row_num, row in enumerate(csv_data, start=1):
            MediLink_ConfigLoader.log("Processing row number {}.".format(row_num), level="INFO")
            patient_id = row.get('Patient ID', '').strip()
            surgery_date = row.get('Surgery Date', '')
            surgery_date_str = surgery_date.strftime("%m-%d-%Y") if isinstance(surgery_date, datetime) and surgery_date != datetime.min else ''

            MediLink_ConfigLoader.log(
                "Patient ID: {}, Surgery Date: {}".format(patient_id, surgery_date_str), 
                level="INFO"
            )

            if patient_id in all_patient_data:
                if surgery_date_str in all_patient_data[patient_id]:
                    diagnosis_code, left_or_right_eye, femto_yes_or_no = all_patient_data[patient_id][surgery_date_str]
                    MediLink_ConfigLoader.log(
                        "Found diagnosis data for Patient ID: {}, Surgery Date: {}".format(
                            patient_id, surgery_date_str
                        ), 
                        level="INFO"
                    )
                    
                    defaulted_code = diagnosis_code[1:].replace('.', '')[-5:] if diagnosis_code else ''
                    medisoft_shorthand = diagnosis_to_medisoft.get(diagnosis_code, defaulted_code)
                    MediLink_ConfigLoader.log(
                        "Converted diagnosis code to Medisoft shorthand: {}".format(medisoft_shorthand), 
                        level="INFO"
                    )
                    
                    row['Default Diagnosis #1'] = medisoft_shorthand
                    updated_count += 1
                    MediLink_ConfigLoader.log(
                        "Updated row number {} with new diagnosis code.".format(row_num), 
                        level="INFO"
                    )
                else:
                    MediLink_ConfigLoader.log(
                        "No matching surgery date found for Patient ID: {} in row {}.".format(patient_id, row_num), 
                        level="INFO"
                    )
            else:
                MediLink_ConfigLoader.log(
                    "Patient ID: {} not found in DOCX data for row {}.".format(patient_id, row_num), 
                    level="INFO"
                )

        MediLink_ConfigLoader.log("Total {} 'Default Diagnosis #1' rows updated.".format(updated_count), level="INFO")

    except Exception as e:
        message = "An error occurred while updating diagnosis codes. Please check the DOCX files and configuration: {}".format(e)
        MediLink_ConfigLoader.log(message, level="ERROR")
        print(message)
        
def load_data_sources(config, crosswalk):
    """Load historical mappings from MAPAT and Carol's CSVs."""
    patient_ids = load_insurance_data_from_mapat(config, crosswalk)
    if not patient_ids:
        raise ValueError("Failed to load historical Patient ID to Insurance ID mappings from MAPAT.")

    payer_ids = load_historical_payer_to_patient_mappings(config)
    if not payer_ids:
        raise ValueError("Failed to load historical Carol's CSVs.")

    return patient_ids, payer_ids

def map_payer_ids_to_insurance_ids(patient_id_to_insurance_id, payer_id_to_patient_ids):
    """Map Payer IDs to Insurance IDs based on historical data."""
    payer_id_to_details = {}
    for payer_id, patient_ids in payer_id_to_patient_ids.items():
        medisoft_ids = {patient_id_to_insurance_id[pid] for pid in patient_ids if pid in patient_id_to_insurance_id}
        for pid in patient_ids:
            if pid in patient_id_to_insurance_id:
                MediLink_ConfigLoader.log(
                    "Added Medisoft ID {} for Patient ID {} and Payer ID {}".format(
                        patient_id_to_insurance_id[pid], pid, payer_id
                    )
                )
            else:
                MediLink_ConfigLoader.log("No matching Insurance ID found for Patient ID {}".format(pid))
        if medisoft_ids:
            payer_id_to_details[payer_id] = {
                "endpoint": "OPTUMEDI",  # TODO Refine via API poll. Multiple defaults exist.
                "medisoft_id": list(medisoft_ids),
                "medisoft_medicare_id": []  # Placeholder for future implementation
            }
    return payer_id_to_details

def load_insurance_data_from_mains(config):
    """
    Loads insurance data from MAINS and creates a mapping from insurance names to their respective IDs.
    This mapping is critical for the crosswalk update process to correctly associate payer IDs with insurance IDs.

    Args:
        config (dict): Configuration object containing necessary paths and parameters.

    Returns:
        dict: A dictionary mapping insurance names to insurance IDs.
    """
    # Reset config pull to make sure its not using the MediLink config key subset
    config, crosswalk = MediLink_ConfigLoader.load_configuration()
    
    # Retrieve MAINS path and slicing information from the configuration   
    # TODO (Low) For secondary insurance, this needs to be pulling from the correct MAINS (there are 2)
    # TODO (Low) Performance: There probably needs to be a dictionary proxy for MAINS that gets updated.
    # Meh, this just has to be part of the new architecture plan where we make Medisoft a downstream 
    # recipient from the db.
    mains_path = config['MAINS_MED_PATH']
    mains_slices = crosswalk['mains_mapping']['slices']
    
    # Initialize the dictionary to hold the insurance to insurance ID mappings
    insurance_to_id = {}
    
    # Read data from MAINS using a provided function to handle fixed-width data
    for record, line_number in MediLink_DataMgmt.read_fixed_width_data(mains_path, mains_slices):
        insurance_name = record['MAINSNAME']
        # Assuming line_number gives the correct insurance ID without needing adjustment
        insurance_to_id[insurance_name] = line_number
    
    return insurance_to_id

def load_insurance_data_from_mapat(config, crosswalk):
    """Load insurance data from MAPAT and map Patient IDs to Insurance IDs."""
    mapat_path = app_control.get_mapat_med_path()
    mapat_slices = crosswalk['mapat_mapping']['slices']
    patient_id_to_insurance_id = {}

    for record, _ in MediLink_DataMgmt.read_fixed_width_data(mapat_path, mapat_slices):
        patient_id = record['MAPATPXID']
        insurance_id = record['MAPATINID']
        patient_id_to_insurance_id[patient_id] = insurance_id

    return patient_id_to_insurance_id

def parse_z_dat(z_dat_path, config):
    """Parse the Z.dat file to map Patient IDs to Insurance Names."""
    patient_id_to_insurance_name = {}
    try:
        for personal_info, insurance_info, service_info, service_info_2, service_info_3 in MediLink_DataMgmt.read_fixed_width_data(z_dat_path):
            parsed_data = MediLink_DataMgmt.parse_fixed_width_data(
                personal_info, insurance_info, service_info, service_info_2, service_info_3, 
                config.get('MediLink_Config', config)
            )
            patient_id = parsed_data.get('PATID')
            insurance_name = parsed_data.get('INAME')
            if patient_id and insurance_name:
                patient_id_to_insurance_name[patient_id] = insurance_name
                MediLink_ConfigLoader.log(
                    "Mapped Patient ID {} to Insurance Name {}".format(patient_id, insurance_name), 
                    config, 
                    level="INFO"
                )
    except FileNotFoundError:
        MediLink_ConfigLoader.log("File not found: {}".format(z_dat_path), config, level="INFO")
    except Exception as e:
        MediLink_ConfigLoader.log("Failed to parse Z.dat: {}".format(str(e)), config, level="INFO")

    return patient_id_to_insurance_name

def load_historical_payer_to_patient_mappings(config):
    """Load historical mappings from Carol's CSV files, mapping Payer IDs to Patient IDs."""
    directory_path = os.path.dirname(config['CSV_FILE_PATH'])
    payer_to_patient_ids = defaultdict(set)

    try:
        if not os.path.isdir(directory_path):
            raise FileNotFoundError("Directory '{}' not found.".format(directory_path))

        for filename in os.listdir(directory_path):
            if filename.endswith('.csv'):
                file_path = os.path.join(directory_path, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as csvfile:
                        reader = csv.DictReader(csvfile)
                        patient_count = 0
                        for row in reader:
                            pid = row.get('Patient ID', '').strip()
                            payer_id = row.get('Ins1 Payer ID', '').strip()
                            if pid and payer_id:
                                payer_to_patient_ids[payer_id].add(pid)
                                patient_count += 1
                        if patient_count:
                            MediLink_ConfigLoader.log(
                                "CSV file '{}' has {} Patient IDs with Payer IDs.".format(filename, patient_count)
                            )
                        else:
                            MediLink_ConfigLoader.log(
                                "CSV file '{}' is empty or does not have valid Patient ID or Payer ID mappings.".format(filename)
                            )
                except Exception as e:
                    print("Error processing file {}: {}".format(filename, e))
    except FileNotFoundError as e:
        print("Error: {}".format(e))

    if not payer_to_patient_ids:
        print("No historical mappings were generated.")

    return dict(payer_to_patient_ids)