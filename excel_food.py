import openpyxl, sqlite3
from openpyxl.styles import Font

# Read the database
co = sqlite3.connect("db.sqlite")
cu = co.cursor()

# Create a new workbook
wb = openpyxl.Workbook()

# Rename the active sheet as "Violations Types"
sheet = wb.active
sheet.title = "Violations Types"

# Calculate the number of each type of violations
calculate_number_violations_q = """
SELECT violation_code, violation_description, COUNT(violation_description) count_violations FROM violations
GROUP BY violation_description ORDER BY violation_code
"""

res = cu.execute(calculate_number_violations_q).fetchall()

# Add headers and a bit of style
sheet['A1'] = "Code"
sheet['B1'] = "Description"
sheet['C1'] = "Count"

sheet['A1'].font = sheet['B1'].font = sheet['C1'].font = Font(bold=True)
sheet.column_dimensions['B'].width = 70

# Write result from the request to the worksheet
for i, r in enumerate(res):
    sheet["A" + str(i + 2)] = r[0]
    sheet["B" + str(i + 2)] = r[1].split(". ")[-1]
    sheet["C" + str(i + 2)] = r[2]

# Save "ViolationTypes.xlsx" workbook
wb.save("ViolationTypes.xlsx")

co.close()