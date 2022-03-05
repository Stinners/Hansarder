-- migrate:up
-- migrate:up
CREATE TABLE IF NOT EXISTS vote (
    id SERIAL PRIMARY KEY NOT NULL,
    choice BOOL NOT NULL,
    party INT,
    mp INT,
    CONSTRAINT mp_xor_party check ((mp NOTNULL and party ISNULL) or
                                   (party NOTNULL and mp ISNULL)),
    CONSTRAINT party_fk 
    	FOREIGN KEY (party)
    	REFERENCES party(id),
    CONSTRAINT mp_fk
    	FOREIGN KEY (mp)
    	REFERENCES member(id)
)
-- migrate:down
DROP TABLE vote;

