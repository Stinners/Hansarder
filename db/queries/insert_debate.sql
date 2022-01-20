WITH ins (title, debate_type, document_id) AS 
    ( VALUES 
        (%(title)s, %(debate_type)s, %(document_id)s)
    )
INSERT INTO debate 
    (title, debate_type, document)
SELECT 
    ins.title, debate_type.debate_type_id, ins.document_id 
FROM 
    ins JOIN debate_type
    ON ins.debate_type = debate_type.debate_type;
