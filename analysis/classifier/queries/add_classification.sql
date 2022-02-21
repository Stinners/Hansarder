-- TODO this is probably better done using a pl/pgsql function 
-- learn how to do that 
INSERT INTO debate_topic (debate, topic, certanty)
( 
    SELECT %(debate_id)s, topic.id, %(certanty)s
    FROM topic 
    WHERE topic.description = %(topic)s
    LIMIT 1
);
