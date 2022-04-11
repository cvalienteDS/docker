BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "EMPLOYEES" (
    "id" INTEGER,
    "employee_name" TEXT,
    "employee_salary" INTEGER,
    "employee_age" INTEGER,
    "profile_image" TEXT,
	PRIMARY KEY("id")
);

INSERT INTO "EMPLOYEES" ("id", "employee_name", "employee_salary", "employee_age", "profile_image")
VALUES (2,'Garrett Winters', 170750, 63, '');
COMMIT;