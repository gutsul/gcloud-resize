from dotenv import load_dotenv, find_dotenv
from os import getenv

load_dotenv(find_dotenv())

PROJECT_ID = getenv("PROJECT_ID")
FREE_LIMIT_PERCENT = getenv("FREE_LIMIT_PERCENT")
RESIZE_PERCENT = getenv("RESIZE_PERCENT")
SLACK_URL = getenv("SLACK_URL")
SLACK_USERS = getenv("SLACK_USERS")

