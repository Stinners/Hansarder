
from functools import cache
import pathlib 
import logging

# TODO there is currently no way to invalidate the cache other than 
# restarting the app 

class QueryCache:
    def __init__(self, directory_path):
        self.base_dir = pathlib.Path(directory_path) 

    @cache
    def get_query(self, query_name):
        query_path = self.base_dir / (query_name + ".sql")
        logging.debug(f"Loading query: {query_path}")

        try:
            with open (query_path, 'r') as f:
                not_comment = [line for line in f.readlines() if not line.strip().startswith("--")]
                query = "\n".join(not_comment)
                return query
        except:
            logging.error(f"Couldn't read query #{query_path}")
            exit()



