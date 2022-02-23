-- migrate:up
CREATE TABLE IF NOT EXISTS debate_topic (
    debate INT NOT NULL,
    topic INT,
    certanty FLOAT NOT NULL CHECK (certanty BETWEEN 0 AND 1),
    hand_classified BOOLEAN NOT NULL,
    PRIMARY KEY(debate, topic),

    CONSTRAINT debate_topic_debate_fk
        FOREIGN KEY (debate)
        REFERENCES debate(id),

    CONSTRAINT debate_topic_topic_fk
        FOREIGN KEY (topic)
        REFERENCES topic(id)
)

-- migrate:down
DROP TABLE IF EXISTS speech_topic;

