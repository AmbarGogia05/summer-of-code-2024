### Bonus Tasks for Week 2

1. **Advanced CRUD Operations:** --> DONE
   - Implement pagination and filtering for product lists.
   - Add sorting capabilities based on various product attributes.

2. **Testing:**
   - Write unit tests using pytest to verify CRUD operations and API endpoints.
   - Include integration tests to ensure proper interaction between frontend and backend.

3. **Documentation:** -- FIGURE OUT LATER
   - Generate API documentation using tools like Swagger or Flask-RESTPlus.
   - Document frontend interfaces and backend architecture for future reference.

4. **Error Handling:**
   - Implement error handling mechanisms for API responses (e.g., 404 Not Found, 500 Internal Server Error).
   - Use Flask error handlers to provide meaningful error messages.

5. **Security Measures:**
   - Apply security best practices such as input validation, SQL injection prevention, and CSRF protection.
   - Ensure sensitive data (like passwords) are stored securely using hashed values.

## Main tasks for week 2 are complete

## Week 3 Task 1 is complete

# Make a staff approval page

**Create API Endpoints for Customers:**
   - Design and implement RESTful API endpoints for managing customers (`/customers`).
   - Define endpoints for Create, Read, Update, and Delete operations.
   - Ensure proper HTTP methods (`GET`, `POST`, `PUT`, `DELETE`) are used as per REST conventions.

## Need to figure out how to differentiate between customers and staff when logged in using roles
## Update the database and apply a migration

4. **CRUD Operations:**
   - Implement functions/methods to handle:
     - Create a new staff member (admin-only). --> DONE
     - Approve a new staff member (admin-only). --> TO DO
     - Retrieve a list of all staff members or a specific staff member by ID. --> TO DO
     - Update an existing staff member (admin-only). --> TO DO
     - Delete a staff member from the database (admin-only). --> TO DO
     - Create a new customer.
     - Retrieve a list of all customers or a specific customer by ID.
     - Update an existing customer.
     - Delete a customer from the database.

     All customer tasks yet to be done

### Task 3: Transaction Management

#### Implementing Transaction CRUD Operations

1. **Transaction Model:**
   - Create a Transaction model with fields for `id`, `c_id` (customer ID), `s_id`, `product_amount_list`, `date`, and `time`.
   - Ensure proper relationships between the Transaction model and the Customer and Staff models.

2. **Create API Endpoints for Transactions:**
   - Design and implement RESTful API endpoints for managing transactions (`/transactions`).
   - Define endpoints for Create, Read, Update, and Delete operations.
   - Ensure proper HTTP methods (`GET`, `POST`, `PUT`, `DELETE`) are used as per REST conventions.

3. **CRUD Operations:**
   - Implement functions/methods to handle:
     - Create a new transaction.
     - Retrieve a list of all transactions or a specific transaction by ID.
     - Update an existing transaction.
     - Delete a transaction from the database.

### Task 4: Secure Password Handling

#### Implementing Secure Password Handling

1. **Password Hashing:**  --> Have done using different method, need to check whether this needs updates
   - Use bcrypt to hash staff passwords before storing them in the database.
   - Implement password hashing during staff registration.

3. **Session Management:**
   - Configure session management to maintain staff login sessions. --> DONE
   - Securely store session information and handle session expiration. --> WILL SEE IF IMPROVEMENTS NEEDED

### Bonus Tasks for Week 3

1. **Email Verification:**
   - Implement email verification during staff registration to ensure valid email addresses. --> DONE
   - Send verification emails with unique tokens for account activation. --> HOW?

2. **Password Reset:**
   - Implement password reset functionality to allow staff to reset their passwords if they forget them. --> TO DO
   - Send password reset emails with unique tokens for secure password updates. --> HOW?

3. **Multi-Factor Authentication (MFA):** -- NEED TO LEARN HOW
   - Implement multi-factor authentication to enhance staff account security. 
   - Integrate with an MFA provider or use time-based one-time passwords (TOTP).

4. **Logging and Monitoring:** -- NEED TO LEARN HOW
   - Implement logging to track authentication events (e.g., logins, logouts, failed login attempts).
   - Monitor staff activity and identify potential security threats.

5. **Advanced Role Management:** -- DAMN
   - Implement more complex role hierarchies and permissions.
   - Allow dynamic role assignment and modification through the admin interface.

6. **Transaction Analytics:** -- DUDE
   - Implement analytics for transactions to provide insights into sales and performance.
   - Create reports for transaction history, sales trends, and staff performance.