-- migrate:up
CREATE TABLE IF NOT EXISTS party (
    id serial PRIMARY KEY,
    name text UNIQUE NOT NULL
)

-- migrate:down
DROP TABLE IF EXISTS party;

