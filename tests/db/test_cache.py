from pathlib import Path

from ...libhansard.db.query_cache import QueryCache

def tests_query_cache():
    cache = QueryCache(Path(__file__).parent)
    
    query = cache.get_query("test").strip()

    assert query == "SELECT * FROM TEST"
