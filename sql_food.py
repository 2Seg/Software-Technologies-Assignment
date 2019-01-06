import sqlite3
from tabulate import tabulate

# Read the database
co = sqlite3.connect("db.sqlite")
cu = co.cursor()

# Distinctive businesses that have at least 1 violation ordered alphabetically query
select_distinct_businesses_q = """
select i.facility_name, i.facility_address, i.facility_zip, i.facility_city
from inspections i join violations v on i.serial_number = v.serial_number
group by i.facility_name having count(distinct v.serial_number) >= 1
order by i.facility_name
"""

res1 = cu.execute(select_distinct_businesses_q).fetchall()

# Print the result of the query to the console
res1_list = []
for r in res1:
    res1_list.append([r[0]])
print(tabulate(res1_list, headers=['Businesses with at least 1 violation']))

# 'previous_violations' table query
create_prev_violations_table_q = """
create table if not exists previous_violations (
    facility_name text,
    facility_address text,
    facility_zip text,
    facility_city text
)
"""

cu.execute(create_prev_violations_table_q)

# Check if "inspections" table is empty or not
count_lines_prev_violations_q = "select * from previous_violations"
inspections_data = cu.execute(count_lines_prev_violations_q).fetchall()

if inspections_data == []:
    insert_into_prev_violations_table_q = """insert into previous_violations (facility_name, facility_address, facility_zip, facility_city) values """
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
select i.facility_name, count(distinct v.serial_number) count_serial_numbers
from inspections i join violations v on i.serial_number = v.serial_number
group by i.facility_name having count_serial_numbers >= 1
order by count_serial_numbers desc
"""

res2 = cu.execute(count_violations_q).fetchall()

# Print the result of the query to the console
for r in res2:
    print(r[0], r[1])

res2_list = []
for r in res2:
    res2_list.append([r[0], r[1]])
print(tabulate(res2_list, headers=['Businesses name', 'Number of violation']))