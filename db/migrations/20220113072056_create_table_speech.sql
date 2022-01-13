-- migrate:up
CREATE TABLE IF NOT EXISTS speech (
    speech_id SERIAL PRIMARY KEY,
    topic TEXT, 
    speaker_id INT,
    html TEXT,

    CONSTRAINT speaker_fk 
        FOREIGN KEY (speaker_id)
        REFERENCES minister(minister_id)
)


-- migrate:down
DROP TABLE IF EXISTS speech;
