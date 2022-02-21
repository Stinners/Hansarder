-- using order by random isn't ideal here 
-- since it requires sorting the whole table
-- but if the table gets big enough that it's a problem 
-- it'll be big enough to use statistical sampling
-- realistically that's probably tens of thousands of rows
SELECT 
    debate.id, 
    debate.title,
    string_agg(speech.html, '' order by speech."position") 
from debate 
left join debate_topic on debate_topic.debate = debate.id
inner join speech on speech.debate = debate.id
where debate_topic.debate is null
  and debate.debate_type != 1  -- karakia 
  and debate.debate_type != 3  -- preamble 
  and debate.debate_type != 12 -- point of order
group by debate.id
order by Random()
limit 1;
