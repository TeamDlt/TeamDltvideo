import os
from os import getenv
from dotenv import load_dotenv

if os.path.exists("local.env"):
    load_dotenv("local.env")

load_dotenv()
admins = {}
SESSION_NAME = getenv("SESSION_NAME", "session")
BOT_TOKEN = getenv("BOT_TOKEN")
BOT_NAME = getenv("BOT_NAME", "Video Stream")
API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")
SOURCE_CODE = getenv("SOURCE_CODE")
OWNER_NAME = getenv("OWNER_NAME", "somyajeet_mishra")
ALIVE_NAME = getenv("ALIVE_NAME", "TeamDlt")
BOT_USERNAME = getenv("BOT_USERNAME", "Somyajeet_Afk_VideoBot")
ASSISTANT_NAME = getenv("ASSISTANT_NAME", "Somyajeet_Afk_Video_Assistant")
SUPPORT_GROUP = getenv("GROUP_SUPPORT", "TeamDlt")
UPDATES_CHANNEL = getenv("UPDATES_CHANNEL", "Teamdlt_update")
SUDO_USERS = list(map(int, getenv("SUDO_USERS").split()))
COMMAND_PREFIXES = list(getenv("COMMAND_PREFIXES", "/ ! .").split())
ALIVE_IMG = getenv("ALIVE_IMG", "https://te.legra.ph/file/fb35577fb0098e0ea14c3.jpg")
DURATION_LIMIT = int(getenv("DURATION_LIMIT", "190"))
IMG_1 = getenv("IMG_1", "https://te.legra.ph/file/67e93cd10c81636188c67.jpg")
IMG_2 = getenv("IMG_2", "https://te.legra.ph/file/8d92face1dd0607f60c96.jpg")
IMG_3 = getenv("IMG_3", "https://te.legra.ph/file/42cd463ca520a59b81d4f.jpg")
