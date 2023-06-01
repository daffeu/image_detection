import os

from dotenv import load_dotenv

load_dotenv()

DEBUG = os.getenv("DEBUG") == "1"
AMQP_URI = os.getenv("AMQP_URI")
AMQP_PORT = os.getenv("AMQP_PORT")
UNIQUE_PREFIX = os.getenv("UNIQUE_PREFIX")
VK_TOKEN = os.getenv("VK_TOKEN")
