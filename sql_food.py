import sqlite3
from tabulate import tabulate

# Read the database
co = sqlite3.connect("db.sqlite")
cu = co.cursor()

# Distinctive businesses that have at least 1 violation ordered alphabetically query
select_distinct_businesses_q = """
SELECT i.facility_name, i.facility_address, i.facility_zip, i.facility_city
FROM inspections i JOIN violations v ON i.serial_number = v.serial_number
GROUP BY i.facility_name HAVING COUNT(DISTINCT v.serial_number) >= 1
ORDER BY i.facility_name
"""

res1 = cu.execute(select_distinct_businesses_q).fetchall()

# Print the result of the query to the console
res1_list = []
for r in res1:
    res1_list.append([r[0]])
print(tabulate(res1_list, headers=['Businesses with at least 1 violation']))

# 'previous_violations' table query
create_prev_violations_table_q = """
CREATE TABLE IF NOT EXISTS previous_violations (
    facility_name TEXT,
    facility_address TEXT,
    facility_zip TEXT,
    facility_city TEXT
)
"""

cu.execute(create_prev_violations_table_q)

# Check if "inspections" table is empty or not
count_lines_prev_violations_q = "SELECT * FROM previous_violations"
inspections_data = cu.execute(count_lines_prev_violations_q).fetchall()

if inspections_data == []:
    insert_into_prev_violations_table_q = """INSERT INTO previous_violations VALUES """
    for r in res1:
        insert_into_prev_violations_table_q += """("{}", "{}", "{}", "{}"), """.format(
            r[0], r[1],
            r[2], r[3]
        )
    insert_into_prev_violations_table_q = insert_into_prev_violations_table_q[:-2]

    # Execute the query
    cu.execute(insert_into_prev_violations_table_q)
    co.commit()

# Count of the violations for each business that has at least one violation query
count_violations_q = """
SELECT i.facility_name, COUNT(DISTINCT v.serial_number) count_serial_numbers
FROM inspections i JOIN violations v ON i.serial_number = v.serial_number
GROUP BY i.facility_name HAVING count_serial_numbers >= 1
ORDER BY count_serial_numbers DESC 
"""

res2 = cu.execute(count_violations_q).fetchall()

# Print the result of the query to the console
for r in res2:
    print(r[0], r[1])

res2_list = []
for r in res2:
    res2_list.append([r[0], r[1]])
print(tabulate(res2_list, headers=['Businesses name', 'Number of violation']))

co.close()