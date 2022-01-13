-- migrate:up
CREATE TABLE IF NOT EXISTS debate (
    debate_id serial PRIMARY KEY,
    title text NOT NULL,
    debate_type INT,
    document INT NOT NULL,
    CONSTRAINT debate_type_fk
        FOREIGN KEY (debate_type)
        REFERENCES debate_type(debate_type_id),
    CONSTRAINT document_type_fk 
        FOREIGN KEY (document)
        REFERENCES document(document_id)
)

-- migrate:down
DROP TABLE IF EXISTS debate;

