-- migrate:up
CREATE TABLE IF NOT EXISTS debate (
    id serial PRIMARY KEY,
    title text NOT NULL,
    debate_type INT,
    document INT NOT NULL,

    CONSTRAINT debate_type_fk
        FOREIGN KEY (debate_type)
        REFERENCES debate_type(id),

    CONSTRAINT document_fk 
        FOREIGN KEY (document)
        REFERENCES document(id)
)

-- migrate:down
DROP TABLE IF EXISTS debate;