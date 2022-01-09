# This file contains a list of regexs and their coresponding debate types 

class DebateTypes:
    exact_matches: dict[str, str] = {
        "Karakia/Prayers": "Karakia",
        "Oral Questions — Questions to Ministers": "Questions",
        "Petitions, Papers, Select Committee Reports, and Introduction of Bills": "Preamble",
        "Business Statement": "Business Statement",
        "General Debate": "General Debate"
    }

    contains: dict[str, str] = {
        "In Committee": "Committee",
        "First Reading": "First Reading",
        "Second Reading": "Second Reading",
        "Third Reading": "Third Reading",
        "Urgent Debate": "Urgent Debate",
        "Special Debate —": "Special Debate",
        "Points of Order": "Points of Order",
    }


# This currently isn't used 
#__regexs: dict[str, str] = {}

#regex: dict[Pattern, str] = {re.compile(key): value for key, value in __regexs.items()}

