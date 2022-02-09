INSERT INTO document (title, url, start_date, continued_date) 
VALUES (%(title)s, %(url)s, %(start_date)s, %(continued_date)s)
RETURNING id;
