# database/schema/sample_data.sql

Project support/configuration file; পূর্ণ source ও line reference নিচে দেওয়া হয়েছে।

Source: [মূল file](../../database/schema/sample_data.sql)। Snapshot 2026-10-04; 43 lines; SHA-256 `f7cabc4ace507dac06289b26ac70cf3c548472b9a904e42f4926e7d96a277bb3`।

## Function / object / element inventory


## সম্পূর্ণ original source

```sql
-- Sample members use the example session 2023-2024.
INSERT INTO student(name,department,phone,email,password,roll_no,registration_no,academic_session) VALUES('Rahim','CSE','01700000001','rahim@gmail.com',DBMS_RANDOM.STRING('X',30),'2300001','11700','2023-2024');
INSERT INTO student(name,department,phone,email,password,roll_no,registration_no,academic_session) VALUES('Karim','EEE','01700000002','karim@gmail.com',DBMS_RANDOM.STRING('X',30),'2300002','11701','2023-2024');
INSERT INTO student(name,department,phone,email,password,roll_no,registration_no,academic_session) VALUES('Sadia','BBA','01700000003','sadia@gmail.com',DBMS_RANDOM.STRING('X',30),'2300003','11702','2023-2024');
INSERT INTO student(name,department,phone,email,password,roll_no,registration_no,academic_session) VALUES('Nusrat Jahan','CSE','01700000004','nusrat@pstu.ac.bd',DBMS_RANDOM.STRING('X',30),'2300004','11703','2023-2024');
INSERT INTO student(name,department,phone,email,password,roll_no,registration_no,academic_session) VALUES('Tanvir Hasan','Agriculture','01700000005','tanvir@pstu.ac.bd',DBMS_RANDOM.STRING('X',30),'2300005','11704','2023-2024');
INSERT INTO student(name,department,phone,email,password,roll_no,registration_no,academic_session) VALUES('Mehedi Islam','EEE','01700000006','mehedi@pstu.ac.bd',DBMS_RANDOM.STRING('X',30),'2300006','11705','2023-2024');
INSERT INTO student(name,department,phone,email,password,roll_no,registration_no,academic_session) VALUES('Farzana Akter','Nutrition and Food Science','01700000007','farzana@pstu.ac.bd',DBMS_RANDOM.STRING('X',30),'2300007','11706','2023-2024');
INSERT INTO student(name,department,phone,email,password,roll_no,registration_no,academic_session) VALUES('Tasnim','CSE','01700000008','tasnim@pstu.ac.bd',DBMS_RANDOM.STRING('X',30),'2300008','11707','2023-2024');
INSERT INTO author(author_name) VALUES('Robert C. Martin');
INSERT INTO author(author_name) VALUES('Herbert Schildt');
INSERT INTO author(author_name) VALUES('Elmasri & Navathe');
INSERT INTO author(author_name) VALUES('Abraham Silberschatz');
INSERT INTO author(author_name) VALUES('Thomas H. Cormen');
INSERT INTO author(author_name) VALUES('Andrew S. Tanenbaum');
INSERT INTO category(category_name) VALUES('Database');
INSERT INTO category(category_name) VALUES('Programming');
INSERT INTO category(category_name) VALUES('Software Engineering');
INSERT INTO category(category_name) VALUES('Algorithms');
INSERT INTO category(category_name) VALUES('Computer Networks');
INSERT INTO category(category_name) VALUES('Operating Systems');
INSERT INTO book(title,author_id,category_id,publisher,quantity,available_quantity) VALUES('Database System Concepts',4,1,'McGraw Hill',10,10);
INSERT INTO book(title,author_id,category_id,publisher,quantity,available_quantity) VALUES('Java Programming',2,2,'Tata McGraw',8,8);
INSERT INTO book(title,author_id,category_id,publisher,quantity,available_quantity) VALUES('Clean Code',1,3,'Pearson',5,5);
INSERT INTO book(title,author_id,category_id,publisher,quantity,available_quantity) VALUES('Operating System Concepts',4,6,'Wiley',7,7);
INSERT INTO book(title,author_id,category_id,publisher,quantity,available_quantity) VALUES('Introduction to Algorithms',5,4,'MIT Press',6,6);
INSERT INTO book(title,author_id,category_id,publisher,quantity,available_quantity) VALUES('Computer Networks',6,5,'Pearson',9,9);
INSERT INTO book(title,author_id,category_id,publisher,quantity,available_quantity) VALUES('Effective Java',2,2,'Addison-Wesley',4,4);
INSERT INTO book(title,author_id,category_id,publisher,quantity,available_quantity) VALUES('Clean Architecture',1,3,'Pearson',5,5);
INSERT INTO issue_book(student_id,book_id,issue_date,due_date,status) VALUES(1,1,SYSDATE,SYSDATE+15,'ISSUED');
INSERT INTO issue_book(student_id,book_id,issue_date,due_date,status) VALUES(2,2,SYSDATE,SYSDATE+15,'ISSUED');
INSERT INTO issue_book(student_id,book_id,issue_date,due_date,status) VALUES(4,5,SYSDATE-2,SYSDATE+13,'ISSUED');
INSERT INTO issue_book(student_id,book_id,issue_date,due_date,status) VALUES(5,6,SYSDATE-25,SYSDATE-10,'ISSUED');
INSERT INTO issue_book(student_id,book_id,issue_date,due_date,status) VALUES(6,4,SYSDATE-18,SYSDATE-3,'ISSUED');
BEGIN return_book_proc(4); END;
/
BEGIN return_book_proc(5); END;
/
UPDATE fine SET payment_status='PAID',paid_amount=amount WHERE issue_id=5;
COMMIT;

INSERT INTO login_user(username,password,user_type) VALUES(:seed_admin_username,:seed_admin_password,'ADMIN');
COMMIT;
```

## প্রতিটি line-এর reading notes

| Line | Original line | ব্যাখ্যা |
| --- | --- | --- |
| 1 | <code>-- Sample members use the example session 2023-2024.</code> | Comment/documentation; উদ্দেশ্য বা design choice বোঝায়, নিজে business operation execute করে না। |
| 2 | <code>INSERT INTO student(name,department,phone,email,password,roll_no,registration_no,academic_session) VALUES(&#x27;Rahim&#x27;,&#x27;CSE&#x27;,&#x27;01700000001&#x27;,&#x27;rahim@gmail.com&#x27;,DBMS_RANDOM.STRING(&#x27;X&#x27;,30),&#x27;2300001&#x27;,&#x27;11700&#x27;,&#x27;2023-2024&#x27;);</code> | নতুন business/audit/sample row insert করার statement। |
| 3 | <code>INSERT INTO student(name,department,phone,email,password,roll_no,registration_no,academic_session) VALUES(&#x27;Karim&#x27;,&#x27;EEE&#x27;,&#x27;01700000002&#x27;,&#x27;karim@gmail.com&#x27;,DBMS_RANDOM.STRING(&#x27;X&#x27;,30),&#x27;2300002&#x27;,&#x27;11701&#x27;,&#x27;2023-2024&#x27;);</code> | নতুন business/audit/sample row insert করার statement। |
| 4 | <code>INSERT INTO student(name,department,phone,email,password,roll_no,registration_no,academic_session) VALUES(&#x27;Sadia&#x27;,&#x27;BBA&#x27;,&#x27;01700000003&#x27;,&#x27;sadia@gmail.com&#x27;,DBMS_RANDOM.STRING(&#x27;X&#x27;,30),&#x27;2300003&#x27;,&#x27;11702&#x27;,&#x27;2023-2024&#x27;);</code> | নতুন business/audit/sample row insert করার statement। |
| 5 | <code>INSERT INTO student(name,department,phone,email,password,roll_no,registration_no,academic_session) VALUES(&#x27;Nusrat Jahan&#x27;,&#x27;CSE&#x27;,&#x27;01700000004&#x27;,&#x27;nusrat@pstu.ac.bd&#x27;,DBMS_RANDOM.STRING(&#x27;X&#x27;,30),&#x27;2300004&#x27;,&#x27;11703&#x27;,&#x27;2023-2024&#x27;);</code> | নতুন business/audit/sample row insert করার statement। |
| 6 | <code>INSERT INTO student(name,department,phone,email,password,roll_no,registration_no,academic_session) VALUES(&#x27;Tanvir Hasan&#x27;,&#x27;Agriculture&#x27;,&#x27;01700000005&#x27;,&#x27;tanvir@pstu.ac.bd&#x27;,DBMS_RANDOM.STRING(&#x27;X&#x27;,30),&#x27;2300005&#x27;,&#x27;11704&#x27;,&#x27;2023-2024&#x27;);</code> | নতুন business/audit/sample row insert করার statement। |
| 7 | <code>INSERT INTO student(name,department,phone,email,password,roll_no,registration_no,academic_session) VALUES(&#x27;Mehedi Islam&#x27;,&#x27;EEE&#x27;,&#x27;01700000006&#x27;,&#x27;mehedi@pstu.ac.bd&#x27;,DBMS_RANDOM.STRING(&#x27;X&#x27;,30),&#x27;2300006&#x27;,&#x27;11705&#x27;,&#x27;2023-2024&#x27;);</code> | নতুন business/audit/sample row insert করার statement। |
| 8 | <code>INSERT INTO student(name,department,phone,email,password,roll_no,registration_no,academic_session) VALUES(&#x27;Farzana Akter&#x27;,&#x27;Nutrition and Food Science&#x27;,&#x27;01700000007&#x27;,&#x27;farzana@pstu.ac.bd&#x27;,DBMS_RANDOM.STRING(&#x27;X&#x27;,30),&#x27;2300007&#x27;,&#x27;11706&#x27;,&#x27;2023-2024&#x27;);</code> | নতুন business/audit/sample row insert করার statement। |
| 9 | <code>INSERT INTO student(name,department,phone,email,password,roll_no,registration_no,academic_session) VALUES(&#x27;Tasnim&#x27;,&#x27;CSE&#x27;,&#x27;01700000008&#x27;,&#x27;tasnim@pstu.ac.bd&#x27;,DBMS_RANDOM.STRING(&#x27;X&#x27;,30),&#x27;2300008&#x27;,&#x27;11707&#x27;,&#x27;2023-2024&#x27;);</code> | নতুন business/audit/sample row insert করার statement। |
| 10 | <code>INSERT INTO author(author_name) VALUES(&#x27;Robert C. Martin&#x27;);</code> | নতুন business/audit/sample row insert করার statement। |
| 11 | <code>INSERT INTO author(author_name) VALUES(&#x27;Herbert Schildt&#x27;);</code> | নতুন business/audit/sample row insert করার statement। |
| 12 | <code>INSERT INTO author(author_name) VALUES(&#x27;Elmasri &amp; Navathe&#x27;);</code> | নতুন business/audit/sample row insert করার statement। |
| 13 | <code>INSERT INTO author(author_name) VALUES(&#x27;Abraham Silberschatz&#x27;);</code> | নতুন business/audit/sample row insert করার statement। |
| 14 | <code>INSERT INTO author(author_name) VALUES(&#x27;Thomas H. Cormen&#x27;);</code> | নতুন business/audit/sample row insert করার statement। |
| 15 | <code>INSERT INTO author(author_name) VALUES(&#x27;Andrew S. Tanenbaum&#x27;);</code> | নতুন business/audit/sample row insert করার statement। |
| 16 | <code>INSERT INTO category(category_name) VALUES(&#x27;Database&#x27;);</code> | নতুন business/audit/sample row insert করার statement। |
| 17 | <code>INSERT INTO category(category_name) VALUES(&#x27;Programming&#x27;);</code> | নতুন business/audit/sample row insert করার statement। |
| 18 | <code>INSERT INTO category(category_name) VALUES(&#x27;Software Engineering&#x27;);</code> | নতুন business/audit/sample row insert করার statement। |
| 19 | <code>INSERT INTO category(category_name) VALUES(&#x27;Algorithms&#x27;);</code> | নতুন business/audit/sample row insert করার statement। |
| 20 | <code>INSERT INTO category(category_name) VALUES(&#x27;Computer Networks&#x27;);</code> | নতুন business/audit/sample row insert করার statement। |
| 21 | <code>INSERT INTO category(category_name) VALUES(&#x27;Operating Systems&#x27;);</code> | নতুন business/audit/sample row insert করার statement। |
| 22 | <code>INSERT INTO book(title,author_id,category_id,publisher,quantity,available_quantity) VALUES(&#x27;Database System Concepts&#x27;,4,1,&#x27;McGraw Hill&#x27;,10,10);</code> | নতুন business/audit/sample row insert করার statement। |
| 23 | <code>INSERT INTO book(title,author_id,category_id,publisher,quantity,available_quantity) VALUES(&#x27;Java Programming&#x27;,2,2,&#x27;Tata McGraw&#x27;,8,8);</code> | নতুন business/audit/sample row insert করার statement। |
| 24 | <code>INSERT INTO book(title,author_id,category_id,publisher,quantity,available_quantity) VALUES(&#x27;Clean Code&#x27;,1,3,&#x27;Pearson&#x27;,5,5);</code> | নতুন business/audit/sample row insert করার statement। |
| 25 | <code>INSERT INTO book(title,author_id,category_id,publisher,quantity,available_quantity) VALUES(&#x27;Operating System Concepts&#x27;,4,6,&#x27;Wiley&#x27;,7,7);</code> | নতুন business/audit/sample row insert করার statement। |
| 26 | <code>INSERT INTO book(title,author_id,category_id,publisher,quantity,available_quantity) VALUES(&#x27;Introduction to Algorithms&#x27;,5,4,&#x27;MIT Press&#x27;,6,6);</code> | নতুন business/audit/sample row insert করার statement। |
| 27 | <code>INSERT INTO book(title,author_id,category_id,publisher,quantity,available_quantity) VALUES(&#x27;Computer Networks&#x27;,6,5,&#x27;Pearson&#x27;,9,9);</code> | নতুন business/audit/sample row insert করার statement। |
| 28 | <code>INSERT INTO book(title,author_id,category_id,publisher,quantity,available_quantity) VALUES(&#x27;Effective Java&#x27;,2,2,&#x27;Addison-Wesley&#x27;,4,4);</code> | নতুন business/audit/sample row insert করার statement। |
| 29 | <code>INSERT INTO book(title,author_id,category_id,publisher,quantity,available_quantity) VALUES(&#x27;Clean Architecture&#x27;,1,3,&#x27;Pearson&#x27;,5,5);</code> | নতুন business/audit/sample row insert করার statement। |
| 30 | <code>INSERT INTO issue_book(student_id,book_id,issue_date,due_date,status) VALUES(1,1,SYSDATE,SYSDATE+15,&#x27;ISSUED&#x27;);</code> | নতুন business/audit/sample row insert করার statement। |
| 31 | <code>INSERT INTO issue_book(student_id,book_id,issue_date,due_date,status) VALUES(2,2,SYSDATE,SYSDATE+15,&#x27;ISSUED&#x27;);</code> | নতুন business/audit/sample row insert করার statement। |
| 32 | <code>INSERT INTO issue_book(student_id,book_id,issue_date,due_date,status) VALUES(4,5,SYSDATE-2,SYSDATE+13,&#x27;ISSUED&#x27;);</code> | নতুন business/audit/sample row insert করার statement। |
| 33 | <code>INSERT INTO issue_book(student_id,book_id,issue_date,due_date,status) VALUES(5,6,SYSDATE-25,SYSDATE-10,&#x27;ISSUED&#x27;);</code> | নতুন business/audit/sample row insert করার statement। |
| 34 | <code>INSERT INTO issue_book(student_id,book_id,issue_date,due_date,status) VALUES(6,4,SYSDATE-18,SYSDATE-3,&#x27;ISSUED&#x27;);</code> | নতুন business/audit/sample row insert করার statement। |
| 35 | <code>BEGIN return_book_proc(4); END;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 36 | <code>/</code> | SQL*Plus আগের PL/SQL buffer execute করার delimiter। |
| 37 | <code>BEGIN return_book_proc(5); END;</code> | PL/SQL declaration, SQL field/value বা multi-line expression continuation; enclosing object-এর source ও purpose-এর সঙ্গে পড়ো। |
| 38 | <code>/</code> | SQL*Plus আগের PL/SQL buffer execute করার delimiter। |
| 39 | <code>UPDATE fine SET payment_status=&#x27;PAID&#x27;,paid_amount=amount WHERE issue_id=5;</code> | Existing record fields পরিবর্তন অথবা trigger UPDATE scope ঘোষণা করে। |
| 40 | <code>COMMIT;</code> | Business changes ও transactional audit durable করে; rollback-এর সুযোগ এখানেই শেষ। |
| 41 | <code>&nbsp;</code> | খালি line; logical blocks আলাদা করে। |
| 42 | <code>INSERT INTO login_user(username,password,user_type) VALUES(:seed_admin_username,:seed_admin_password,&#x27;ADMIN&#x27;);</code> | নতুন business/audit/sample row insert করার statement। |
| 43 | <code>COMMIT;</code> | Business changes ও transactional audit durable করে; rollback-এর সুযোগ এখানেই শেষ। |
