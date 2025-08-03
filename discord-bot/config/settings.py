import os
from dotenv import load_dotenv

load_dotenv()  # carga variables desde .env en la raíz

TOKEN = os.getenv("DISCORD_TOKEN")
ID = os.getenv("ID")
PUBLICKEY = os.getenv("PUBLICKEY")

BNCDDOS = os.getenv("BNCDDOS")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
