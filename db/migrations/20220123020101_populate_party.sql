-- migrate:up
INSERT INTO party (name)
    VALUES 
        ('Labour'),
        ('National'),
        ('Green'),
        ('ACT'),
        ('Māori');

-- migrate:down
DELETE FROM party;