# This file contains a list of regexs and their coresponding debate types 

class DebateTypes:
    exact_matches: dict[str, str] = {
        "Karakia/Prayers": "Karakia",
        "Oral Questions — Questions to Ministers": "Questions",
        "Petitions, Papers, Select Committee Reports, and Introduction of Bills": "Preamble",
        "Business Statement": "Business Statement",
        "General Debate": "General Debate"
    }

    starts_with: dict[str, str] = {
        "Speaker's Ruling": "Speaker's Ruling"
    }

    contains: dict[str, str] = {
        "— In Committee—": "In Committee",
        "First Reading": "First Reading",
        "Second Reading": "Second Reading",
        "Third Reading": "Third Reading", 
        "Urgent Debate": "Urgent Debate",
        "Special Debate": "Special Debate",
        "Points of Order": "Points of Order",
    }

    # This currently isn't used 
    #__regexs: dict[str, str] = {}
    ## Compile all the regexes just once
    #regex: dict[Pattern, str] = {re.compile(key): value for key, value in __regexs.items()}

def all_types():
    return list(DebateTypes.exact_matches.values()) + list(DebateTypes.contains.values()) + ["Unknown"]



