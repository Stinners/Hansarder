-- migrate:up
CREATE TABLE IF NOT EXISTS speech_type (
    id SERIAL PRIMARY KEY,
    description TEXT UNIQUE NOT NULL
)

-- migrate:down
DROP TABLE speech_type;
