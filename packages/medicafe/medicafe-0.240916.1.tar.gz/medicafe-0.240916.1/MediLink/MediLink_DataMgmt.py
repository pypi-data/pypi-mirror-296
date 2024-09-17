# MediLink_DataMgmt.py
import csv, os, re, subprocess
from datetime import datetime, timedelta

# Import necessary modules, handle relative imports if needed
try:
    import MediLink_ConfigLoader, MediLink_UI
except ImportError:
    from . import MediLink_ConfigLoader, MediLink_UI

def slice_data(data, slices, suffix=''):
    """Slice and strip data based on slice definitions."""
    return {key + suffix: data[slice(*slices[key])].strip() for key in slices}

def parse_fixed_width_data(personal_info, insurance_info, service_info, service_info_2=None, service_info_3=None, config=None):
    """Parse fixed-width segments to extract claim data."""
    config = load_and_validate_config(config)
    personal_slices = config['fixedWidthSlices']['personal_slices']
    insurance_slices = config['fixedWidthSlices']['insurance_slices']
    service_slices = config['fixedWidthSlices']['service_slices']
    parsed = {}
    parsed.update(slice_data(personal_info, personal_slices))
    parsed.update(slice_data(insurance_info, insurance_slices))
    parsed.update(slice_data(service_info, service_slices))
    if service_info_2:
        parsed.update(slice_data(service_info_2, service_slices, suffix='_2'))
    if service_info_3:
        parsed.update(slice_data(service_info_3, service_slices, suffix='_3'))
    MediLink_ConfigLoader.log("Successfully parsed data from segments", config, level="INFO")
    return parsed

class MediLinkConfigError(Exception):
    """Custom exception for MediLink configuration errors."""
    pass

def load_and_validate_config(config=None, retry_attempts=3):
    """Load and validate MediLink configuration."""
    attempts = 0
    while attempts < retry_attempts:
        if not config:
            MediLink_ConfigLoader.log("No config passed. Attempting to load configuration...", level="WARNING")
            config, _ = MediLink_ConfigLoader.load_configuration()
        
        if not config:
            MediLink_ConfigLoader.log("Configuration load attempt {} failed.".format(attempts + 1), level="ERROR")
            attempts += 1
            continue

        if 'MediLink_Config' not in config:
            MediLink_ConfigLoader.log("Config missing 'MediLink_Config'. Reloading configuration...", level="WARNING")
            config, _ = MediLink_ConfigLoader.load_configuration()
            attempts += 1
            continue

        try:
            validate_config(config['MediLink_Config'])
            return config['MediLink_Config']
        except (RuntimeError, ValueError) as e:
            MediLink_ConfigLoader.log(str(e), level="ERROR")
            attempts += 1
            config = None  # Reset config to attempt reloading

    MediLink_ConfigLoader.log("Exceeded maximum configuration load attempts.", level="CRITICAL")
    raise MediLinkConfigError("Failed to load a valid MediLink configuration after {} attempts.".format(retry_attempts))

def validate_config(medi_link_config):
    """Ensure essential configuration keys are present in MediLink_Config."""
    required_keys = ['endpoints', 'local_storage_path']
    missing_keys = [key for key in required_keys if key not in medi_link_config]
    
    if missing_keys:
        error_message = "Config missing required key(s): {}".format(", ".join(missing_keys))
        MediLink_ConfigLoader.log(error_message, level="ERROR")
        raise ValueError(error_message)
    
    # Additional validation logic can be added here
    MediLink_ConfigLoader.log("Configuration validated successfully.", level="INFO")

def read_fixed_width_data(file_path, slices=None):
    """Read fixed-width data; handle with or without slice definitions."""
    MediLink_ConfigLoader.log("Starting to read fixed width data from {}".format(file_path))
    if slices:
        with open(file_path, 'r', encoding='utf-8') as file:
            next(file)  # Skip header
            for line_num, line in enumerate(file, 1):
                stripped = line.strip()
                if stripped:
                    record = {k: stripped[slice(*v)].strip() for k, v in slices.items()}
                    MediLink_ConfigLoader.log("Parsed record at line {}: {}".format(line_num, record), level="DEBUG")
                    yield record, line_num
    else:
        with open(file_path, 'r') as file:
            buffer = []
            for line in file:
                stripped = line.strip()
                if stripped:
                    buffer.append(stripped)
                    if 3 <= len(buffer) <= 5:
                        try:
                            next_line = file.readline().strip()
                            if not next_line:
                                yield yield_record(buffer)
                                buffer = []
                        except StopIteration:
                            yield yield_record(buffer)
                            buffer = []
                else:
                    if len(buffer) >= 3:
                        yield yield_record(buffer)
                        buffer = []
            if buffer:
                yield yield_record(buffer)

def yield_record(buffer):
    """Yield parsed segments from buffer."""
    personal, insurance, service = buffer[:3]
    svc2 = buffer[3] if len(buffer) > 3 else None
    svc3 = buffer[4] if len(buffer) > 4 else None
    MediLink_ConfigLoader.log("Successfully read data from buffer.", level="INFO")
    return personal, insurance, service, svc2, svc3

def consolidate_csvs(source_directory, file_prefix="Consolidated", interactive=False):
    """Consolidate CSVs in source_dir into one file with prefix and date."""
    today = datetime.now().strftime("%m%d%y")
    target = os.path.join(source_directory, "{}_{}.csv".format(file_prefix, today))
    if os.path.exists(target):
        MediLink_ConfigLoader.log("The file {} already exists. It will be overwritten.".format(target), level="INFO")
        if interactive:
            overwrite = input("The file {} already exists. Do you want to overwrite it? (y/n): ".format(target)).strip().lower()
            if overwrite != 'y':
                MediLink_ConfigLoader.log("User opted not to overwrite the file {}.".format(target), level="INFO")
                return None
    data, header = collect_csv_data(source_directory, target)
    if data:
        write_consolidated_csv(target, data)
        MediLink_ConfigLoader.log("Consolidated CSVs into {}".format(target), level="INFO")
        return target
    MediLink_ConfigLoader.log("No valid CSV files were found for consolidation.", level="INFO")
    return None

def collect_csv_data(source_dir, target):
    """Gather CSV data from source_dir, ensuring headers match."""
    data, header_saved, expected = [], False, None
    for fname in os.listdir(source_dir):
        path = os.path.join(source_dir, fname)
        if should_skip(path, target) or not file_modified_within(path):
            continue
        try:
            with open(path, 'r') as f:
                reader = csv.reader(f)
                header = next(reader)
                if not header_saved:
                    expected, header_saved = header, True
                    data.append(header)
                elif header != expected:
                    MediLink_ConfigLoader.log("Header mismatch in {}. Skipping.".format(path), level="WARNING")
                    continue
                data.extend(row for row in reader)
        except StopIteration:
            MediLink_ConfigLoader.log("File {} is empty or has only header. Skipping.".format(path), level="WARNING")
            continue
        except Exception as e:
            MediLink_ConfigLoader.log("Error processing {}: {}".format(path, e), level="ERROR")
            continue
        try:
            os.remove(path)
            MediLink_ConfigLoader.log("Deleted source file after consolidation: {}".format(path), level="INFO")
        except Exception as e:
            MediLink_ConfigLoader.log("Failed to delete {}: {}".format(path, e), level="ERROR")
    return data, expected

def should_skip(path, target):
    """Determine if a file should be skipped during consolidation."""
    return not path.endswith('.csv') or os.path.isdir(path) or path == target

def file_modified_within(path, days=1):
    """Check if file was modified within the last 'days' days."""
    return datetime.fromtimestamp(os.path.getmtime(path)) >= datetime.now() - timedelta(days=days)

def write_consolidated_csv(path, data):
    """Write consolidated data to a CSV file."""
    try:
        with open(path, 'w', newline='') as f:
            csv.writer(f).writerows(data)
    except Exception as e:
        MediLink_ConfigLoader.log("Failed to write consolidated CSV {}: {}".format(path, e), level="ERROR")

def operate_winscp(operation_type, files, endpoint_config, local_storage_path, config):
    """Operate WinSCP for upload/download based on operation type."""
    MediLink_ConfigLoader.log("Starting operate_winscp with operation_type: {}".format(operation_type))
    config = ensure_config_loaded(config)
    winscp_path = get_winscp_path(config)
    if not os.path.isfile(winscp_path):
        MediLink_ConfigLoader.log("WinSCP.com not found at {}".format(winscp_path), level="ERROR")
        return []
    validate_endpoint_config(endpoint_config)
    winscp_log_path = setup_logging(operation_type, local_storage_path)
    local_storage_path = validate_local_storage_path(local_storage_path, config)
    remote_directory = get_remote_directory(endpoint_config, operation_type)
    command = build_command(winscp_path, winscp_log_path, endpoint_config, remote_directory, operation_type, files, local_storage_path)
    if config.get("TestMode", True):
        MediLink_ConfigLoader.log("Test mode is enabled. Simulating operation.", level="INFO")
        return simulate_operation(operation_type, files, config)
    result = execute_winscp_command(command, operation_type, files, local_storage_path)
    MediLink_ConfigLoader.log("[Execute WinSCP Command] Result: {}".format(result), level="DEBUG")
    return result

def validate_local_storage_path(local_storage_path, config):
    """Validate and possibly replace local storage path."""
    if ' ' in local_storage_path:
        MediLink_ConfigLoader.log("Local storage path contains spaces, using outputFilePath from config.", level="WARN")
        output_file_path = config.get('outputFilePath', None)
        if not output_file_path:
            raise ValueError("outputFilePath not found in config.")
        return os.path.normpath(output_file_path)
    return os.path.normpath(local_storage_path)

def ensure_config_loaded(config):
    """Ensure configuration is loaded and valid."""
    MediLink_ConfigLoader.log("Ensuring configuration is loaded.")
    if not config:
        MediLink_ConfigLoader.log("Warning: No config passed to ensure_config_loaded. Re-loading config...", level="WARNING")
        config, _ = MediLink_ConfigLoader.load_configuration()
    if not config or 'MediLink_Config' not in config:
        MediLink_ConfigLoader.log("Failed to load the MediLink configuration. Config is None or missing 'MediLink_Config'.", level="ERROR")
        raise RuntimeError("Failed to load the MediLink configuration. Config is None or missing 'MediLink_Config'.")
    if 'endpoints' not in config['MediLink_Config'] or 'local_storage_path' not in config['MediLink_Config']:
        MediLink_ConfigLoader.log("The loaded configuration is missing required sections.", level="ERROR")
        raise ValueError("The loaded configuration is missing required sections.")
    MediLink_ConfigLoader.log("Configuration loaded successfully.", level="INFO")
    return config['MediLink_Config']

def get_winscp_path(config):
    """Retrieve WinSCP path from config or default locations."""
    MediLink_ConfigLoader.log("Retrieving WinSCP path from config.")
    winscp_path = config.get('winscp_path')
    if winscp_path and os.path.isfile(winscp_path):
        MediLink_ConfigLoader.log("WinSCP path found in config: {}".format(winscp_path), level="INFO")
        return winscp_path
    MediLink_ConfigLoader.log("WinSCP path not found in config. Searching default paths.", level="WARN")
    default_paths = [
        os.path.join(os.getcwd(), "Installers", "WinSCP-Portable", "WinSCP.com"),
        os.path.join(os.getcwd(), "Necessary Programs", "WinSCP-Portable", "WinSCP.com")
    ]
    for path in default_paths:
        if os.path.exists(path):
            MediLink_ConfigLoader.log("WinSCP found at {}. Using this path.".format(path), level="INFO")
            return path
    MediLink_ConfigLoader.log("WinSCP not found in config or default paths. Reloading configuration.", level="ERROR")
    try:
        config, _ = MediLink_ConfigLoader.load_configuration()
        winscp_path = config.get('winscp_path')
        if winscp_path and os.path.isfile(winscp_path):
            MediLink_ConfigLoader.log("WinSCP path found after reloading config: {}".format(winscp_path), level="INFO")
            return winscp_path
    except Exception as e:
        MediLink_ConfigLoader.log("Failed to reload configuration: {}".format(e), level="ERROR")
    raise FileNotFoundError("WinSCP path not found in config or default locations.")

def validate_endpoint_config(endpoint_config):
    """Ensure endpoint configuration is a dictionary."""
    MediLink_ConfigLoader.log("Validating endpoint configuration.")
    if not isinstance(endpoint_config, dict):
        MediLink_ConfigLoader.log("Endpoint configuration is not a dictionary.", level="ERROR")
        raise ValueError("Endpoint configuration must be a dictionary.")

def setup_logging(operation_type, local_storage_path):
    """Set up logging for WinSCP operations."""
    log_filename = "winscp_upload.log" if operation_type == "upload" else "winscp_download.log"
    log_path = os.path.join(local_storage_path, log_filename)
    MediLink_ConfigLoader.log("Logging WinSCP operation to {}".format(log_path), level="INFO")
    return log_path

def get_remote_directory(endpoint_config, operation_type):
    """Retrieve remote directory based on operation type."""
    MediLink_ConfigLoader.log("Getting remote directory for operation type: {}".format(operation_type))
    if operation_type == "upload":
        return endpoint_config['remote_directory_up']
    elif operation_type == "download":
        return endpoint_config['remote_directory_down']
    else:
        MediLink_ConfigLoader.log("Invalid operation type: {}. Expected 'upload' or 'download'.".format(operation_type), level="ERROR")
        raise ValueError("Invalid operation type: {}. Expected 'upload' or 'download'.".format(operation_type))

def build_command(winscp_path, winscp_log_path, endpoint_config, remote_directory, operation_type, files, local_storage_path):
    """Construct the WinSCP command list."""
    MediLink_ConfigLoader.log("Building WinSCP command for operation type: {}".format(operation_type))
    session_name = endpoint_config.get('session_name', '')
    command = [
        winscp_path,
        '/log=' + winscp_log_path,
        '/loglevel=1',
        '/command',
        'open {}'.format(session_name),
        'cd /',
        'cd {}'.format(remote_directory)
    ]
    if operation_type == "upload":
        if not files:
            MediLink_ConfigLoader.log("No files provided for upload operation.", level="ERROR")
            raise ValueError("No files provided for upload operation.")
        command += ['put "{}"'.format(os.path.normpath(f)) for f in files]
    elif operation_type == "download":
        command += ['lcd "{}"'.format(os.path.normpath(local_storage_path)), 'get *']
    command += ['close', 'exit']
    MediLink_ConfigLoader.log("[Build Command] WinSCP command: {}".format(command))
    return command

def simulate_operation(operation_type, files, config):
    """Simulate WinSCP operations in test mode."""
    MediLink_ConfigLoader.log("Simulating {} operation.".format(operation_type), level="INFO")
    if operation_type == 'upload':
        simulated = [os.path.normpath(f) for f in files if os.path.exists(f)]
        MediLink_ConfigLoader.log("Simulated uploaded files: {}".format(simulated), level="DEBUG")
        return simulated
    elif operation_type == 'download':
        MediLink_ConfigLoader.log("Simulated download operation. No files downloaded in test mode.", level="INFO")
        return []
    MediLink_ConfigLoader.log("Invalid operation type for simulation: {}".format(operation_type), level="ERROR")
    return []

def execute_winscp_command(command, operation_type, files, local_storage_path):
    """Execute the WinSCP command and handle results."""
    MediLink_ConfigLoader.log("Executing WinSCP command for operation type: {}".format(operation_type), level="INFO")
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
        stdout, stderr = process.communicate()
    except Exception as e:
        MediLink_ConfigLoader.log("Execution error: {}".format(e), level="ERROR")
        return []
    if process.returncode == 0:
        MediLink_ConfigLoader.log("WinSCP {} operation completed successfully.".format(operation_type), level="INFO")
        if operation_type == 'download':
            return list_downloaded_files(local_storage_path)
        elif operation_type == 'upload':
            uploaded_files = [os.path.normpath(f) for f in files if os.path.exists(f)]
            MediLink_ConfigLoader.log("Uploaded files: {}".format(uploaded_files), level="DEBUG")
            return uploaded_files
    error = stderr.decode('utf-8').strip()
    MediLink_ConfigLoader.log("WinSCP {} failed. Exit code: {}. Details: {}".format(operation_type, process.returncode, error), level="ERROR")
    return []

def list_downloaded_files(local_storage_path):
    """List all files in the local storage path."""
    MediLink_ConfigLoader.log("Listing downloaded files in {}".format(local_storage_path), level="INFO")
    files_found = []
    try:
        for root, _, files in os.walk(local_storage_path):
            for f in files:
                path = os.path.join(root, f)
                files_found.append(path)
                MediLink_ConfigLoader.log("Found downloaded file: {}".format(path), level="DEBUG")
        if not files_found:
            MediLink_ConfigLoader.log("No files found in {}".format(local_storage_path), level="WARNING")
    except Exception as e:
        MediLink_ConfigLoader.log("Error listing files in {}: {}".format(local_storage_path, e), level="ERROR")
    return files_found

def detect_new_files(directory_path, file_extension='.DAT'):
    """Detect and optionally timestamp new files with the given extension."""
    MediLink_ConfigLoader.log("Scanning directory: {}".format(directory_path), level="INFO")
    detected, flagged = [], False
    try:
        for fname in os.listdir(directory_path):
            if not fname.endswith(file_extension):
                continue
            MediLink_ConfigLoader.log("Processing file: {}".format(fname), level="INFO")
            name, ext = os.path.splitext(fname)
            if not is_timestamped(name):
                new_name = "{}_{}{}".format(name, datetime.now().strftime('%Y%m%d_%H%M%S'), ext)
                os.rename(os.path.join(directory_path, fname), os.path.join(directory_path, new_name))
                MediLink_ConfigLoader.log("Renamed {} to {}".format(fname, new_name), level="INFO")
                fname = new_name
                flagged = True
            else:
                MediLink_ConfigLoader.log("File already timestamped: {}".format(fname), level="INFO")
            path = os.path.join(directory_path, fname)
            detected.append(path)
            MediLink_ConfigLoader.log("Detected file: {}".format(path), level="INFO")
    except Exception as e:
        MediLink_ConfigLoader.log("Error during file detection: {}".format(e), level="ERROR")
    MediLink_ConfigLoader.log("Detected files: {}".format(detected), level="INFO")
    MediLink_ConfigLoader.log("File flagged for timestamp: {}".format(flagged), level="INFO")
    return detected, flagged

def is_timestamped(name):
    """Check if filename has a timestamp in YYYYMMDD_HHMMSS format."""
    return bool(re.match(r'.*_\d{8}_\d{6}$', name))

def organize_patient_data_by_endpoint(detailed_patient_data):
    """Organize patient data by their confirmed endpoints."""
    organized = {}
    for data in detailed_patient_data:
        endpoint = data.get('confirmed_endpoint', data.get('suggested_endpoint'))
        if not endpoint:
            MediLink_ConfigLoader.log("No endpoint found for patient data: {}".format(data), level="WARNING")
            continue
        organized.setdefault(endpoint, []).append(data)
    return organized

def confirm_all_suggested_endpoints(detailed_patient_data):
    """Set 'confirmed_endpoint' to 'suggested_endpoint' or 'AVAILITY'."""
    for data in detailed_patient_data:
        data['confirmed_endpoint'] = data.get('suggested_endpoint', 'AVAILITY')
    return detailed_patient_data

def bulk_edit_insurance_types(detailed_patient_data, insurance_options):
    """Allow user to bulk edit insurance types with validation."""
    print("Edit Insurance Type (Enter the 2-character code). Enter 'LIST' to display available insurance types.")
    for data in detailed_patient_data:
        current = data.get('insurance_type', 'Unknown')
        desc = insurance_options.get(current, "Unknown")
        print("({}) {:<25} | Current Ins. Type: {} - {}".format(
            data.get('patient_id', 'N/A'),
            data.get('patient_name', 'N/A'),
            current,
            desc))
        while True:
            inp = input("Enter new insurance type (or press Enter to keep current): ").upper()
            if inp == 'LIST':
                MediLink_UI.display_insurance_options(insurance_options)
            elif not inp:
                break
            elif inp in insurance_options:
                data['insurance_type'] = inp
                break
            else:
                print("Invalid insurance type. Please enter a valid 2-character code or type 'LIST' to see options.")

def review_and_confirm_changes(detailed_patient_data, insurance_options):
    """Review and confirm insurance type changes."""
    print("\nReview changes:")
    print("{:<20} {:<10} {:<30}".format("Patient Name", "Ins. Type", "Description"))
    print("="*60)
    for data in detailed_patient_data:
        ins = data.get('insurance_type', 'Unknown')
        desc = insurance_options.get(ins, "Unknown")
        print("{:<20} {:<10} {:<30}".format(
            data.get('patient_name', 'N/A'),
            ins,
            desc))
    return input("\nConfirm changes? (y/n): ").strip().lower() in ['y', 'yes', '']