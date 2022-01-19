-- migrate:up
CREATE TABLE IF NOT EXISTS speech (
    speech_id SERIAL PRIMARY KEY,
    topic TEXT, 
    speaker_id INT,
    html TEXT,
    type_id INT,

    CONSTRAINT speaker_fk 
        FOREIGN KEY (speaker_id)
        REFERENCES member(member_id)
)


-- migrate:down
DROP TABLE IF EXISTS speech;
