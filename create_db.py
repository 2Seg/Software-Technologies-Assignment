import sqlite3, openpyxl

def escape_quote(string):
    """Escape the quotes from a string"""
    return str(string).replace('"', ' ').replace("'", " ")

# Create and read the database OR read the database
co = sqlite3.connect("db.sqlite")
cu = co.cursor()

# 'inspections' table query
create_inspections_table_q = """
CREATE TABLE IF NOT EXISTS inspections (
    activity_date NUMERIC,
    employee_id TEXT,
    facility_address TEXT,
    facility_city TEXT,
    facility_id TEXT,
    facility_name TEXT,
    facility_state TEXT,
    facility_zip TEXT,
    grade TEXT,
    owner_id TEXT,
    owner_name TEXT,
    pe_description TEXT,
    program_element_pe INT,
    program_name TEXT,
    program_status TEXT,
    record_id TEXT,
    score TEXT,
    serial_number TEXT,
    service_code INT,
    service_description TEXT
)
"""

# 'violations' table query
create_violations_table_q = """
CREATE TABLE IF NOT EXISTS violations (
    points INT,
    serial_number TEXT,
    violation_code TEXT,
    violation_description TEXT,
    violation_status TEXT
)
"""

# Execute the queries to create the tables
cu.execute(create_inspections_table_q)
cu.execute(create_violations_table_q)

# Check if "inspections" table is empty or not
count_lines_inspections_q = "SELECT * FROM inspections"
inspections_data = cu.execute(count_lines_inspections_q).fetchall()

if inspections_data == []:
    # Load workbook with openpyxl
    inspections_wb = openpyxl.load_workbook('inspections.xlsx')
    inspections_ws = inspections_wb['inspections']

    # Build the query
    insert_into_inspections_table_q = """INSERT INTO inspections VALUES """
    for r in inspections_ws.iter_rows(min_row=2, max_row=191372): # max row = 191372
        insert_into_inspections_table_q += """("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", {}, "{}", "{}", "{}", "{}", "{}", {}, "{}"), """.format(
            escape_quote(r[0].value), r[1].value,
            escape_quote(r[2].value), escape_quote(r[3].value),
            escape_quote(r[4].value), escape_quote(r[5].value),
            escape_quote(r[6].value), escape_quote(r[7].value),
            escape_quote(r[8].value), escape_quote(r[9].value),
            escape_quote(r[10].value), r[11].value,
            r[12].value, escape_quote(r[13].value),
            escape_quote(r[14].value), escape_quote(r[15].value),
            escape_quote(r[16].value), escape_quote(r[17].value),
            r[18].value, escape_quote(r[19].value),
        )
    insert_into_inspections_table_q = insert_into_inspections_table_q[:-2]

    # Execute the query
    cu.execute(insert_into_inspections_table_q)

# Check if "violations" table is empty
count_lines_violations_q = "SELECT * FROM violations"
violations_data = cu.execute(count_lines_violations_q).fetchall()

if violations_data == []:
    # Load workbook with openpyxl
    violations_wb = openpyxl.load_workbook('violations.xlsx')
    violations_ws = violations_wb['violations']

    # Build the query
    insert_into_violations_table_q = """INSERT INTO violations VALUES """
    for r in violations_ws.iter_rows(min_row=2, max_row=906015): # max row = 906015
        insert_into_violations_table_q += """({}, "{}", "{}", "{}", "{}"), """.format(
            r[0].value, escape_quote(r[1].value), escape_quote(r[2].value),
            escape_quote(r[3].value), escape_quote(r[4].value)
        )
    insert_into_violations_table_q = insert_into_violations_table_q[:-2]

    # Execute the query
    cu.execute(insert_into_violations_table_q)

co.commit()
co.close()