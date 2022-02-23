select count(distinct debate.id) 
from debate
join debate_topic on debate.id = debate_topic.debate;
