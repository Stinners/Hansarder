-- migrate:up
CREATE TABLE IF NOT EXISTS debate_type (
    id SERIAL PRIMARY KEY,
    description TEXT UNIQUE NOT NULL
)

-- migrate:down
DROP TABLE speech_type;
