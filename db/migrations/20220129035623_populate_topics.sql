-- migrate:up
INSERT INTO topic (description)
VALUES 
    ('Art'),
    ('Education'),
    ('Finance'),
    ('Māori Development'),
    ('Treaty of Waitangi Negotiations'),
    ('Children'),
    ('Housing'),
    ('Environment'),
    ('Health'),
    ('Social Development'),
    ('Disability Issues'),
    ('Research, Science and Inovation'),
    ('Energy and Resources'),
    ('Infrastructure'),
    ('Oceans and Fisheries'),
    ('Agriculture'),
    ('Economic and Regional Development'),
    ('Justice'),
    ('Broadcasting and Media'),
    ('Climate'),
    ('Transport'),
    ('Digital Economy and Communication'),
    ('Women'),
    ('Tourism'),
    ('Foreign Affairs');

-- migrate:down
DELETE FROM topic;

