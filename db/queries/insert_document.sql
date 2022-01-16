INSERT INTO document (title, url, start_date, continued_date) 
VALUES (%s, %s, %s, %s)
RETURNING document_id;
