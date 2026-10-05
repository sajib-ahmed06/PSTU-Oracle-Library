# Project queries: output ও verification

এই query-গুলো Oracle SQLPlus/SQL Developer-এ project schema দিয়ে চালাতে হবে। এখানে শুধু SELECT আছে; existing data পরিবর্তন হবে না। ID 1 এবং search text নিজের প্রয়োজনমতো বদলাতে পারবেন। Output-এর column নাম query-তেই দেওয়া আছে; live result সময় ও data অনুযায়ী বদলাবে।

SQLPlus-এ বড় output দেখতে আগে:
```sql
SET LINESIZE 250
SET PAGESIZE 100
SET LONG 100000
SET LONGCHUNKSIZE 100000
SET DEFINE OFF
```

Fine নিয়ম: 14 দিনের loan; overdue প্রতি calendar day 10 টাকা। Active overdue amount estimate; return-এর পরে fine table-এ recorded amount থাকে। Audit time UTC। Sequence LAST_NUMBER cached allocation দেখাতে পারে, পরের ID-এর নিশ্চয়তা নয়।

## 1. Connection ও Oracle সময়

```sql
SELECT 1 AS connection_ok, SYSDATE AS database_time FROM dual;
```

## 2. Dashboard: বই, কপি, member ও active loan

```sql
SELECT (SELECT COUNT(*) FROM book) AS book_titles,
       (SELECT NVL(SUM(quantity),0) FROM book) AS total_copies,
       (SELECT NVL(SUM(available_quantity),0) FROM book) AS available_copies,
       (SELECT COUNT(*) FROM student WHERE membership_status='ACTIVE') AS active_members,
       (SELECT COUNT(*) FROM issue_book WHERE status='ISSUED') AS active_loans
FROM dual;
```

## 3. বইয়ের পুরো board

```sql
SELECT * FROM book_details ORDER BY title;
```

## 4. বই খোঁজা: Clean এর জায়গায় নিজের search লিখুন

```sql
SELECT * FROM book_details
WHERE LOWER(title||author_name||category_name) LIKE '%clean%' ORDER BY title;
```

## 5. সব member: roll ও registration সহ

```sql
SELECT student_id, name, department, phone, email, membership_status, roll_no, registration_no, academic_session
FROM student ORDER BY student_id;
```

## 6. Member 1 এর details

```sql
SELECT student_id, name, department, phone, email, membership_status, roll_no, registration_no, academic_session
FROM student WHERE student_id=1;
```

## 7. Roll / registration দিয়ে member খোঁজা

```sql
SELECT student_id, name, roll_no, registration_no, membership_status
FROM student WHERE UPPER(TRIM(roll_no))='2300001' OR UPPER(TRIM(registration_no))='11700';
```

## 8. Author ও category

```sql
SELECT author_id, author_name FROM author ORDER BY author_name;
SELECT category_id, category_name FROM category ORDER BY category_name;
```

## 9. Issue ও return history: frontend-এর একই overdue হিসাব

```sql
SELECT i.issue_id, s.student_id, s.name, s.roll_no, s.registration_no,
       b.book_id, b.title, i.issue_date, i.due_date, i.return_date, i.status,
       CASE WHEN i.status='ISSUED' THEN GREATEST(TRUNC(SYSDATE)-TRUNC(NVL(i.due_date,SYSDATE)),0) ELSE 0 END AS overdue_days,
       CASE WHEN i.status='ISSUED' THEN GREATEST(TRUNC(SYSDATE)-TRUNC(NVL(i.due_date,SYSDATE)),0)*10 ELSE 0 END AS current_fine
FROM issue_book i JOIN student s ON s.student_id=i.student_id
JOIN book b ON b.book_id=i.book_id ORDER BY i.issue_date DESC, i.issue_id DESC;
```

## 10. বর্তমানে issued বই

```sql
SELECT i.issue_id, s.name, s.roll_no, b.title, i.issue_date, i.due_date
FROM issue_book i JOIN student s ON s.student_id=i.student_id
JOIN book b ON b.book_id=i.book_id WHERE i.status='ISSUED' ORDER BY i.due_date;
```

## 11. শুধু overdue: return করার আগের estimated fine

```sql
SELECT i.issue_id, s.name, s.roll_no, s.registration_no, b.title, i.due_date,
       GREATEST(TRUNC(SYSDATE)-TRUNC(i.due_date),0) AS overdue_days,
       GREATEST(TRUNC(SYSDATE)-TRUNC(i.due_date),0)*10 AS estimated_fine
FROM issue_book i JOIN student s ON s.student_id=i.student_id
JOIN book b ON b.book_id=i.book_id
WHERE i.status='ISSUED' AND TRUNC(i.due_date)<TRUNC(SYSDATE) ORDER BY i.due_date;
```

## 12. Return board এবং return-এর সময়ের fine

```sql
SELECT r.return_id, i.issue_id, s.name, s.roll_no, b.title,
       i.due_date, r.return_date, r.fine_amount, r.status, f.payment_status
FROM return_book r JOIN issue_book i ON i.issue_id=r.issue_id
JOIN student s ON s.student_id=i.student_id JOIN book b ON b.book_id=i.book_id
LEFT JOIN fine f ON f.issue_id=i.issue_id ORDER BY r.return_id DESC;
```

## 13. Fine history: paid ও unpaid

```sql
SELECT f.fine_id, i.issue_id, s.student_id, s.name, s.roll_no, s.registration_no,
       b.title, i.return_date, f.amount, f.payment_status
FROM fine f JOIN issue_book i ON i.issue_id=f.issue_id
JOIN student s ON s.student_id=i.student_id JOIN book b ON b.book_id=i.book_id
ORDER BY f.fine_id DESC;
```

## 14. শুধু unpaid fine

```sql
SELECT f.fine_id, s.name, b.title, f.amount, i.return_date
FROM fine f JOIN issue_book i ON i.issue_id=f.issue_id
JOIN student s ON s.student_id=i.student_id JOIN book b ON b.book_id=i.book_id
WHERE f.payment_status='UNPAID' ORDER BY f.fine_id DESC;
```

## 15. Fine section-এর total: double counting বাদ দিয়ে

```sql
SELECT recorded_unpaid, overdue_estimate, recorded_unpaid+overdue_estimate AS total_outstanding
FROM (SELECT
 (SELECT NVL(SUM(amount),0) FROM fine WHERE payment_status='UNPAID') AS recorded_unpaid,
 (SELECT NVL(SUM(GREATEST(TRUNC(SYSDATE)-TRUNC(NVL(i.due_date,SYSDATE)),0)*10),0)
  FROM issue_book i WHERE i.status='ISSUED'
  AND NOT EXISTS (SELECT 1 FROM fine f WHERE f.issue_id=i.issue_id)) AS overdue_estimate
 FROM dual);
```

## 16. Member 1-এর loan ও unpaid fine: issue/disable validation

```sql
SELECT COUNT(*) AS active_loans FROM issue_book WHERE student_id=1 AND status='ISSUED';
SELECT COUNT(*) AS unpaid_fines, NVL(SUM(f.amount),0) AS unpaid_amount
FROM fine f JOIN issue_book i ON i.issue_id=f.issue_id
WHERE i.student_id=1 AND f.payment_status='UNPAID';
```

## 17. Accounts board: password বাদ দিয়ে

```sql
SELECT user_id, username, user_type, account_status FROM login_user ORDER BY user_id;
SELECT admin_id, name, email FROM admin ORDER BY admin_id;
```

## 18. Audit: সর্বশেষ 25টি change ও before/after

```sql
SELECT * FROM (SELECT audit_id, occurred_at, actor, action, entity, record_id, before_data, after_data
FROM audit_log ORDER BY audit_id DESC) WHERE ROWNUM<=25;
```

## 19. এক member-এর সব audit

```sql
SELECT audit_id, occurred_at, actor, action, before_data, after_data
FROM audit_log WHERE entity='STUDENT' AND record_id=1 ORDER BY audit_id DESC;
```

## 20. Audit filter এবং action count

```sql
SELECT audit_id, occurred_at, actor, action, entity, record_id
FROM audit_log WHERE action='UPDATE' ORDER BY audit_id DESC;
SELECT entity, action, COUNT(*) AS event_count FROM audit_log GROUP BY entity, action ORDER BY entity, action;
```

## 21. সব table-এর row count

```sql
SELECT 'ADMIN' AS table_name, COUNT(*) AS row_count FROM admin
UNION ALL SELECT 'STUDENT', COUNT(*) FROM student
UNION ALL SELECT 'AUTHOR', COUNT(*) FROM author
UNION ALL SELECT 'CATEGORY', COUNT(*) FROM category
UNION ALL SELECT 'BOOK', COUNT(*) FROM book
UNION ALL SELECT 'ISSUE_BOOK', COUNT(*) FROM issue_book
UNION ALL SELECT 'RETURN_BOOK', COUNT(*) FROM return_book
UNION ALL SELECT 'FINE', COUNT(*) FROM fine
UNION ALL SELECT 'LOGIN_USER', COUNT(*) FROM login_user
UNION ALL SELECT 'AUDIT_LOG', COUNT(*) FROM audit_log;
```

## 22. Table structure: type, size, nullable ও default

```sql
SELECT table_name, column_id, column_name, data_type, data_length, nullable, data_default
FROM user_tab_columns ORDER BY table_name, column_id;
```

## 23. Primary / foreign / unique / check constraints

```sql
SELECT c.table_name, c.constraint_name, c.constraint_type, c.status,
       cc.column_name, c.r_constraint_name, c.search_condition
FROM user_constraints c LEFT JOIN user_cons_columns cc ON cc.constraint_name=c.constraint_name
ORDER BY c.table_name, c.constraint_name, cc.position;
```

## 24. Indexes ও sequences

```sql
SELECT table_name, index_name, uniqueness, status FROM user_indexes ORDER BY table_name, index_name;
SELECT index_name, column_position, column_name FROM user_ind_columns ORDER BY index_name, column_position;
SELECT sequence_name, increment_by, last_number FROM user_sequences ORDER BY sequence_name;
```

## 25. Trigger, procedure, function ও view status

```sql
SELECT object_name, object_type, status FROM user_objects
WHERE object_type IN ('TRIGGER','PROCEDURE','FUNCTION','VIEW') ORDER BY object_type, object_name;
SELECT trigger_name, table_name, triggering_event, status FROM user_triggers ORDER BY table_name, trigger_name;
```

## 26. Database-এ stored PL/SQL এবং view SQL

```sql
SELECT name, type, line, text FROM user_source ORDER BY name, type, line;
SELECT view_name, text FROM user_views ORDER BY view_name;
```

## 27. Compilation error ও invalid object

```sql
SELECT object_name, object_type, status FROM user_objects WHERE status='INVALID';
SELECT name, type, line, position, text FROM user_errors ORDER BY name, sequence;
```

## 28. Duplicate roll / registration: ঠিক থাকলে empty result

```sql
SELECT UPPER(TRIM(roll_no)) AS roll_no, COUNT(*) AS duplicates
FROM student WHERE roll_no IS NOT NULL GROUP BY UPPER(TRIM(roll_no)) HAVING COUNT(*)>1;
SELECT UPPER(TRIM(registration_no)) AS registration_no, COUNT(*) AS duplicates
FROM student WHERE registration_no IS NOT NULL GROUP BY UPPER(TRIM(registration_no)) HAVING COUNT(*)>1;
```

## 29. যাদের academic ID এখনও নেই

```sql
SELECT student_id, name, roll_no, registration_no FROM student
WHERE roll_no IS NULL OR registration_no IS NULL ORDER BY student_id;
```

## 30. Book stock mismatch: ঠিক থাকলে empty result

```sql
SELECT b.book_id, b.title, b.quantity, b.available_quantity, COUNT(i.issue_id) AS active_loans
FROM book b LEFT JOIN issue_book i ON i.book_id=b.book_id AND i.status='ISSUED'
GROUP BY b.book_id, b.title, b.quantity, b.available_quantity
HAVING b.available_quantity<>b.quantity-COUNT(i.issue_id);
```

## 31. Book availability function-এর output

```sql
SELECT check_book_available(1) AS book_1_availability FROM dual;
```

## Backend-এ ব্যবহৃত SQL templates: source অনুযায়ী

নিচে backend-এর সব SQL-containing string expression source locationসহ আছে, authentication, validation এবং write logic-সহ। এগুলো reference: Python f-string placeholders ও helper calls SQL editor-এ সরাসরি চালানো যায় না। SELECT ছাড়াও transaction/write template আছে; copy করে execute না করে সংশ্লিষ্ট endpoint ও source পড়ুন। `|` ও `~` frontend API serialization-এর জন্য।

### backend/auth/member_access.py:59

```python
f"SELECT user_id FROM login_user WHERE student_id={sid} AND user_type='STUDENT'"
```

### backend/auth/member_access.py:97

```python
f"SELECT user_id FROM login_user WHERE student_id={sid}"
```

### backend/auth/member_access.py:51

```python
f"BEGIN "
                        f"reset_student_password_proc({sid},{quote(roll)},{quote(registration)},{quote(phone)},{quote(email)},{quote(hash_password(data['password']))});"
                        f" COMMIT; END;\n/"
```

### backend/auth/member_access.py:92

```python
f"BEGIN activate_student_proc({sid},{quote(phone)},{quote(hash_password(data['password']))}); COMMIT; END;\n/"
```

### backend/auth/routes.py:215

```python
"SELECT user_id||'|'||account_status FROM login_user "
        f"WHERE user_id={user_id} AND user_type='LIBRARIAN'"
```

### backend/auth/routes.py:124

```python
"SELECT user_id||'|'||username||'|'||user_type||'|'||account_status "
            "FROM login_user WHERE user_type IN ('ADMIN','LIBRARIAN') "
            "ORDER BY DECODE(user_type,'ADMIN',1,2), username"
```

### backend/auth/routes.py:142

```python
"INSERT INTO login_user(username,password,user_type,account_status) "
            f"VALUES({quote(username)},{quote(hash_password(password))},'LIBRARIAN','ACTIVE')"
```

### backend/auth/routes.py:153

```python
"UPDATE login_user " f"SET account_status={quote(next_status)} WHERE user_id={user_id}"
```

### backend/auth/routes.py:163

```python
f"DELETE FROM login_user WHERE user_id={user_id}"
```

### backend/auth/routes.py:176

```python
f"SELECT password FROM login_user WHERE user_id={session['user_id']}"
```

### backend/auth/routes.py:185

```python
f"UPDATE login_user SET username={quote(username)}, "
            f"password={quote(hash_password(data['newPassword']))} "
            f"WHERE user_id={session['user_id']}"
```

### backend/auth/routes.py:51

```python
"SELECT user_id||'|'||username||'|'||user_type||'|'||account_status||'|'||password||'|'||NVL(TO_CHAR(student_id),'~') "
                "FROM login_user "
                f"WHERE {condition}"
```

### backend/auth/routes.py:206

```python
"SELECT COUNT(*) FROM login_user "
        f"WHERE LOWER(username)=LOWER({quote(username)}){exclusion}"
```

### backend/auth/routes.py:72

```python
f"SELECT membership_status FROM student WHERE student_id={user['student_id']}"
```

### backend/auth/routes.py:82

```python
f"UPDATE login_user SET password={quote(hash_password(data['password']))} WHERE user_id={user['user_id']}"
```

### backend/database.py:63

```python
f"BEGIN DBMS_APPLICATION_INFO.SET_CLIENT_INFO({quote(actor)}); END;\n/\n"
```

### backend/database.py:177

```python
f"{statement};\nCOMMIT;"
```

### backend/database.py:201

```python
"Only read-only SELECT statements can be batched"
```

### backend/reminders/store.py:35

```python
"SET SERVEROUTPUT ON\nDECLARE claimed NUMBER:=0; BEGIN\n"
        "BEGIN INSERT INTO reminder_delivery(event_key,issue_id,channel,status,attempts) "
        f"VALUES({key},{int(message['issue_id'])},{quote(message['channel'])},'SENDING',1); "
        "claimed:=1; EXCEPTION WHEN DUP_VAL_ON_INDEX THEN "
        "UPDATE reminder_delivery SET status='SENDING',attempts=attempts+1,updated_at=SYSDATE "
        f"WHERE event_key={key} AND status='FAILED' AND attempts<3 AND next_attempt<=SYSDATE; "
        "claimed:=SQL%ROWCOUNT; END; COMMIT; "
        "IF claimed=1 THEN DBMS_OUTPUT.PUT_LINE('CLAIMED'); END IF; END;\n/"
```

### backend/reminders/store.py:52

```python
f"UPDATE reminder_delivery SET status={quote(status)},provider_id={provider},"
        "updated_at=SYSDATE,next_attempt=SYSDATE+30/1440 "
        f"WHERE event_key={quote(key)} AND status='SENDING';\nCOMMIT;"
```

### backend/reminders/store.py:61

```python
"UPDATE reminder_delivery SET status='UNKNOWN',updated_at=SYSDATE "
        "WHERE status='SENDING' AND updated_at<SYSDATE-15/1440;\nCOMMIT;"
```

### backend/reminders/store.py:9

```python
"SELECT i.issue_id||'|'||i.student_id||'|'||REPLACE(s.name,'|',' ')||'|'||s.phone||'|'||s.email||'|'||"
        "REPLACE(b.title,'|',' ')||'|'||NVL(TO_CHAR(c.copy_no),'~')||'|'||"
        "TO_CHAR(i.due_date,'YYYY-MM-DD')||'|'||i.status||'|'||NVL(f.amount-f.paid_amount,0) "
        "FROM issue_book i JOIN student s ON s.student_id=i.student_id JOIN book b ON b.book_id=i.book_id "
        "LEFT JOIN book_copy c ON c.copy_id=i.copy_id LEFT JOIN fine f ON f.issue_id=i.issue_id "
        "WHERE i.due_date IS NOT NULL AND (i.status='ISSUED' OR f.amount>f.paid_amount)"
```

### backend/reservations.py:145

```python
f"""DECLARE v_student NUMBER; v_book NUMBER; v_copy NUMBER; v_lock NUMBER; v_status VARCHAR2(12); v_expires DATE;
BEGIN
  SELECT student_id,book_id INTO v_student,v_book FROM book_reservation WHERE reservation_id={rid}{restriction};
  SELECT student_id INTO v_lock FROM student WHERE student_id=v_student FOR UPDATE;
  SELECT book_id INTO v_lock FROM book WHERE book_id=v_book FOR UPDATE;
  SELECT copy_id,status,expires_at INTO v_copy,v_status,v_expires FROM book_reservation WHERE reservation_id={rid}{restriction} FOR UPDATE;
  IF v_status<>'ACTIVE' OR v_expires<=SYSDATE THEN RAISE_APPLICATION_ERROR(-20032,'This reservation is no longer active'); END IF;
  {action}
  COMMIT;
END;
/"""
```

### backend/reservations.py:21

```python
f"SELECT membership_status FROM student WHERE student_id={sid}"
```

### backend/reservations.py:143

```python
f"UPDATE book_reservation SET status='CANCELLED' WHERE reservation_id={rid};"
```

### backend/reservations.py:39

```python
"SELECT r.reservation_id||'|'||r.student_id||'|'||REPLACE(s.name,'|',' "
            "')||'|'||r.book_id||'|'||REPLACE(b.title,'|',' "
            "')||'|'||c.copy_no||'|'||TO_CHAR(r.reserved_at,'YYYY-MM-DD "
            "HH24:MI:SS')||'|'||TO_CHAR(r.expires_at,'YYYY-MM-DD HH24:MI:SS')||'|'||CASE WHEN "
            "r.status='ACTIVE' AND r.expires_at<=SYSDATE THEN 'EXPIRED' ELSE r.status END FROM "
            "book_reservation r JOIN student s ON s.student_id=r.student_id JOIN book b ON "
            "b.book_id=r.book_id JOIN book_copy c ON c.copy_id=r.copy_id"
```

### backend/reservations.py:83

```python
f"SELECT student_id||'|'||REPLACE(name,'|',' ')||'|'||NVL(roll_no,'~')||'|'||NVL(registration_no,'~') FROM student WHERE student_id={sid}"
```

### backend/reservations.py:128

```python
f"BEGIN reserve_book_proc({sid},{book_id}); COMMIT; END;\n/"
```

### backend/reservations.py:178

```python
f"SELECT password FROM login_user WHERE user_id={session['user_id']}"
```

### backend/reservations.py:183

```python
f"UPDATE login_user SET password={quote(hash_password(data['newPassword']))} WHERE user_id={session['user_id']};\nCOMMIT;"
```

### backend/routes/audit.py:51

```python
f"""SELECT audit_id||'|'||TO_CHAR(occurred_at,'YYYY-MM-DD"T"HH24:MI:SS.FF3"Z"')||'|'||
      RAWTOHEX(actor)||'|'||action||'|'||entity||'|'||record_id||'|'||
      NVL(RAWTOHEX(before_data),'~')||'|'||NVL(RAWTOHEX(after_data),'~')
    FROM (
      SELECT ordered_logs.*, ROWNUM AS row_number FROM (
        SELECT * FROM audit_log WHERE {where} ORDER BY audit_id DESC
      ) ordered_logs WHERE ROWNUM <= {last}
    ) WHERE row_number > {first}"""
```

### backend/routes/audit.py:48

```python
f"SELECT COUNT(*) FROM audit_log WHERE {where}"
```

### backend/routes/books.py:15

```python
f"SELECT d.book_id||'|'||REPLACE(d.title,'|',' ')||'|'||REPLACE(d.author_name,'|',' "
        f"')||'|'||REPLACE(d.category_name,'|',' ')||'|'||REPLACE(NVL(d.publisher,'~'),'|',' "
        f"')||'|'||d.quantity||'|'||(d.available_quantity-(SELECT COUNT(*) FROM book_reservation"
        f" r WHERE r.book_id=d.book_id AND r.status='ACTIVE' AND r.expires_at>SYSDATE)) FROM "
        f"book_details d WHERE LOWER(d.title||d.author_name||d.category_name) LIKE {search} "
        f"ORDER BY d.title"
```

### backend/routes/books.py:42

```python
f"""
DECLARE
  v_author_id author.author_id%TYPE;
  v_category_id category.category_id%TYPE;
  v_book_id book.book_id%TYPE;
BEGIN
  BEGIN
    SELECT author_id INTO v_author_id
    FROM author
    WHERE LOWER(author_name) = LOWER({quote(p['author'])});
  EXCEPTION WHEN NO_DATA_FOUND THEN
    INSERT INTO author(author_name) VALUES({quote(p['author'])})
    RETURNING author_id INTO v_author_id;
  END;

  BEGIN
    SELECT category_id INTO v_category_id
    FROM category
    WHERE LOWER(category_name) = LOWER({quote(p['category'])});
  EXCEPTION WHEN NO_DATA_FOUND THEN
    INSERT INTO category(category_name) VALUES({quote(p['category'])})
    RETURNING category_id INTO v_category_id;
  END;

  BEGIN
    SELECT book_id INTO v_book_id
    FROM book
    WHERE LOWER(TRIM(title)) = LOWER(TRIM({quote(p['title'])}))
      AND author_id = v_author_id
      AND category_id = v_category_id
    FOR UPDATE;

    UPDATE book
    SET quantity = quantity + {quantity},
        available_quantity = available_quantity + {quantity},
        publisher = {quote(p.get('publisher', 'PSTU Library'))}
    WHERE book_id = v_book_id;
  EXCEPTION WHEN NO_DATA_FOUND THEN
    INSERT INTO book(
      title, author_id, category_id, publisher, quantity, available_quantity
    ) VALUES(
      {quote(p['title'])}, v_author_id, v_category_id,
      {quote(p.get('publisher', 'PSTU Library'))}, {quantity}, {quantity}
    );
  END;
  COMMIT;
END;
/"""
```

### backend/routes/books.py:115

```python
f"""
DECLARE
  v_available book.available_quantity%TYPE;
BEGIN
  SELECT available_quantity INTO v_available
  FROM book
  WHERE book_id = {book_id}
  FOR UPDATE;

  IF {quantity} > v_available THEN
    RAISE_APPLICATION_ERROR(-20008, 'Only available copies can be removed from stock');
  END IF;

  UPDATE book
  SET quantity = quantity - {quantity},
      available_quantity = available_quantity - {quantity}
  WHERE book_id = {book_id};
  COMMIT;
END;
/"""
```

### backend/routes/books.py:99

```python
f"SELECT c.copy_id||'|'||c.copy_no||'|'||CASE WHEN EXISTS (SELECT 1 FROM "
            f"book_reservation r WHERE r.copy_id=c.copy_id AND r.status='ACTIVE' AND "
            f"r.expires_at>SYSDATE) THEN 'RESERVED' ELSE c.status END FROM book_copy c WHERE "
            f"c.book_id={book_id} AND c.status<>'RETIRED' ORDER BY c.copy_no"
```

### backend/routes/circulation.py:14

```python
"SELECT i.issue_id||'|'||i.student_id||'|'||i.book_id||'|'||REPLACE(s.name,'|',' "
        "')||'|'||REPLACE(b.title,'|',' "
        "')||'|'||TO_CHAR(i.issue_date,'YYYY-MM-DD')||'|'||NVL(TO_CHAR(i.due_date,'YYYY-MM-DD'),'~')||'|'||NVL(TO_CHAR(i.return_date,'YYYY-MM-DD'),'~')||'|'||i.status||'|'||NVL(TO_CHAR(c.copy_no),'~')||'|'||CASE"
        " WHEN i.status='ISSUED' THEN GREATEST(TRUNC(SYSDATE)-TRUNC(NVL(i.due_date,SYSDATE)),0)"
        " ELSE 0 END||'|'||CASE WHEN i.status='ISSUED' THEN "
        "GREATEST(TRUNC(SYSDATE)-TRUNC(NVL(i.due_date,SYSDATE)),0)*10 ELSE 0 END FROM "
        "issue_book i JOIN student s ON s.student_id=i.student_id JOIN book b ON "
        "b.book_id=i.book_id LEFT JOIN book_copy c ON c.copy_id=i.copy_id ORDER BY i.issue_date"
        " DESC, i.issue_id DESC"
```

### backend/routes/circulation.py:60

```python
"\n  COMMIT;\nEND;\n/"
```

### backend/routes/circulation.py:68

```python
f"BEGIN\n return_book_proc({issue_id});\n COMMIT;\nEND;\n/"
```

### backend/routes/circulation.py:60

```python
"BEGIN\n"
```

### backend/routes/fines.py:32

```python
"SELECT f.fine_id||'|'||i.issue_id||'|'||i.student_id||'|'||REPLACE(s.name,'|',' "
        "')||'|'||REPLACE(b.title,'|',' "
        "')||'|'||f.amount||'|'||f.payment_status||'|'||f.paid_amount||'|'||(f.amount-f.paid_amount)"
        " FROM fine f JOIN issue_book i ON i.issue_id=f.issue_id JOIN student s ON "
        "s.student_id=i.student_id JOIN book b ON b.book_id=i.book_id ORDER BY f.fine_id DESC"
```

### backend/routes/fines.py:74

```python
f"SELECT payment_id||'|'||amount||'|'||TO_CHAR(paid_at,'YYYY-MM-DD "
            f"HH24:MI:SS')||'|'||REPLACE(actor,'|',' ')||'|'||NVL(REPLACE(note,'|',' '),'~') FROM "
            f"fine_payment WHERE fine_id={fine_id} ORDER BY paid_at DESC,payment_id DESC"
```

### backend/routes/fines.py:19

```python
"SELECT (SELECT NVL(SUM(paid_amount),0) FROM fine)||'|'||"
        f"(SELECT NVL(SUM(amount),0) FROM fine_payment WHERE paid_at>={day} AND paid_at<{day}+1)||'|'||"
        f"(SELECT NVL(SUM(amount),0) FROM fine_payment WHERE paid_at>={month} AND paid_at<ADD_MONTHS({month},1)) "
        "FROM dual"
```

### backend/routes/fines.py:64

```python
f"BEGIN\n pay_fine_proc({fine_id}, NULL, {quote(note)});\n COMMIT;\nEND;\n/"
```

### backend/routes/members.py:20

```python
"SELECT student_id||'|'||REPLACE(name,'|',' ')||'|'||REPLACE(department,'|',' "
        "')||'|'||phone||'|'||REPLACE(email,'|',' "
        "')||'|'||membership_status||'|'||NVL(REPLACE(roll_no,'|',' "
        "'),'~')||'|'||NVL(REPLACE(registration_no,'|',' "
        "'),'~')||'|'||NVL(academic_session,'~') FROM student ORDER BY student_id DESC"
```

### backend/routes/members.py:52

```python
f"""
BEGIN
  add_student_proc(
    {quote(p['name'])},
    {quote(p['department'])},
    {quote(phone)},
    {quote(p['email'])},
    DBMS_RANDOM.STRING('X',30),
    {quote(p['roll_no'])},
    {quote(p['registration_no'])},
    {quote(p['academic_session'])}
  );
  COMMIT;
END;
/"""
```

### backend/routes/members.py:81

```python
f"""
DECLARE
  current_status student.membership_status%TYPE;
  active_loans NUMBER;
  unpaid_fines NUMBER;
BEGIN
  SELECT membership_status INTO current_status FROM student
  WHERE student_id = {student_id} FOR UPDATE;
  IF current_status = 'ACTIVE' AND {quote(status)} = 'DISABLED' THEN
    SELECT COUNT(*) INTO active_loans FROM issue_book
    WHERE student_id = {student_id} AND status = 'ISSUED';
    SELECT COUNT(*) INTO unpaid_fines FROM fine f
    JOIN issue_book i ON i.issue_id = f.issue_id
    WHERE i.student_id = {student_id} AND f.payment_status = 'UNPAID';
    IF active_loans > 0 THEN
      RAISE_APPLICATION_ERROR(-20003, 'Return all issued books before disabling membership');
    END IF;
    IF unpaid_fines > 0 THEN
      RAISE_APPLICATION_ERROR(-20004, 'Pay all fines before disabling membership');
    END IF;
  END IF;
  UPDATE student SET
    name = {quote(details['name'])}, department = {quote(details['department'])},
    phone = {quote(details['phone'])}, email = {quote(details['email'])},
    academic_session = {quote(details['academic_session'])},
    roll_no = {quote(details['roll_no'])}, registration_no = {quote(details['registration_no'])},
    membership_status = {quote(status)}
  WHERE student_id = {student_id};
  COMMIT;
END;
/"""
```

### backend/routes/members.py:141

```python
f"""
DECLARE
  v_status student.membership_status%TYPE;
  v_active_loans NUMBER;
  v_unpaid_fines NUMBER;
BEGIN
  SELECT membership_status INTO v_status
  FROM student
  WHERE student_id = {student_id}
  FOR UPDATE;

  IF v_status = 'ACTIVE' THEN
    SELECT COUNT(*) INTO v_active_loans
    FROM issue_book
    WHERE student_id = {student_id} AND status = 'ISSUED';

    SELECT COUNT(*) INTO v_unpaid_fines
    FROM fine f
    JOIN issue_book i ON i.issue_id = f.issue_id
    WHERE i.student_id = {student_id} AND f.payment_status = 'UNPAID';

    IF v_active_loans > 0 THEN
      RAISE_APPLICATION_ERROR(-20003, 'Return all issued books before disabling membership');
    END IF;
    IF v_unpaid_fines > 0 THEN
      RAISE_APPLICATION_ERROR(-20004, 'Pay all fines before disabling membership');
    END IF;
    UPDATE student SET membership_status = 'DISABLED' WHERE student_id = {student_id};
  ELSE
    UPDATE student SET membership_status = 'ACTIVE' WHERE student_id = {student_id};
  END IF;
  COMMIT;
END;
/"""
```

### backend/routes/members.py:125

```python
f"""
BEGIN
  UPDATE student
  SET roll_no = {quote(roll_no)}, registration_no = {quote(registration_no)}
  WHERE student_id = {student_id};
  IF SQL%ROWCOUNT = 0 THEN RAISE NO_DATA_FOUND; END IF;
  COMMIT;
END;
/"""
```

### backend/routes/members.py:47

```python
f"SELECT COUNT(*) FROM student WHERE phone = {quote(phone)};"
```

### backend/routes/pages.py:48

```python
"SELECT 1 FROM dual;"
```

### backend/routes/snapshot.py:17

```python
"SELECT author_id||'|'||REPLACE(author_name,'|',' ') FROM author ORDER BY author_name"
```

### backend/routes/snapshot.py:22

```python
"SELECT category_id||'|'||REPLACE(category_name,'|',' ') FROM category ORDER BY category_name"
```

### backend/setup_database.py:90

```python
f"VARIABLE {name} VARCHAR2(4000)\nBEGIN :{name} := '{escaped}'; END;\n/\n"
```

### backend/upgrade_circulation.py:12

```python
"SELECT name||':'||line||':'||text FROM user_errors ORDER BY name,sequence;"
```
