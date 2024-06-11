ALTER TABLE IF EXISTS works
    ADD COLUMN IF NOT EXISTS executor_id INTEGER NULL;

ALTER TABLE IF EXISTS works
    DROP CONSTRAINT IF EXISTS work_executor_fk,
    ADD CONSTRAINT work_executor_fk
        FOREIGN KEY (executor_id)
        REFERENCES groups (id)
        ON DELETE SET NULL
        ON UPDATE CASCADE;
