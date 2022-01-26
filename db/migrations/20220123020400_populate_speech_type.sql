-- migrate:up
INSERT INTO speech_type (description)
VALUES
    ('Speech'),
    ('Vote'),
    ('Question'),
    ('Unknown');

-- migrate:down
DELETE FROM speech_type;