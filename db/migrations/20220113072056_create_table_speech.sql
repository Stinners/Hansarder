-- migrate:up
CREATE TABLE IF NOT EXISTS speech (
    speech_id SERIAL PRIMARY KEY,
    topic TEXT, 
    html TEXT,
    debate_id INT,
    speaker_id INT,

    CONSTRAINT speaker_fk 
        FOREIGN KEY (speaker_id)
        REFERENCES member(member_id),

    CONSTRAINT debate_fk
        FOREIGN KEY (debate_id)
        REFERENCES debate(debate_id)
)


-- migrate:down
DROP TABLE IF EXISTS speech;
