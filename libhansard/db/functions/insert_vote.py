from psycopg import Cursor, Connection

from typing import Optional, List
import pathlib

from ..query_cache import QueryCache
from ...vote_types import *
from ...util import normalize_party_name

QUERY_DIRECTORY = pathlib.Path(__file__).parent.parent / "queries" 

cache = QueryCache(QUERY_DIRECTORY)

def insert_votes(votes: List[Vote], debate_id: int, conn: Connection):

    vote_parameters = [{
        "debate": debate_id,
        "choice": vote.choice == VoteChoice.AYE,
        "party": normalize_party_name(vote.voter) if vote.vote_type == VoteType.PARTY else None,
        "mp": vote.voter if vote.vote_type == VoteType.CONSCIENCE else None,
    } for vote in votes]

    with conn.cursor() as cur:
        cur.executemany(
            cache.get_query("insert_votes"),
            vote_parameters
        )
    conn.commit()
    
