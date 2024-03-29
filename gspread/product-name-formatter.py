from collections import Counter, defaultdict  # <-- Added defaultdict
from config import config, products_spreadsheetid
from datetime import datetime
import unicodedata
import gspread


current_datetime = datetime.now()
formatted_time = current_datetime.strftime("%Y-%m-%d | %H:%M:%S")
print(f'START: {formatted_time}')

gc = gspread.service_account_from_dict(config)
spreadsheet = gc.open_by_key(products_spreadsheetid)
worksheet = spreadsheet.worksheet("MVP")

# Find column indices by label
col_labels = worksheet.row_values(1)
try:
    name_col_index = col_labels.index("product-name") + 1
    master_id_col_index = col_labels.index("product-master-id") + 1  
    quantity_col_index = col_labels.index("quantity") + 1  # <-- Added
    unit_col_index = col_labels.index("product-unit") + 1  # <-- Added
except ValueError as e:
    print(f"Column not found: {e}")
    exit(1)

# Get column values
product_names = worksheet.col_values(name_col_index)[1:]
product_master_ids = worksheet.col_values(master_id_col_index)[1:]  # <-- Added this line
quantities = worksheet.col_values(quantity_col_index)[1:]  # <-- Added
units = worksheet.col_values(unit_col_index)[1:]  # <-- Added

# ... (initial part of the code remains the same)

# Format product names first, considering quantity and unit
temp_formatted_names = []
for name, qty, unit in zip(product_names, quantities, units):
    name = unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode('ASCII')
    formatted_name = name.lower().strip()

    if qty is not None and qty.strip() != "" and float(qty) != 0.0:
        formatted_name = f"{formatted_name} {qty}{unit}"
    
    temp_formatted_names.append(formatted_name)

# Find or create the "temp_formatted_names" column in the MVP sheet
try:
    temp_formatted_col_index = col_labels.index("temp_formatted_names") + 1
except ValueError:
    worksheet.append_row(["temp_formatted_names"])
    temp_formatted_col_index = worksheet.row_values(1).index("temp_formatted_names") + 1

# Update the "temp_formatted_names" column in batch
worksheet.update(f"{chr(64 + temp_formatted_col_index)}2:{chr(64 + temp_formatted_col_index)}{len(temp_formatted_names) + 1}", [[x] for x in temp_formatted_names])

# Group by master_id, but now use temp_formatted_names for grouping
formatted_names_by_master_id = defaultdict(list)  # <-- This line remains the same
for master_id, formatted_name in zip(product_master_ids, temp_formatted_names):  # <-- **Changed**
    formatted_names_by_master_id[master_id].append(formatted_name)

# Choose one unique formatted name for each master ID
for master_id, names in formatted_names_by_master_id.items():
    most_common_name, _ = Counter(names).most_common(1)[0]
    formatted_names_by_master_id[master_id] = most_common_name

# Prepare the list of formatted names in the order of the original sheet
new_formatted_names = [formatted_names_by_master_id[id] for id in product_master_ids]

# Count occurrences of each unique formatted product name
formatted_product_name_count = Counter(new_formatted_names)  # <-- Modified this line

# Update the "formatted_product_names" column in batch
formatted_col_index = col_labels.index("formatted_product_names") + 1
worksheet.update(f"{chr(64 + formatted_col_index)}2:{chr(64 + formatted_col_index)}{len(new_formatted_names) + 1}", [[x] for x in new_formatted_names])  # <-- Modified this line

# Fetch the already existing "formatted-product-names-count" worksheet
try:
    new_worksheet = spreadsheet.worksheet("formatted-product-names-count")
except gspread.exceptions.WorksheetNotFound:  # <-- Fixed exception name
    print("Worksheet 'formatted-product-names-count' not found")
    exit(1)

# Clear existing data in the worksheet
new_worksheet.clear()

# Add headers
new_worksheet.append_row(["formatted-product-name", "count"])

# Create a batch update to insert the unique formatted product names and their counts
batch_data = [[name, count] for name, count in formatted_product_name_count.items()]
new_worksheet.append_rows(batch_data)

current_datetime = datetime.now()
formatted_time = current_datetime.strftime("%Y-%m-%d | %H:%M:%S")
print(f'Script ended at: {formatted_time}')
