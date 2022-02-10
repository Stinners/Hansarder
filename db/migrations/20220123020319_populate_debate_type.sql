-- migrate:up
INSERT INTO debate_type (description)
VALUES 
    ('Karakia'),
    ('Questions'),
    ('Preamble'),
    ('Business Statement'),
    ('General Debate'),
    ('In Committee'),
    ('First Reading'),
    ('Second Reading'),
    ('Third Reading'),
    ('Urgent Debate'),
    ('Special Debate'),
    ('Points of Order'),
    ('Unknown');

-- migrate:down
DELETE FROM debate_type;
