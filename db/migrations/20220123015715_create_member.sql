-- migrate:up
CREATE TABLE IF NOT EXISTS member (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    party INT,

    CONSTRAINT party_fk 
        FOREIGN KEY (party)
        REFERENCES party(id)
)

-- migrate:down
DROP TABLE IF EXISTS member;

