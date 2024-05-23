ALTER TABLE IF EXISTS designers
    DROP CONSTRAINT IF EXISTS designer_user_unique,
    ADD CONSTRAINT designer_user_unique UNIQUE (user_id);

ALTER TABLE IF EXISTS engineers
    DROP CONSTRAINT IF EXISTS engineer_user_unique,
    ADD CONSTRAINT engineer_user_unique UNIQUE (user_id);

ALTER TABLE IF EXISTS technicians
    DROP CONSTRAINT IF EXISTS technician_user_unique,
    ADD CONSTRAINT technician_user_unique UNIQUE (user_id);

ALTER TABLE IF EXISTS laboratorians
    DROP CONSTRAINT IF EXISTS laboratorian_user_unique,
    ADD CONSTRAINT laboratorian_user_unique UNIQUE (user_id);

ALTER TABLE IF EXISTS departments
    DROP CONSTRAINT IF EXISTS department_leader_unique,
    ADD CONSTRAINT department_leader_unique UNIQUE (leader_id);
