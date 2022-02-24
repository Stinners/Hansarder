select debate.id, debate.title, STRING_AGG(speech.html, '') as html from debate
join debate_type on debate.debate_type = debate_type.id
join speech on debate.id = speech.debate
where debate_type.description = %s
group by debate.id;
