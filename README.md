## 7810ICT -- Software Technologies Assignment

### Eliott de SEGUIER -- s5151654

---

#### Guidelines
- Install **openpyxl**, **matplotlib** and **tabulate** package
- Be sure that **inspections.xlsx** and **violations.xlsx** files are at the 
root of the project 

---

#### Steps
1. Run **create.db.py** file
2. Run **sql_food.py** file
3. Run **excel_food** file
4. Run **numpy_food.py** file

---
#### Files
- **create.db.py** -> creates the database **db.sqlite**, the tables 
**inspections** and **violations** and insert into them the respective 
data from the files **inspections.xlsx** and **violations.xlsx**

- **sql_food.py** --> prints two lists to the console
    - The list of distinctive businesses that have at least one violation 
    ordered alphabetically
    - The list of distinctive businesses that have at least one violation 
    along with and ordered by the count of their violations

- **excel_food.py** --> creates a new workbook **ViolationTypes.xlsx** 
containing a distinctive list of violations code along with their description
and number of occurrences in **violations** table

- **numpy_food.py** --> prints a list of distinctive violations code and
description containing the word 'food' and plots several graphs:
    - the number of violations per month for the postcode with the highest
    total of violations
    - the number of violations per month for the postcode with the lowest
    total of violations
    - the average number of violations per months for all California (all
    postcode (all postcodes combined)
    - the average number of violations per month for all McDonalds compared
    with the average of all Burger Kings