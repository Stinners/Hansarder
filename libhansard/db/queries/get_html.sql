SELECT id, title, debate_type, STRING_AGG
FROM debate 
INNER JOIN speech ON debate.id = speech.debate
WHERE debate.id = %(debate_id)s;

