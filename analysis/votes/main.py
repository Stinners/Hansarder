import sys
from pathlib import Path
from dataclasses import dataclass
from typing import List

sys.path.insert(1, str(Path(__file__).parent.parent.parent))

from libhansard.db.db import get_db 
from libhansard.db.query_cache import QueryCache

@dataclass
class Debate:
    id: int
    title: str
    debate_type: str
    html: str

pool = get_db()
conn = pool.getconn()

queries = QueryCache(Path(__file__).parent / "queries")

# TODO look into pycopg data factories
def get_debate_by_type(debate_type: str) -> List[Debate]:
    with conn.cursor() as cur:
        cur.execute(queries.get_query("get_debate_by_type"), (debate_type,))
        debate_rows = cur.fetchall()

        debates = [
            Debate(
                id = row[0],
                title = row[1],
                debate_type = debate_type,
                html = row[2],
            ) for row in debate_rows]
        return debates


