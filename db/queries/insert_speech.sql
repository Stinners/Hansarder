WITH ins AS (topic, speaker, html, debate_type) 
( VALUES 
    (%(topic)s, %(speaker)s, %(html)s, %(debate_type))
)
INSERT INTO speech 
    (topic, member_id, html, debate_type_id)
SELECT 
    ins.topic, member.member_id, ins.html, debate_type.debate_type_id
FROM 
    ins 
    LEFT JOIN member ON ins.speaker ILIKE member.member_id; 
    LEFT JOIN debate_type ON ins.debate_type = debate_type.description;
