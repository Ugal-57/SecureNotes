### **🔐 SecureNotes — Vulnerable vs Secure Web Application**



SecureNotes is a deliberately vulnerable Flask web application built to demonstrate real-world OWASP Top 10 web security issues and their mitigations.



The project follows a **Red Team** → **Blue Team** approach:



* 🔴 First, vulnerabilities are intentionally implemented and exploited



* 🟢 Then, the application is hardened using industry-standard security practices



This provides hands-on understanding of both attack and defense perspectives in web security.



🎯 **Project Objectives**



* Demonstrate common web application vulnerabilities
* Perform hands-on exploitation of insecure implementations
* Apply secure coding best practices
* Compare vulnerable vs hardened application behavior
* Build practical web penetration testing skills



🏗️ **Tech Stack**



Python, Flask, SQLite, Jinja2, HTML5, CSS3, Bootstrap 5, Git, Burp Suite



📂 **Project Structure**

SecureNotes/

│

├── vulnerable\_app/

│   ├── app.py

│   ├── database.db

│   ├── uploads/

│   └── templates/

│

├── secure\_app/

│   ├── app.py

│   ├── database.db

│   ├── uploads/

│   └── templates/

│

└── README.md



##### 🔴 **Vulnerable Application**



The vulnerable version intentionally contains multiple OWASP Top 10 security flaws for educational and testing purposes.



**🚨 Vulnerabilities Demonstrated**

**🔴 1. SQL Injection (Authentication Bypass)**



**Description:**

The login functionality constructs SQL queries using unsanitized user input.



**Impact:**

Attackers can bypass authentication without valid credentials.



**Proof of Concept Payload:**

|' OR '1'='1' --|
|-|



**Result:**

Successfully logged into the application without knowing the password.



**OWASP:** Injection



**🔴 2. Stored Cross-Site Scripting (XSS)**



**Description:**

User notes are rendered using unsafe Jinja output (|safe) without sanitization.



**Impact:**

Attackers can execute arbitrary JavaScript in victims’ browsers.



**Proof of Concept Payload:**

|<script>alert(1)</script>|
|-|



**Result:**

JavaScript executes whenever the dashboard loads.



**OWASP:** Cross-Site Scripting (XSS)



**🔴 3. Broken Authentication (Plaintext Passwords)**



**Description:**

User passwords are stored directly in the database without hashing.



**Impact:**

Database compromise exposes all user credentials.



**Proof of Concept:**

|SELECT username, password FROM users;|
|-|



**Result:**

Passwords visible in readable plaintext.



**OWASP:** Identification and Authentication Failures



**🔴 4. Weak Flask Secret Key**



**Description:**

Application uses a hardcoded predictable secret key.

|app.secret\_key = "insecure\_secret\_key"|
|-|



**Impact:**

Session cookies may be forged or tampered with.



**OWASP:** Security Misconfiguration



**🔴 5. Insecure File Upload**



**Description:**

The application allows unrestricted file uploads without validation.



**Impact:**

Attackers can upload malicious files (HTML, scripts, potential web shells).



**Proof of Concept:**

Files such as:

|test.html<br />shell.php|
|-|



were successfully uploaded to the server.



**OWASP:** Security Misconfiguration / Unrestricted File Upload

##### 

##### **🟢 Secure Application (Hardened Version)**



The secure version remediates all identified vulnerabilities using industry best practices.



✅ **Security Improvements Implemented**



**🟢 SQL Injection Prevention**



* Parameterized queries used throughout the application
* User input properly handled



**🟢 Secure Password Storage**



* Passwords hashed using bcrypt
* Automatic salting applied
* Plaintext storage eliminated



**🟢 Stored XSS Mitigation**



* Removed unsafe Jinja rendering
* Enabled automatic output escaping



**🟢 Secure File Upload**



* File type whitelist enforced
* Filenames sanitized
* Randomized file naming implemented
* User feedback via flash messages



**🟢 Strong Session Security**



* Cryptographically secure secret key
* Proper logout with session destruction



**🟢 Security Headers Added**



* The application implements:
* Content Security Policy (CSP)
* X-Frame-Options
* X-Content-Type-Options
* Referrer-Policy
* Strict-Transport-Security



These mitigate XSS impact, clickjacking, and MIME sniffing attacks.



##### 🧪 How to Run



1️⃣ Install dependencies

|pip install flask flask-bcrypt|
|-|



2️⃣ Run Vulnerable App

|cd vulnerable\_app<br />python app.py|
|-|



Open:

|http://127.0.0.1:5000|
|-|



3️⃣ Run Secure App

|cd secure\_app<br />python app.py|
|-|



Open:

|http://127.0.0.1:5001|
|-|



**🔬 Testing Guide**



**SQL Injection Test (vulnerable only)**

|' OR '1'='1' --|
|-|



✅ Works in vulnerable

❌ Blocked in secure



**XSS Test**

|<script>alert(1)</script>|
|-|



✅ Executes in vulnerable

❌ Rendered as text in secure



**File Upload Test**



Try uploading:

|shell.php<br />test.html|
|-|



✅ Allowed in vulnerable

❌ Blocked in secure



###### **⚠️ Disclaimer**



This project is built strictly for educational and ethical security research purposes.



Do **NOT** deploy the vulnerable version in production environments.



**👨‍💻 Author**



Ugal Sharma

Technical Lead (Red Team \& Web Pentesting) — The CyberSapiens



⭐ **Future Enhancements**



* CSRF protection
* Rate limiting
* JWT-based authentication
* Advanced logging \& monitoring
* Optional production deployment
