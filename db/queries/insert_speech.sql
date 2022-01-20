WITH ins AS (topic, speaker, html, debate_type, debate_id) 
( VALUES 
    (%(topic)s, %(speaker)s, %(html)s, %(debate_type), %(debate_id)s)
)
INSERT INTO speech 
    (topic, member_id, html, debate_type_id, debate_id)
SELECT 
    ins.topic, member.member_id, ins.html, debate_type.debate_type_id, ins.debate_id
FROM 
    ins 
    LEFT JOIN member ON ins.speaker ILIKE member.member_id; 
    LEFT JOIN debate_type ON ins.debate_type = debate_type.description;
