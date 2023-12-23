from dbutils import *
from dotenv import load_dotenv
from os import getenv
load_dotenv()
dbpath = getenv("DBPATH")

conn = create_connection(dbpath)