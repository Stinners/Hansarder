-- migrate:up
CREATE TABLE IF NOT EXISTS topic (
    id SERIAL PRIMARY KEY,
    description text NOT NULL
)

-- migrate:down
DROP TABLE topic;

