"""Build readable SQL references from the project's database and backend sources."""

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parents[1]


def block(sql):
    return "```sql\n" + sql.strip() + "\n```\n"


QUERIES = [
    ("Connection ও Oracle সময়", "SELECT 1 AS connection_ok, SYSDATE AS database_time FROM dual;"),
    (
        "Dashboard: বই, কপি, member ও active loan",
        "SELECT (SELECT COUNT(*) FROM book) AS book_titles,\n       (SELECT NVL(SUM(quantity),0) FROM book) AS total_copies,\n       (SELECT NVL(SUM(available_quantity),0) FROM book) AS available_copies,\n       (SELECT COUNT(*) FROM student WHERE membership_status='ACTIVE') AS active_members,\n       (SELECT COUNT(*) FROM issue_book WHERE status='ISSUED') AS active_loans\nFROM dual;",
    ),
    ("বইয়ের পুরো board", "SELECT * FROM book_details ORDER BY title;"),
    (
        "বই খোঁজা: Clean এর জায়গায় নিজের search লিখুন",
        "SELECT * FROM book_details\nWHERE LOWER(title||author_name||category_name) LIKE '%clean%' ORDER BY title;",
    ),
    (
        "সব member: roll ও registration সহ",
        "SELECT student_id, name, department, phone, email, membership_status, roll_no, registration_no, academic_session\nFROM student ORDER BY student_id;",
    ),
    (
        "Member 1 এর details",
        "SELECT student_id, name, department, phone, email, membership_status, roll_no, registration_no, academic_session\nFROM student WHERE student_id=1;",
    ),
    (
        "Roll / registration দিয়ে member খোঁজা",
        "SELECT student_id, name, roll_no, registration_no, membership_status\nFROM student WHERE UPPER(TRIM(roll_no))='2300001' OR UPPER(TRIM(registration_no))='11700';",
    ),
    (
        "Author ও category",
        "SELECT author_id, author_name FROM author ORDER BY author_name;\nSELECT category_id, category_name FROM category ORDER BY category_name;",
    ),
    (
        "Issue ও return history: frontend-এর একই overdue হিসাব",
        "SELECT i.issue_id, s.student_id, s.name, s.roll_no, s.registration_no,\n       b.book_id, b.title, i.issue_date, i.due_date, i.return_date, i.status,\n       CASE WHEN i.status='ISSUED' THEN GREATEST(TRUNC(SYSDATE)-TRUNC(NVL(i.due_date,SYSDATE)),0) ELSE 0 END AS overdue_days,\n       CASE WHEN i.status='ISSUED' THEN GREATEST(TRUNC(SYSDATE)-TRUNC(NVL(i.due_date,SYSDATE)),0)*10 ELSE 0 END AS current_fine\nFROM issue_book i JOIN student s ON s.student_id=i.student_id\nJOIN book b ON b.book_id=i.book_id ORDER BY i.issue_date DESC, i.issue_id DESC;",
    ),
    (
        "বর্তমানে issued বই",
        "SELECT i.issue_id, s.name, s.roll_no, b.title, i.issue_date, i.due_date\nFROM issue_book i JOIN student s ON s.student_id=i.student_id\nJOIN book b ON b.book_id=i.book_id WHERE i.status='ISSUED' ORDER BY i.due_date;",
    ),
    (
        "শুধু overdue: return করার আগের estimated fine",
        "SELECT i.issue_id, s.name, s.roll_no, s.registration_no, b.title, i.due_date,\n       GREATEST(TRUNC(SYSDATE)-TRUNC(i.due_date),0) AS overdue_days,\n       GREATEST(TRUNC(SYSDATE)-TRUNC(i.due_date),0)*10 AS estimated_fine\nFROM issue_book i JOIN student s ON s.student_id=i.student_id\nJOIN book b ON b.book_id=i.book_id\nWHERE i.status='ISSUED' AND TRUNC(i.due_date)<TRUNC(SYSDATE) ORDER BY i.due_date;",
    ),
    (
        "Return board এবং return-এর সময়ের fine",
        "SELECT r.return_id, i.issue_id, s.name, s.roll_no, b.title,\n       i.due_date, r.return_date, r.fine_amount, r.status, f.payment_status\nFROM return_book r JOIN issue_book i ON i.issue_id=r.issue_id\nJOIN student s ON s.student_id=i.student_id JOIN book b ON b.book_id=i.book_id\nLEFT JOIN fine f ON f.issue_id=i.issue_id ORDER BY r.return_id DESC;",
    ),
    (
        "Fine history: paid ও unpaid",
        "SELECT f.fine_id, i.issue_id, s.student_id, s.name, s.roll_no, s.registration_no,\n       b.title, i.return_date, f.amount, f.payment_status\nFROM fine f JOIN issue_book i ON i.issue_id=f.issue_id\nJOIN student s ON s.student_id=i.student_id JOIN book b ON b.book_id=i.book_id\nORDER BY f.fine_id DESC;",
    ),
    (
        "শুধু unpaid fine",
        "SELECT f.fine_id, s.name, b.title, f.amount, i.return_date\nFROM fine f JOIN issue_book i ON i.issue_id=f.issue_id\nJOIN student s ON s.student_id=i.student_id JOIN book b ON b.book_id=i.book_id\nWHERE f.payment_status='UNPAID' ORDER BY f.fine_id DESC;",
    ),
    (
        "Fine section-এর total: double counting বাদ দিয়ে",
        "SELECT recorded_unpaid, overdue_estimate, recorded_unpaid+overdue_estimate AS total_outstanding\nFROM (SELECT\n (SELECT NVL(SUM(amount),0) FROM fine WHERE payment_status='UNPAID') AS recorded_unpaid,\n (SELECT NVL(SUM(GREATEST(TRUNC(SYSDATE)-TRUNC(NVL(i.due_date,SYSDATE)),0)*10),0)\n  FROM issue_book i WHERE i.status='ISSUED'\n  AND NOT EXISTS (SELECT 1 FROM fine f WHERE f.issue_id=i.issue_id)) AS overdue_estimate\n FROM dual);",
    ),
    (
        "Member 1-এর loan ও unpaid fine: issue/disable validation",
        "SELECT COUNT(*) AS active_loans FROM issue_book WHERE student_id=1 AND status='ISSUED';\nSELECT COUNT(*) AS unpaid_fines, NVL(SUM(f.amount),0) AS unpaid_amount\nFROM fine f JOIN issue_book i ON i.issue_id=f.issue_id\nWHERE i.student_id=1 AND f.payment_status='UNPAID';",
    ),
    (
        "Accounts board: password বাদ দিয়ে",
        "SELECT user_id, username, user_type, account_status FROM login_user ORDER BY user_id;\nSELECT admin_id, name, email FROM admin ORDER BY admin_id;",
    ),
    (
        "Audit: সর্বশেষ 25টি change ও before/after",
        "SELECT * FROM (SELECT audit_id, occurred_at, actor, action, entity, record_id, before_data, after_data\nFROM audit_log ORDER BY audit_id DESC) WHERE ROWNUM<=25;",
    ),
    (
        "এক member-এর সব audit",
        "SELECT audit_id, occurred_at, actor, action, before_data, after_data\nFROM audit_log WHERE entity='STUDENT' AND record_id=1 ORDER BY audit_id DESC;",
    ),
    (
        "Audit filter এবং action count",
        "SELECT audit_id, occurred_at, actor, action, entity, record_id\nFROM audit_log WHERE action='UPDATE' ORDER BY audit_id DESC;\nSELECT entity, action, COUNT(*) AS event_count FROM audit_log GROUP BY entity, action ORDER BY entity, action;",
    ),
    (
        "সব table-এর row count",
        "SELECT 'ADMIN' AS table_name, COUNT(*) AS row_count FROM admin\nUNION ALL SELECT 'STUDENT', COUNT(*) FROM student\nUNION ALL SELECT 'AUTHOR', COUNT(*) FROM author\nUNION ALL SELECT 'CATEGORY', COUNT(*) FROM category\nUNION ALL SELECT 'BOOK', COUNT(*) FROM book\nUNION ALL SELECT 'ISSUE_BOOK', COUNT(*) FROM issue_book\nUNION ALL SELECT 'RETURN_BOOK', COUNT(*) FROM return_book\nUNION ALL SELECT 'FINE', COUNT(*) FROM fine\nUNION ALL SELECT 'LOGIN_USER', COUNT(*) FROM login_user\nUNION ALL SELECT 'AUDIT_LOG', COUNT(*) FROM audit_log;",
    ),
    (
        "Table structure: type, size, nullable ও default",
        "SELECT table_name, column_id, column_name, data_type, data_length, nullable, data_default\nFROM user_tab_columns ORDER BY table_name, column_id;",
    ),
    (
        "Primary / foreign / unique / check constraints",
        "SELECT c.table_name, c.constraint_name, c.constraint_type, c.status,\n       cc.column_name, c.r_constraint_name, c.search_condition\nFROM user_constraints c LEFT JOIN user_cons_columns cc ON cc.constraint_name=c.constraint_name\nORDER BY c.table_name, c.constraint_name, cc.position;",
    ),
    (
        "Indexes ও sequences",
        "SELECT table_name, index_name, uniqueness, status FROM user_indexes ORDER BY table_name, index_name;\nSELECT index_name, column_position, column_name FROM user_ind_columns ORDER BY index_name, column_position;\nSELECT sequence_name, increment_by, last_number FROM user_sequences ORDER BY sequence_name;",
    ),
    (
        "Trigger, procedure, function ও view status",
        "SELECT object_name, object_type, status FROM user_objects\nWHERE object_type IN ('TRIGGER','PROCEDURE','FUNCTION','VIEW') ORDER BY object_type, object_name;\nSELECT trigger_name, table_name, triggering_event, status FROM user_triggers ORDER BY table_name, trigger_name;",
    ),
    (
        "Database-এ stored PL/SQL এবং view SQL",
        "SELECT name, type, line, text FROM user_source ORDER BY name, type, line;\nSELECT view_name, text FROM user_views ORDER BY view_name;",
    ),
    (
        "Compilation error ও invalid object",
        "SELECT object_name, object_type, status FROM user_objects WHERE status='INVALID';\nSELECT name, type, line, position, text FROM user_errors ORDER BY name, sequence;",
    ),
    (
        "Duplicate roll / registration: ঠিক থাকলে empty result",
        "SELECT UPPER(TRIM(roll_no)) AS roll_no, COUNT(*) AS duplicates\nFROM student WHERE roll_no IS NOT NULL GROUP BY UPPER(TRIM(roll_no)) HAVING COUNT(*)>1;\nSELECT UPPER(TRIM(registration_no)) AS registration_no, COUNT(*) AS duplicates\nFROM student WHERE registration_no IS NOT NULL GROUP BY UPPER(TRIM(registration_no)) HAVING COUNT(*)>1;",
    ),
    (
        "যাদের academic ID এখনও নেই",
        "SELECT student_id, name, roll_no, registration_no FROM student\nWHERE roll_no IS NULL OR registration_no IS NULL ORDER BY student_id;",
    ),
    (
        "Book stock mismatch: ঠিক থাকলে empty result",
        "SELECT b.book_id, b.title, b.quantity, b.available_quantity, COUNT(i.issue_id) AS active_loans\nFROM book b LEFT JOIN issue_book i ON i.book_id=b.book_id AND i.status='ISSUED'\nGROUP BY b.book_id, b.title, b.quantity, b.available_quantity\nHAVING b.available_quantity<>b.quantity-COUNT(i.issue_id);",
    ),
    (
        "Book availability function-এর output",
        "SELECT check_book_available(1) AS book_1_availability FROM dual;",
    ),
]


def main():
    queries = [
        "# Project queries: output ও verification\n",
        "এই query-গুলো Oracle SQLPlus/SQL Developer-এ project schema দিয়ে চালাতে হবে। এখানে শুধু SELECT আছে; existing data পরিবর্তন হবে না। ID 1 এবং search text নিজের প্রয়োজনমতো বদলাতে পারবেন। Output-এর column নাম query-তেই দেওয়া আছে; live result সময় ও data অনুযায়ী বদলাবে।\n",
        "SQLPlus-এ বড় output দেখতে আগে:\n"
        + block(
            "SET LINESIZE 250\nSET PAGESIZE 100\nSET LONG 100000\nSET LONGCHUNKSIZE 100000\nSET DEFINE OFF"
        ),
        "Fine নিয়ম: 14 দিনের loan; overdue প্রতি calendar day 10 টাকা। Active overdue amount estimate; return-এর পরে fine table-এ recorded amount থাকে। Audit time UTC। Sequence LAST_NUMBER cached allocation দেখাতে পারে, পরের ID-এর নিশ্চয়তা নয়।\n",
    ]
    for index, (title, sql) in enumerate(QUERIES, 1):
        queries.append(f"## {index}. {title}\n\n" + block(sql))
    queries.append(
        "## Backend-এ ব্যবহৃত SQL templates: source অনুযায়ী\n\nনিচে backend-এর সব SQL-containing string expression source locationসহ আছে, authentication, validation এবং write logic-সহ। এগুলো reference: Python f-string placeholders ও helper calls SQL editor-এ সরাসরি চালানো যায় না। SELECT ছাড়াও transaction/write template আছে; copy করে execute না করে সংশ্লিষ্ট endpoint ও source পড়ুন। `|` ও `~` frontend API serialization-এর জন্য।\n"
    )
    for path in sorted((ROOT / "backend").rglob("*.py")):
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source)
        parents = {child: node for node in ast.walk(tree) for child in ast.iter_child_nodes(node)}
        for node in ast.walk(tree):
            if not isinstance(node, (ast.Constant, ast.JoinedStr)):
                continue
            if isinstance(parents.get(node), (ast.JoinedStr, ast.FormattedValue)):
                continue
            text = ast.get_source_segment(source, node) or ""
            value = (
                node.value
                if isinstance(node, ast.Constant) and isinstance(node.value, str)
                else text if isinstance(node, ast.JoinedStr) else ""
            )
            if not any(
                token in value.upper()
                for token in (
                    "SELECT ",
                    "INSERT INTO ",
                    "UPDATE ",
                    "DELETE FROM ",
                    "BEGIN",
                    "ALTER ",
                    "COMMIT;",
                    "ROLLBACK;",
                )
            ):
                continue
            queries.append(
                f"### {path.relative_to(ROOT).as_posix()}:{node.lineno}\n\n```python\n{text}\n```\n"
            )
    (OUT / "queries.md").write_text("\n".join(queries), encoding="utf-8")
    code = [
        "# Complete fresh database SQL\n",
        "bootstrap creates the Oracle account. setup is the ordered entry point for schema modules, feature upgrades, audit objects and sample records. Schema modules are not standalone upgrades. Use Setup-Database.bat only when you intend to reset the data; use backend.upgrade_circulation for an existing installation.\n",
    ]
    sources = sorted(
        path for path in (ROOT / "database").rglob("*.sql") if "backups" not in path.parts
    )
    for path in sources:
        name = path.relative_to(ROOT / "database").as_posix()
        code.append(
            f"## database/{name}\n\nSource: [মূল ফাইল](../../database/{name})\n\n"
            + block(path.read_text(encoding="utf-8"))
        )
    (OUT / "database-full-code.md").write_text("\n".join(code), encoding="utf-8")
    print(
        f"Created two references with {len(QUERIES)} output-query sections and {len(sources)} SQL source files."
    )


if __name__ == "__main__":
    main()
