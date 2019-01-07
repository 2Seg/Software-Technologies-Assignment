import sqlite3, datetime, matplotlib.pyplot as plt, re, dateutil.parser
from tabulate import tabulate

# Read the database
co = sqlite3.connect("db.sqlite")
cu = co.cursor()


## Number of violations per month for the postcode with the highest total violations
q1 = """
WITH
    postcode_highest_violations (postcode) AS (
        SELECT i.facility_zip FROM inspections i
        JOIN violations v ON i.serial_number = v.serial_number
        GROUP BY i.facility_zip ORDER BY COUNT(DISTINCT v.serial_number) DESC LIMIT 1
    ),
    violations_per_date (date, count) AS (
        SELECT i.activity_date, COUNT(DISTINCT v.serial_number) FROM inspections i
        JOIN violations v ON i.serial_number = v.serial_number
        NATURAL JOIN postcode_highest_violations
        GROUP BY i.activity_date HAVING i.facility_zip = postcode_highest_violations.postcode
    )
SELECT strftime("%Y", date) AS year, strftime("%m", date) AS month, SUM(count)
FROM violations_per_date GROUP BY month ORDER BY year
"""

res1 = cu.execute(q1).fetchall()

# Create a dictionary with the result of the query for plotting
highest_violations_month_dict = {}
for r in res1:
    highest_violations_month_dict[
        str(datetime.datetime(int(r[0]), int(r[1]), 1).strftime('%B %Y'))
    ] = r[2]

# Create and plot the result
plt.plot(
    list(highest_violations_month_dict.keys()),
    list(highest_violations_month_dict.values()),
    "b.-"
)
plt.xlabel("Months")
plt.xticks(rotation=60)
plt.ylabel("Number of violations")
plt.title("Violation per month for the postcode with the highest total violations")
plt.show()


## Number of violations per month for the postcode with the lowest total violations
q2 = """
WITH
    postcode_lowest_violations (postcode) AS (
        SELECT i.facility_zip FROM inspections i
        JOIN violations v ON i.serial_number = v.serial_number
        GROUP BY i.facility_zip ORDER BY COUNT(DISTINCT v.serial_number) LIMIT 1
    ),
    violations_per_date (date, count) AS (
        SELECT i.activity_date, COUNT(DISTINCT v.serial_number) FROM inspections i
        JOIN violations v ON i.serial_number = v.serial_number
        NATURAL JOIN postcode_lowest_violations
        WHERE i.facility_zip = postcode_lowest_violations.postcode
    )
SELECT strftime("%Y", date) AS year, strftime("%m", date) AS month, SUM(count)
FROM violations_per_date GROUP BY month ORDER BY year
"""

res2 = cu.execute(q2).fetchall()

# Create a dictionary with the result of the query for plotting
lowest_violations_month_dict = {}
for r in res2:
    lowest_violations_month_dict[
        str(datetime.datetime(int(r[0]), int(r[1]), 1).strftime('%B %Y'))
    ] = r[2]

# Create and plot the result
plt.plot(
    list(lowest_violations_month_dict.keys()),
    list(lowest_violations_month_dict.values()),
    "r.-"
)
plt.xlabel("Months")
plt.ylabel("Number of violations")
plt.title("Violation per month for the postcode with the lowest total violations")
plt.show()


## Average number of violations per month for all California (all postcode combined)
q3 = """
WITH
    postcode_violations_count (date, count) AS (
        SELECT i.activity_date, COUNT(v.serial_number) FROM inspections i
        JOIN violations v ON i.serial_number = v.serial_number
        GROUP BY i.facility_zip HAVING i.facility_state = 'CA'
    )
SELECT strftime("%Y", date) AS year, strftime("%m", date) AS month, AVG(count)
FROM postcode_violations_count GROUP BY month ORDER BY year
"""

res3 = cu.execute(q3).fetchall()

# Create a dictionary with the result of the query for plotting
avg_violations_month_ca_dict = {}
for r in res3:
    avg_violations_month_ca_dict[
        str(datetime.datetime(int(r[0]), int(r[1]), 1).strftime('%B %Y'))
    ] = r[2]

# Create and plot the result
plt.plot(
    list(avg_violations_month_ca_dict.keys()),
    list(avg_violations_month_ca_dict.values()),
    "g.-"
)
plt.xlabel("Months")
plt.xticks(rotation=60)
plt.ylabel("Average number of violations")
plt.title("Average number of violations per month for all California")
plt.show()


## Average number of violations per months for all McDonalds compared to the average for all Burger Kings
# Average number of violations per months for all McDonalds
q4 = """
WITH
    mcdonalds_violations_count (date, count) AS (
        SELECT i.activity_date, COUNT(v.serial_number) FROM inspections i
        JOIN violations v ON i.serial_number = v.serial_number
        GROUP BY i.facility_name HAVING i.facility_name LIKE '%MCDONALD%'
    )
SELECT strftime("%Y", date) AS year, strftime("%m", date) AS month, AVG(count)
FROM mcdonalds_violations_count GROUP BY month ORDER BY year
"""

res4 = cu.execute(q4).fetchall()

# Create a dictionary with the result of the query for plotting
avg_violations_month_mcdonalds_dict = {}
for r in res4:
    avg_violations_month_mcdonalds_dict[
        str(datetime.datetime(int(r[0]), int(r[1]), 1))
    ] = r[2]

# Average number of violations per months for all Burger Kings
q5 = """
WITH
    burgerking_violations_count (date, count) AS (
        SELECT i.activity_date, COUNT(v.serial_number) FROM inspections i
        JOIN violations v ON i.serial_number = v.serial_number
        GROUP BY i.facility_name HAVING i.facility_name LIKE '%BURGER KING%'
    )
SELECT strftime("%Y", date) AS year, strftime("%m", date) AS month, AVG(count)
FROM burgerking_violations_count GROUP BY month ORDER BY year
"""

res5 = cu.execute(q5).fetchall()

# Create a dictionary with the result of the query for plotting
avg_violations_month_burgerking_dict = {}
for r in res5:
    avg_violations_month_burgerking_dict[
        str(datetime.datetime(int(r[0]), int(r[1]), 1))
    ] = r[2]

# Create a list of the dates from the two requests as the x axis and remove duplicates
xaxis = sorted(set(list(avg_violations_month_mcdonalds_dict.keys()) + list(avg_violations_month_burgerking_dict.keys())))

# Make the dates human readable
xaxix_hr = []
for date in xaxis:
    xaxix_hr.append(dateutil.parser.parse(date).strftime("%b %Y"))

# Add missing values for the two y axis
avg_mcdonalds_dict = {}
avg_burgerking_dict = {}
for date in xaxis:
    if date in avg_violations_month_mcdonalds_dict:
        avg_mcdonalds_dict[date] = avg_violations_month_mcdonalds_dict[date]
    else:
        avg_mcdonalds_dict[date] = 0

    if date in avg_violations_month_burgerking_dict:
        avg_burgerking_dict[date] = avg_violations_month_burgerking_dict[date]
    else:
        avg_burgerking_dict[date] = 0

# Create and plot the result
plt.plot(
    xaxis,
    list(avg_mcdonalds_dict.values()),
    "r.-",
    label="Mc Donald's"
)
plt.plot(
    xaxis,
    list(avg_burgerking_dict.values()),
    "y.-",
    label="Burger King"
)

plt.xlabel("Months")
plt.xticks(range(len(xaxis)), xaxix_hr, rotation=90)
plt.ylabel("Average number of violations")
plt.title("Average number of violations per month \n for Mc Donald's compared to Burger King")
plt.legend()
plt.show()


## Retrieve distinct violation codes and descriptions
q6 = """
SELECT DISTINCT violation_code, violation_description FROM violations
"""

res6 = cu.execute(q6).fetchall()

# Create a dictionary with the results of the query
distinct_violations = {}
for r in res6:
    distinct_violations[r[0]] = r[1]

# Create lists with only the violations which have the word 'food' in their description
res_list = []
for key in distinct_violations:
    if re.search("food", distinct_violations[key]):
        res_list.append([key, distinct_violations[key]])

# Print the list to the console
print(tabulate(res_list, headers=['Code', 'Description']))