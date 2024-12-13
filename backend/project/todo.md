### Bonus Tasks for Week 2
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
## Yet to build home pages for staff, admin, customers

### Task 3: Transaction Management

#### Implementing Transaction CRUD Operations
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
3. **Session Management:**
   - Securely store session information and handle session expiration. --> WILL SEE IF IMPROVEMENTS NEEDED

### Bonus Tasks for Week 3

1. **Email Verification:**
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