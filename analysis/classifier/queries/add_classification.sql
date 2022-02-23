-- TODO this is probably better done using a pl/pgsql function 
-- learn how to do that 
INSERT INTO debate_topic (debate, topic, certanty, hand_classified)
( 
    SELECT %(debate_id)s, topic.id, %(certanty)s, true
    FROM topic 
    WHERE topic.description = %(topic)s
    LIMIT 1
);
