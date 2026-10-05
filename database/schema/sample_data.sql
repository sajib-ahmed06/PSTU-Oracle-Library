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
