ALTER TABLE IF EXISTS contracts
    ADD COLUMN IF NOT EXISTS finish_date DATE NULL;
