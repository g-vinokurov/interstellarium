CREATE TABLE IF NOT EXISTS assignments_equipment_department (
    id SERIAL NOT NULL,
    equipment_id INTEGER NOT NULL,
    department_id INTEGER NOT NULL,
    assignment_date DATE NULL,
    is_assigned BOOLEAN NULL,
    CONSTRAINT assignment_equipment_department_pk PRIMARY KEY (id),
    CONSTRAINT assignment_equipment_department_equipment_fk FOREIGN KEY(equipment_id)
        REFERENCES equipment (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT assignment_equipment_department_department_fk FOREIGN KEY(department_id)
        REFERENCES departments (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
