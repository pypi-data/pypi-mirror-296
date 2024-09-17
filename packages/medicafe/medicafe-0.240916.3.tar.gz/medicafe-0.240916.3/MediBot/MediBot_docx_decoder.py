from docx import Document
import re
from lxml import etree
import zipfile
from datetime import datetime
import os
import sys
from collections import OrderedDict
import pprint

# Add parent directory of the project to the Python path
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_dir)

try:
    import MediLink_ConfigLoader
except ImportError:
    from MediLink import MediLink_ConfigLoader

# Compile regex patterns once
ICD10_PATTERN = re.compile(r'H\d{2}\.\d+')
DAY_WEEK_PATTERN = re.compile(r"(MONDAY|TUESDAY|WEDNESDAY|THURSDAY|FRIDAY|SATURDAY|SUNDAY)", re.IGNORECASE)
MONTH_DAY_PATTERN = re.compile(r"(JANUARY|FEBRUARY|MARCH|APRIL|MAY|JUNE|JULY|AUGUST|SEPTEMBER|OCTOBER|NOVEMBER|DECEMBER) \d{1,2}", re.IGNORECASE)
YEAR_PATTERN = re.compile(r"\d{4}")

def parse_docx(filepath):
    try:
        doc = Document(filepath)
    except Exception as e:
        MediLink_ConfigLoader.log("Error opening document: {}".format(e))
        return {}

    patient_data = OrderedDict()
    MediLink_ConfigLoader.log("Extracting Date of Service from {}".format(filepath), level="DEBUG")

    date_of_service = extract_date_of_service(filepath)
    MediLink_ConfigLoader.log("Date of Service recorded as: {}".format(date_of_service), level="DEBUG")

    for table in doc.tables:
        for row in table.rows:
            cells = [cell.text.strip() for cell in row.cells]
            if len(cells) > 4 and cells[3].startswith('#'):
                patient_id = parse_patient_id(cells[3])
                if not patient_id:
                    MediLink_ConfigLoader.log("Invalid patient ID in row: {}".format(cells), level="WARNING")
                    continue

                diagnosis_code = parse_diagnosis_code(cells[4])
                left_or_right_eye = parse_left_or_right_eye(cells[4])
                femto_yes_or_no = parse_femto_yes_or_no(cells[4])

                if patient_id not in patient_data:
                    patient_data[patient_id] = {}

                if date_of_service in patient_data[patient_id]:
                    MediLink_ConfigLoader.log("Duplicate entry for patient ID {} on date {}. Skipping.".format(patient_id, date_of_service))
                else:
                    patient_data[patient_id][date_of_service] = [diagnosis_code, left_or_right_eye, femto_yes_or_no]

    # Validation steps
    validate_unknown_entries(patient_data)
    validate_diagnostic_code(patient_data)

    return patient_data

def validate_unknown_entries(patient_data):
    for patient_id, dates in list(patient_data.items()):
        for date, details in list(dates.items()):
            if 'Unknown' in details:
                warning_message = "Warning: 'Unknown' entry found. Patient ID: {}, Date: {}, Details: {}".format(patient_id, date, details)
                MediLink_ConfigLoader.log(warning_message, level="WARNING")
                del patient_data[patient_id][date]
        if not patient_data[patient_id]:
            del patient_data[patient_id]

def validate_diagnostic_code(patient_data):
    for patient_id, dates in patient_data.items():
        for date, details in dates.items():
            diagnostic_code, eye, _ = details
            if diagnostic_code and diagnostic_code[-1].isdigit():
                if eye == 'Left' and not diagnostic_code.endswith('2'):
                    log_and_warn(patient_id, date, diagnostic_code, eye)
                elif eye == 'Right' and not diagnostic_code.endswith('1'):
                    log_and_warn(patient_id, date, diagnostic_code, eye)

def log_and_warn(patient_id, date, diagnostic_code, eye):
    warning_message = (
        "Warning: Mismatch found for Patient ID: {}, Date: {}, "
        "Diagnostic Code: {}, Eye: {}".format(patient_id, date, diagnostic_code, eye)
    )
    MediLink_ConfigLoader.log(warning_message, level="WARNING")

def extract_date_of_service(docx_path):
    try:
        with zipfile.ZipFile(docx_path, 'r') as docx:
            MediLink_ConfigLoader.log("Opened DOCX as zip: {}".format(docx_path), level="DEBUG")
            for file_info in docx.infolist():
                if file_info.filename.endswith('.xml'):
                    with docx.open(file_info) as file:
                        try:
                            tree = etree.parse(file)
                            root = tree.getroot()
                            namespaces = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
                            for elem in root.xpath('//w:t', namespaces=namespaces):
                                if elem.text and "Surgery Schedule" in elem.text:
                                    MediLink_ConfigLoader.log("Found target text in file: {}".format(file_info.filename), level="DEBUG")
                                    return extract_date_from_file_from_tree(tree)
                        except Exception as e:
                            MediLink_ConfigLoader.log("Error parsing XML file {}: {}".format(file_info.filename, e))
        MediLink_ConfigLoader.log("Target text 'Surgery Schedule' not found in any XML files.", level="WARNING")
        return None
    except Exception as e:
        MediLink_ConfigLoader.log("Error opening DOCX file {}: {}".format(docx_path, e), level="ERROR")
        return None

def extract_date_from_file_from_tree(tree):
    try:
        root = tree.getroot()
        collected_text = []

        namespaces = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
        for elem in root.xpath('//w:t', namespaces=namespaces):
            if elem.text:
                collected_text.append(elem.text.strip())

        combined_text = ' '.join(collected_text)
        combined_text = reassemble_year(combined_text)
        combined_text = normalize_text(combined_text)
        combined_text = re.sub(r',', '', combined_text)

        MediLink_ConfigLoader.log("Combined text: {}".format(combined_text), level="DEBUG")

        day_of_week = DAY_WEEK_PATTERN.search(combined_text)
        month_day = MONTH_DAY_PATTERN.search(combined_text)
        year_match = YEAR_PATTERN.search(combined_text)

        MediLink_ConfigLoader.log("Day of week found: {}".format(day_of_week.group() if day_of_week else 'None'), level="DEBUG")
        MediLink_ConfigLoader.log("Month and day found: {}".format(month_day.group() if month_day else 'None'), level="DEBUG")
        MediLink_ConfigLoader.log("Year found: {}".format(year_match.group() if year_match else 'None'), level="DEBUG")

        if day_of_week and month_day and year_match:
            date_str = "{} {} {}".format(day_of_week.group(), month_day.group(), year_match.group())
            try:
                date_obj = datetime.strptime(date_str, '%A %B %d %Y')
                return date_obj.strftime('%m-%d-%Y')
            except ValueError as e:
                MediLink_ConfigLoader.log("Error converting date: {}. Error: {}".format(date_str, e), level="ERROR")
        else:
            MediLink_ConfigLoader.log(
                "Date components not found or incomplete in the text. Combined text: {}, Day of week: {}, Month and day: {}, Year: {}".format(
                    combined_text,
                    day_of_week.group() if day_of_week else 'None',
                    month_day.group() if month_day else 'None',
                    year_match.group() if year_match else 'None'
                ),
                level="WARNING"
            )
    except Exception as e:
        MediLink_ConfigLoader.log("Error extracting date from tree: {}".format(e), level="ERROR")

    return None

def normalize_text(text):
    month_map = {
        'JAN': 'JANUARY', 'FEB': 'FEBRUARY', 'MAR': 'MARCH', 'APR': 'APRIL', 
        'MAY': 'MAY', 'JUN': 'JUNE', 'JUL': 'JULY', 'AUG': 'AUGUST', 
        'SEP': 'SEPTEMBER', 'OCT': 'OCTOBER', 'NOV': 'NOVEMBER', 'DEC': 'DECEMBER'
    }
    day_map = {
        'MON': 'MONDAY', 'TUE': 'TUESDAY', 'WED': 'WEDNESDAY', 'THU': 'THURSDAY', 
        'FRI': 'FRIDAY', 'SAT': 'SATURDAY', 'SUN': 'SUNDAY'
    }

    for abbr, full in month_map.items():
        text = re.sub(r'\b{}\b'.format(abbr), full, text, flags=re.IGNORECASE)
    for abbr, full in day_map.items():
        text = re.sub(r'\b{}\b'.format(abbr), full, text, flags=re.IGNORECASE)

    return text

def reassemble_year(text):
    text = re.sub(r'(\d{3})\s+(\d{1})', r'\1\2', text)
    text = re.sub(r'(\d{1})\s+(\d{3})', r'\1\2', text)
    text = re.sub(r'(\d{2})\s+(\d{2})', r'\1\2', text)

    parts = re.findall(r'\b(\d{1,2})\b', text)
    if len(parts) >= 4:
        for i in range(len(parts) - 3):
            candidate = ''.join(parts[i:i + 4])
            if len(candidate) == 4 and candidate.isdigit():
                combined_year = candidate
                pattern = r'\b{}\b'.format(r'\b \b'.join(parts[i:i + 4]))
                text = re.sub(pattern, combined_year, text)
                break
    return text

def parse_patient_id(text):
    try:
        return text.split()[0].lstrip('#')
    except Exception as e:
        MediLink_ConfigLoader.log("Error parsing patient ID: {}. Error: {}".format(text, e))
        return None

def parse_diagnosis_code(text):
    try:
        matches = ICD10_PATTERN.findall(text)
        if matches:
            return matches[0]
        else:
            if '(' in text and ')' in text:
                full_code = text[text.index('(')+1:text.index(')')]
                return full_code.split('/')[0]
            return text.split('/')[0]
    except Exception as e:
        MediLink_ConfigLoader.log("Error parsing diagnosis code: {}. Error: {}".format(text, e))
        return "Unknown"

def parse_left_or_right_eye(text):
    try:
        upper_text = text.upper()
        if 'LEFT EYE' in upper_text:
            return 'Left'
        elif 'RIGHT EYE' in upper_text:
            return 'Right'
        else:
            return 'Unknown'
    except Exception as e:
        MediLink_ConfigLoader.log("Error parsing left or right eye: {}. Error: {}".format(text, e))
        return 'Unknown'

def parse_femto_yes_or_no(text):
    try:
        return 'FEMTO' in text.upper()
    except Exception as e:
        MediLink_ConfigLoader.log("Error parsing femto yes or no: {}. Error: {}".format(text, e))
        return False

def rotate_docx_files(directory):
    files = [file for file in os.listdir(directory) if "DR" in file and "SS" in file]
    file_paths = [os.path.join(directory, file) for file in files]

    for filepath in file_paths:
        try:
            patient_data_dict = parse_docx(filepath)
            filename = os.path.basename(filepath)
            print("Data from file '{}':".format(filename))
            pprint.pprint(patient_data_dict)
            print()
        except Exception as e:
            MediLink_ConfigLoader.log("Error processing file '{}': {}".format(filepath, e), level="ERROR")

def main():
    if len(sys.argv) > 1:
        directory = sys.argv[1]
    else:
        directory = "C:\\Users\\danie\\Downloads\\"
    rotate_docx_files(directory)

if __name__ == "__main__":
    main()