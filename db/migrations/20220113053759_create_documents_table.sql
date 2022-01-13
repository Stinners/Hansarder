-- migrate:up
CREATE TABLE IF NOT EXISTS document (
    document_id serial PRIMARY KEY,
    title text NOT NULL UNIQUE, 
    url text NOT NULL UNIQUE,
    start_date date NOT NULL,
    continued_date date
);

-- migrate:down
DROP TABLE document IF EXISTS;
