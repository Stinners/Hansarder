-- migrate:up
CREATE TABLE IF NOT EXISTS document (
    id serial PRIMARY KEY,
    title text NOT NULL UNIQUE, 
    url text NOT NULL UNIQUE,
    start_date date NOT NULL,
    continued_date date,
    UNIQUE(start_date, continued_date)
);

-- migrate:down
DROP TABLE document IF EXISTS;
