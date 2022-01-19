-- migrate:up
ALTER TABLE speech
    ADD COLUMN speech_type_id INT,
    ADD CONSTRAINT speech_type_fk
        FOREIGN KEY (speech_type_id)
        REFERENCES speech_type(speech_type_id);

-- migrate:down
ALTER TABLE speech
    DROP COLUMN speech_type_id,
    DROP CONSTRAINT speech_type_fk;
