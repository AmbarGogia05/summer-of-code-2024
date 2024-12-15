### Bonus Tasks for Week 2
2. **Testing:**
   - Write unit tests using pytest to verify CRUD operations and API endpoints.
   - Include integration tests to ensure proper interaction between frontend and backend.

3. **Documentation:** -- FIGURE OUT LATER
   - Generate API documentation using tools like Swagger or Flask-RESTPlus.
   - Document frontend interfaces and backend architecture for future reference.

5. **Security Measures:**
   - Apply security best practices such as input validation, SQL injection prevention, and CSRF protection.

## Yet to build home pages for staff, admin, customers

### Bonus Tasks for Week 3
### Password reset for staff left, for customers functional already

3. **Multi-Factor Authentication (MFA):** -- NEED TO LEARN HOW
   - Implement multi-factor authentication to enhance staff account security. 
   - Integrate with an MFA provider or use time-based one-time passwords (TOTP).

4. **Logging and Monitoring:** -- NEED TO LEARN HOW
   - Implement logging to track authentication events (e.g., logins, logouts, failed login attempts).
   - Monitor staff activity and identify potential security threats.

6. **Transaction Analytics:** -- NEED TO LEARN HOW
   - Implement analytics for transactions to provide insights into sales and performance.
   - Create reports for transaction history, sales trends, and staff performance.


### Task 3: Invoice Generation

#### Generating PDF Invoices

1. **Library Selection:**
   - Choose a library for PDF generation: ReportLab or WeasyPrint.
   - Install the chosen library using `pip install reportlab` or `pip install weasyprint`.

2. **PDF Invoice Generation:**
   - Implement functionality to generate PDF invoices for each transaction.
   - Ensure invoices contain all necessary details (e.g., transaction ID, product details, total amount).

3. **Local Storage:**
   - Store generated PDF invoices locally for now.
   - Implement functionality to retrieve and display these invoices as needed.

### Task 4: Transaction History

#### Developing Endpoints for Transaction History

1. **Transaction History Endpoints:**
   - Create endpoints to retrieve transaction history (`/transactions/history`).

2. **Secure Access:**
   - Ensure secure access to transaction history data, possibly by restricting access to authenticated and authorized staff.
