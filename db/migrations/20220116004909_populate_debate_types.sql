-- migrate:up
INSERT INTO debate_type (debate_type)
VALUES 
    ('Karakia/Prayers'),
    ('Oral Questions — Questions to Ministers'),
    ('Petitions, Papers, Select Committee Reports, and Introduction of Bills'),
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
