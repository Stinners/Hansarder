WITH ins (topic, member, html, speech_type, debate_id) AS
( VALUES 
    (%(topic)s, %(member)s, %(html)s, %(speech_type)s, %(debate_id)s)
)
INSERT INTO speech 
    (topic, member, html, speech_type, debate, position)
SELECT 
    ins.topic, member.id, ins.html, speech_type.id, ins.debate_id, %(position)s
FROM 
    ins 
    LEFT JOIN member ON ins.member ILIKE member.name
    LEFT JOIN speech_type ON ins.speech_type = speech_type.description;
