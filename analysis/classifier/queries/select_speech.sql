-- Using orderby random isn't ideal here 
-- since it requires sorting the whole table
-- but if the table gets big enough that it's a problem 
-- it'll be big enough to use statistical sampling
-- Realistically that's probably tens of thousands of rows
SELECT id, debate, speech_type, html
FROM speech 
JOIN speech_topic ON speech.id = speech_topic.speech
WHERE speech_topic.topic IS NULL
ORDER BY RANDOM()
LIMIT 1
