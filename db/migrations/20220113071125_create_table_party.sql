-- migrate:up
CREATE TABLE IF NOT EXISTS party (
    party_id serial PRIMARY KEY,
    name text NOT NULL
)

-- migrate:down
DROP TABLE IF EXISTS party;

