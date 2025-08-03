# cogs/moderation/unwarn.py

import discord
from discord.ext import commands
from discord import app_commands
from utils.supabase import delete_last_warn

class Unwarn(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="unwarn", description="Eliminar la última advertencia de un usuario.")
    @app_commands.describe(user="Usuario al que deseas quitarle una advertencia")
    async def unwarn(self, interaction: discord.Interaction, user: discord.Member):
        if not interaction.user.guild_permissions.ban_members:
            await interaction.response.send_message("🚫 No tienes permiso para usar este comando.", ephemeral=True)
            return

        guild_id = str(interaction.guild_id)
        user_id = str(user.id)

        success = delete_last_warn(guild_id, user_id)

        if success:
            embed = discord.Embed(
                title="✅ Advertencia eliminada",
                description=f"La última advertencia de {user.mention} ha sido eliminada.",
                color=discord.Color.green()
            )
        else:
            embed = discord.Embed(
                title="❌ Sin advertencias",
                description=f"{user.mention} no tiene advertencias activas.",
                color=discord.Color.orange()
            )

        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Unwarn(bot))
