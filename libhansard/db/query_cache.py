
from functools import cache
import pathlib 
import sys
import logging

# TODO there is currently no way to invalidate the cache other than 
# restarting the app 

class QueryCache:
    def __init__(self, directory_path):
        self.base_dir = pathlib.Path(directory_path) 

    @cache
    def get_query(self, query_name):
        query_path = self.base_dir / (query_name + ".sql")

        try:
            return query_path.read_text()
        except:
            logging.error(f"Couldn't read query #{query_path}")
            exit()



