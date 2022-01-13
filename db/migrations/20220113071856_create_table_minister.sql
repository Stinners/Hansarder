-- migrate:up
CREATE TABLE IF NOT EXISTS minister (
    minister_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    party_id INT,

    CONSTRAINT party_fk 
        FOREIGN KEY (party_id)
        REFERENCES party(party_id)
)

-- migrate:down
DROP TABLE IF EXISTS miniser;

