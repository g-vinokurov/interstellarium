CREATE TABLE IF NOT EXISTS assignments_equipment_group (
    id SERIAL NOT NULL,
    equipment_id INTEGER NOT NULL,
    group_id INTEGER NOT NULL,
    assignment_date DATE NULL,
    is_assigned BOOLEAN NULL,
    CONSTRAINT assignment_equipment_group_pk PRIMARY KEY (id),
    CONSTRAINT assignment_equipment_group_equipment_fk FOREIGN KEY(equipment_id)
        REFERENCES equipment (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT assignment_equipment_group_group_fk FOREIGN KEY(group_id)
        REFERENCES groups (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
