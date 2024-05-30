ALTER TABLE IF EXISTS equipment
    DROP CONSTRAINT IF EXISTS equipment_department_fk,
    DROP COLUMN IF EXISTS department_id;
