import os
from dotenv import load_dotenv

load_dotenv()

DEBUG = os.getenv("DEBUG") == "1"
SITE_HOST = os.getenv("SITE_HOST", "127.0.0.1")
MONGO_HOST = os.getenv("MONGO_HOST", "mongo")
AMQP_URI = os.getenv("AMQP_URI")
AMQP_PORT = os.getenv("AMQP_PORT")
UNIQUE_PREFIX = os.getenv("UNIQUE_PREFIX")
