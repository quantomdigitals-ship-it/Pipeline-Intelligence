import csv
import os
from difflib import SequenceMatcher
from column_mappings import COLUMN_MAPPINGS, REQUIRED_FIELDS, OPTIONAL_FIELDS

def similarity(a, b):
    """Calculate string similarity ratio (0-1)."""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def detect_crm_type(headers):
    """Detect which CRM format the CSV is from."""
    headers_lower = [h.lower() for h in headers]

    crm_scores = {
        'hubspot': 0,
        'salesforce': 0,
        'pipedrive': 0,
    }

    # Check for distinctive CRM columns
    for header in headers_lower:
        if any(x in header for x in ['hs_', 'hubspot', 'dealstage']):
            crm_scores['hubspot'] += 2
        if any(x in header for x in ['salesforce', 'stagename', 'accountname']):
            crm_scores['salesforce'] += 2
        if any(x in header for x in ['pipedrive', 'org_id', 'add_time']):
            crm_scores['pipedrive'] += 2

    if max(crm_scores.values()) > 0:
        detected_crm = max(crm_scores, key=crm_scores.get)
        return detected_crm

    return 'generic'

def find_best_match(header, field_name, crm_type):
    """Find best matching column header for a field."""
    headers_lower = [h.lower() for h in header]

    # Get expected names for this field in the detected CRM
    expected_names = COLUMN_MAPPINGS.get(crm_type, {}).get(field_name, [])

    best_match = None
    best_score = 0

    for expected in expected_names:
        for actual in headers_lower:
            score = similarity(expected, actual)
            if score > best_score:
                best_score = score
                best_match = actual

    # Fallback to generic if no match found in specific CRM
    if best_score < 0.6 and crm_type != 'generic':
        generic_names = COLUMN_MAPPINGS['generic'].get(field_name, [])
        for expected in generic_names:
            for actual in headers_lower:
                score = similarity(expected, actual)
                if score > best_score:
                    best_score = score
                    best_match = actual

    return best_match if best_score > 0.5 else None

def auto_map_columns(headers):
    """
    Automatically map CSV columns to our standard fields.

    Returns:
        dict: {standard_field: csv_column_index}
    """
    crm_type = detect_crm_type(headers)
    print(f"Detected CRM type: {crm_type}")

    mapping = {}
    all_fields = REQUIRED_FIELDS + OPTIONAL_FIELDS

    for field in all_fields:
        best_match = find_best_match(headers, field, crm_type)
        if best_match:
            # Find the index of this header
            header_index = next(
                i for i, h in enumerate(headers)
                if h.lower() == best_match
            )
            mapping[field] = header_index
            is_required = field in REQUIRED_FIELDS
            status = "✓" if is_required else "○"
            print(f"{status} {field}: {headers[header_index]}")
        else:
            status = "✗" if field in REQUIRED_FIELDS else "○"
            print(f"{status} {field}: NOT FOUND")

    return mapping

def validate_mapping(mapping):
    """Check if all required fields are mapped."""
    missing = []
    for field in REQUIRED_FIELDS:
        if field not in mapping:
            missing.append(field)

    if missing:
        print(f"\n❌ Missing required fields: {', '.join(missing)}")
        return False

    print(f"\n✅ All required fields mapped!")
    return True

def parse_csv(csv_path, mapping=None):
    """
    Parse CSV file and return normalized data.

    Args:
        csv_path: Path to CSV file
        mapping: Dict of {field: column_index}. If None, auto-detects.

    Returns:
        List of dicts with normalized column names
    """
    if not os.path.exists(csv_path):
        print(f"❌ File not found: {csv_path}")
        return None

    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames

        print(f"\n📖 Found {len(headers)} columns:")
        for i, h in enumerate(headers):
            print(f"  {i}: {h}")

        # Auto-detect mapping if not provided
        if not mapping:
            print("\n🔍 Auto-detecting columns...")
            mapping = auto_map_columns(headers)

        # Validate
        if not validate_mapping(mapping):
            return None

        # Parse rows with mapping
        normalized_rows = []
        for row_num, row in enumerate(reader, 1):
            normalized_row = {}

            for field, col_index in mapping.items():
                # Get the header name for this column
                header_name = headers[col_index]
                value = row.get(header_name, '')
                normalized_row[field] = value.strip() if value else ''

            normalized_rows.append(normalized_row)

        print(f"\n✅ Parsed {len(normalized_rows)} deals")
        return normalized_rows

def export_normalized_csv(normalized_rows, output_path='normalized_pipeline.csv'):
    """Export normalized data back to CSV."""
    if not normalized_rows:
        print("No data to export")
        return

    fieldnames = list(normalized_rows[0].keys())

    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(normalized_rows)

    print(f"✅ Exported to {output_path}")

if __name__ == '__main__':
    # Example usage
    print("CSV Parser - Column Auto-Detection\n")
    print("=" * 60)

    # Parse the sample file
    normalized = parse_csv('sample-pipeline-raw.csv')

    if normalized:
        print("\n" + "=" * 60)
        print("Sample normalized data:")
        for deal in normalized[:2]:
            print(f"\n  {deal['opportunity_name']} ({deal['company_name']})")
            print(f"    Amount: {deal['deal_value']}")
            print(f"    Stage: {deal['pipeline_stage']}")

        # Export for verification
        export_normalized_csv(normalized, 'normalized_pipeline.csv')
