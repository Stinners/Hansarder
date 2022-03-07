WITH ins (debate_id, choice, party, mp) AS 
	( VALUES 
		(%(debate_id)s, %(choice)s, %(party)s, %(mp)s)
	)
INSERT INTO vote 
	(debate, choice, party, mp)
SELECT 
	ins.debate_id, ins.choice, party.id, member.id
FROM 
	ins LEFT JOIN party ON ins.party = party.name
	    LEFT JOIN member ON ins.mp = member.name;
