-- migrate:up
CREATE TABLE IF NOT EXISTS speech (
    id SERIAL PRIMARY KEY,
    topic TEXT, 
    html TEXT,
    debate INT,
    member INT,
    speech_type INT,

    CONSTRAINT member_fk 
        FOREIGN KEY (member)
        REFERENCES member(id),

    CONSTRAINT debate_fk
        FOREIGN KEY (debate)
        REFERENCES debate(id),

    CONSTRAINT speech_type_fk
        FOREIGN KEY (speech_type)
        REFERENCES speech_type(id)
)


-- migrate:down
DROP TABLE IF EXISTS speech;
