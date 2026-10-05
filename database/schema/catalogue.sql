-- Book catalogue
CREATE TABLE author (author_id NUMBER PRIMARY KEY, author_name VARCHAR2(100) NOT NULL UNIQUE);
CREATE SEQUENCE author_seq START WITH 1 INCREMENT BY 1;
CREATE OR REPLACE TRIGGER author_trigger BEFORE INSERT ON author FOR EACH ROW
BEGIN
  IF :NEW.author_id IS NULL THEN
    SELECT author_seq.NEXTVAL INTO :NEW.author_id FROM dual;
  END IF;
END;
/

CREATE UNIQUE INDEX uq_author_name ON author(LOWER(TRIM(author_name)));

CREATE TABLE category (category_id NUMBER PRIMARY KEY, category_name VARCHAR2(100) NOT NULL UNIQUE);
CREATE SEQUENCE category_seq START WITH 1 INCREMENT BY 1;
CREATE OR REPLACE TRIGGER category_trigger BEFORE INSERT ON category FOR EACH ROW
BEGIN
  IF :NEW.category_id IS NULL THEN
    SELECT category_seq.NEXTVAL INTO :NEW.category_id FROM dual;
  END IF;
END;
/

CREATE UNIQUE INDEX uq_category_name ON category(LOWER(TRIM(category_name)));
CREATE UNIQUE INDEX uq_student_roll ON student(UPPER(TRIM(roll_no)));
CREATE UNIQUE INDEX uq_student_registration ON student(UPPER(TRIM(registration_no)));
CREATE UNIQUE INDEX uq_student_email ON student(LOWER(TRIM(email)));

CREATE TABLE book (
  book_id NUMBER PRIMARY KEY,
  title VARCHAR2(200) NOT NULL,
  author_id NUMBER NOT NULL REFERENCES author(author_id),
  category_id NUMBER NOT NULL REFERENCES category(category_id),
  publisher VARCHAR2(100),
  quantity NUMBER DEFAULT 0 NOT NULL CHECK (quantity >= 0),
  available_quantity NUMBER DEFAULT 0 NOT NULL,
  CONSTRAINT ck_book_availability
    CHECK (available_quantity >= 0 AND available_quantity <= quantity)
);
CREATE SEQUENCE book_seq START WITH 1 INCREMENT BY 1;
CREATE OR REPLACE TRIGGER book_trigger BEFORE INSERT ON book FOR EACH ROW
BEGIN
  IF :NEW.book_id IS NULL THEN
    SELECT book_seq.NEXTVAL INTO :NEW.book_id FROM dual;
  END IF;
END;
/
CREATE UNIQUE INDEX uq_book_identity
ON book(LOWER(TRIM(title)), author_id, category_id);

