-- migrate:up
CREATE TABLE IF NOT EXISTS debate_type (
    debate_type_id serial PRIMARY KEY,
    debate_type text NOT NULL UNIQUE
);

-- migrate:down
DROP TABLE IF EXISTS debate_type;
