WITH ins AS (topic, speaker, html) 
( VALUES 
    (%s, %s, %s)
)
INSERT INTO speech 
    (topic, member_id, html)
SELECT 
    ins.topic, member.member_id, ins.html
FROM ins LEFT JOIN member 
ON ins.speaker ilike member.member_id; 
