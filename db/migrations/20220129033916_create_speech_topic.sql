-- migrate:up
CREATE TABLE IF NOT EXISTS speech_topic (
    speech INT NOT NULL,
    topic INT NOT NULL,
    certanty FLOAT NOT NULL CHECK (certanty BETWEEN 0 AND 1),

    CONSTRAINT speech_topic_speech_fk
        FOREIGN KEY (speech)
        REFERENCES speech(id),

    CONSTRAINT speech_topic_topic_fk
        FOREIGN KEY (topic)
        REFERENCES topic(id)
)

-- migrate:down
DROP TABLE IF EXISTS speech_topic;

