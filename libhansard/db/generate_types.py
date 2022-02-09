

if __name__ == "__main__" and __package__ is None:
    import sys, os
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(1, parent_dir)
    __package__ = str("db")

from scraper import debate_types

deb_types = [f"('{debate_type}')" for debate_type in debate_types.all_types()] + ["Unknown"]
values_string = ",\n    ".join(deb_types)

query = f"""
INSERT INTO debate_type (debate_type)
VALUES 
    {values_string};
"""

print(query)
