import pytest 
import dotenv 
import sys
import os
import subprocess
from pathlib import Path

sys.path.insert(1, str(Path(__file__).parent.parent.parent))

from libhansard.db.db import get_db
from tests.util.test_set import insert_test_set
from analysis.votes.main import *

###################################################################
#                         Fixtures                                #
###################################################################

@pytest.fixture(autouse=True)
def set_env_test():
    # Set the current environment to test 
    dotenv.load_dotenv(".env_test")

    assert os.getenv("ENV") == "TEST", "Failed to set environment variable"

    # Initiate the testing database, making sure it wasn't already there
    subprocess.call(["dbmate", "-e", "TEST_DATABASE_URL", "drop"], stdout=subprocess.DEVNULL)
    subprocess.call(["dbmate", "-e", "TEST_DATABASE_URL", "up"], stdout=subprocess.DEVNULL)

    # Setup the test set
    pool = get_db()
    insert_test_set(pool.getconn())
    pool.close()

    # Run the test
    yield 

    # Drop the test database after the test 
    subprocess.call(["dbmate", "-e", "TEST_DATABASE_URL", "drop"], stdout=subprocess.DEVNULL)

###################################################################
#                         Tests                                   #
###################################################################

# Note the test set had the 'Contraception, Sterilisation, and Abortion (Safe Areas) Amendment Bill — Second Reading'
# which was not whipped - make sure to write a test based on this

# The Maritime powers bill -second reading, which was interupted - so there was no vote

# Cases: Examples
#   - Split Vote: 'Contraception, Sterilisation, and Abortion (Safe Areas) Amendment Bill — Second Reading'
#   - Debate Interupted: 'The Maritime powers bill - Second reading'
#   - Unanimous vote: 'Gambling (Reinstating COVID-19 Modification) Amendment Bill — Third Reading'
#   - Votes listed multiple times: 'Land Transport (Clean Vehicles) Amendment Bill — Second Reading'
#   - Full Conscience vote: 'End of Life Choice Bill — Third Reading'
#                           Will need to add to the test set
#                           https://www.parliament.nz/en/pb/hansard-debates/rhr/combined/HansDeb_20191113_20191113_16

def test_get_debates():
    pool = get_db()
    debates = get_debates_by_type("Third Reading", pool.getconn())

    assert len(debates) == 21
    assert all(["Third Reading" in debate.title for debate in debates])

# A case where a vote is called and there are parties on either side
# This reading was on Tuesday 14th Dec 2021
# docs[8].debates[1].title
def test_normal_reading():
    pool = get_db()
    debates = get_debates_by_type("First Reading", pool.getconn())
    debate = next(debate for debate in debates if debate.title == 'Oranga Tamariki Amendment Bill — First Reading')

    vote_type, votes = parse_debate(debate)

    assert vote_type == VoteType.PARTY
    assert votes == [
        Vote("New Zealand Labour", 65, VoteChoice.AYE),
        Vote("Green Party of Aotearoa New Zealand", 10, VoteChoice.AYE),
        Vote("ACT New Zealand", 10, VoteChoice.AYE),
        Vote("New Zealand National", 33, VoteChoice.NAY)
    ]
