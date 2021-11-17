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
OWNER_NAME = getenv("OWNER_NAME", "piroXpower")
ALIVE_NAME = getenv("ALIVE_NAME", "VideoPlayer")
BOT_USERNAME = getenv("BOT_USERNAME", "VcVideoRoBot")
ASSISTANT_NAME = getenv("ASSISTANT_NAME", "Decode_Assistant")
SUPPORT_GROUP = getenv("GROUP_SUPPORT", "DeCodeSupport")
UPDATES_CHANNEL = getenv("UPDATES_CHANNEL", "DeecodeBots")
SUDO_USERS = list(map(int, getenv("SUDO_USERS").split()))
COMMAND_PREFIXES = list(getenv("COMMAND_PREFIXES", "/ ! .").split())
ALIVE_IMG = getenv("ALIVE_IMG", "https://te.legra.ph/file/3230fb4f2943318939118.jpg")
DURATION_LIMIT = int(getenv("DURATION_LIMIT", "190"))
IMG_1 = getenv("IMG_1", "https://telegra.ph/file/1fd52c8ef99566ca72159.jpg")
IMG_2 = getenv("IMG_2", "https://telegra.ph/file/4af38b52cace997702028.jpg")
IMG_3 = getenv("IMG_3", "https://telegra.ph/file/94eb8c66a7436d0890c75.jpg")
