import sys

# This function takes a party name and converts it to the format stored in the DB 
# Hopefull a lookup table will be good enough 
# otherwise will probably need to do fuzzy matching
party_names = {
    "Labour": "Labour",
    "New Zealand Labour": "Labour",

    "Green": "Green",
    "Green Party of Aotearoa New Zealand": "Green",

    "ACT": "ACT",
    "ACT New Zealand": "ACT",

    "Māori": "Māori",
    "Te Paati Māori": "Māori",

    "National": "National",
    "New Zealand National": "National",
}


def normalize_party_name(name):
    try: 
        return party_names[name]
    except:
        sys.exit(f"Couldn't find party name {name}")

