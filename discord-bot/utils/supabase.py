# utils/db.py
from postgrest import PostgrestClient
from config.settings import SUPABASE_URL, SUPABASE_KEY

client = PostgrestClient(f"{SUPABASE_URL}/rest/v1/")
client.auth(SUPABASE_KEY)

def add_warn(user_id, guild_id, mod_id, reason):
    client.table("warns").insert({
        "user_id": user_id,
        "guild_id": guild_id,
        "moderator_id": mod_id,
        "reason": reason
    }).execute()

# utils/supabase.py

def get_warns(guild_id: str, user_id: str = None):
    query = client.table("warns").select("*").eq("guild_id", guild_id)
    if user_id:
        query = query.eq("user_id", user_id)
    data = query.execute().data
    return data

def delete_last_warn(guild_id: str, user_id: str):
    try:
        # Obtener las advertencias del usuario ordenadas por creación
        result = client.table("warns") \
            .select("*") \
            .eq("guild_id", guild_id) \
            .eq("user_id", user_id) \
            .order("id", desc=True) \
            .limit(1) \
            .execute()

        data = result.data
        if not data:
            return False

        warn_id = data[0]["id"]
        client.table("warns").delete().eq("id", warn_id).execute()
        return True
    except Exception as e:
        print(f"[ERROR unwarn] {e}")
        return False

