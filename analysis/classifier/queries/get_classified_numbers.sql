select topic.description, count(*) from topic 
join debate_topic on topic.id = debate_topic.topic
group by topic.id;
