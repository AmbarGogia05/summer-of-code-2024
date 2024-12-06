# Model Documentation
## 1. The InventoryItem Model
Stores data related to all items present in inventory.
- Item_SKU: 
    - Integer datatype
    - Serves as primary key (unique identifier for each item in inventory)
- Item_Name:
    - String with length upto 80 characters
    - `nullable=False` prohibits leaving this field blank
- Item_Description:
    - String with length upto 200 characters
    - `nullable=True` allows leaving this field blank
- Item_Price:
    - Float datatype
    - Cannot be left blank
    - `validate_price` is used to ensure that only non-negative values can be stored here
- Item_Qty:
    - Integer datatype
    - Cannot be left blank

### Custom Method - `total_val`
This function is used to efficiently return the total value of all items present in the inventory, by querying the database.

## 2. The Customer Model
Stores customer data, including contact information.
- c_ID:
    - Integer datatype
    - Serves as primary key for the model (uniquely identifies each customer)
- c_Name:
    - String of length upto 100 characters
    - Stores names of customers, cannot be left blank
- c_Email:
    - String of length upto 100 characters
    - Stores email IDs of customers, cannot be left blank
    - `validate_email` is used to ensure that the email ID entered is correctly formatted
- c_Contact:
    - String of length 10 characters (declared 10 as parameter of string, but must be exactly 10 characters in length)
    - Cannot be left blank
    - `validate_phone_number` checks that input is legal - length of phone number must be 10 characters, and each character must be a digit (0-9).

## 3. The Staff Model
Stores data related to staff, including contact details and administrative status.
- s_ID:
    - Integer datatype
    - Serves as primary key for model (uniquely identifies each staff member)
- s_Name:
    - String of length upto 100 characters
    - Stores names of customers, cannot be left blank
- s_Email:
    - String of length upto 100 characters
    - Stores email IDs of customers, cannot be left blank
    - `validate_email` is used to ensure that the email ID entered is correctly formatted
- s_Contact:
    - String of length 10 characters (declared 10 as parameter of string, but must be exactly 10 characters in length)
    - Cannot be left blank
    - `validate_phone_number` checks that input is legal - length of phone number must be 10 characters, and each character must be a digit (0-9).

## 4. The Transaction Model
Stores data from each transaction and links to the Customer model using a foreign key.
- t_ID:
    - Integer datatype
    - Serves as primary key for the model (unique ID for each transaction)
- c_ID:
    - Integer datatype
    - References the c_ID in the Customer model, and acts as foreign key to link both models (Prevents entry of data in Transaction with a c_ID value that is not present in the Customer model)
- t_Date:
    - Date datatype (YYYY-MM-DD)
    - Cannot be left blank
- t_Amount:
    - Float datatype
    - Cannot be left blank, and is validated by `validate_amount` to prevent negative entries
- t_Category:
    - String of length upto 10 characters
    - Cannot be left blank
### Custom Method - `get_transactions`
This function returns a list of all transactions associated with a given customer ID.
