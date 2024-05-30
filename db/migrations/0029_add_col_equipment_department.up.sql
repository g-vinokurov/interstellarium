ALTER TABLE IF EXISTS equipment
    ADD COLUMN IF NOT EXISTS department_id INTEGER NULL;

ALTER TABLE IF EXISTS equipment
    DROP CONSTRAINT IF EXISTS equipment_department_fk,
    ADD CONSTRAINT equipment_department_fk
        FOREIGN KEY (department_id)
        REFERENCES departments (id)
        ON DELETE SET NULL
        ON UPDATE CASCADE;
