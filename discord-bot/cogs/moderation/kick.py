# cogs/moderation/kick.py

import discord
from discord.ext import commands
from discord import app_commands

class Kick(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="kick", description="Expulsa a un usuario del servidor.")
    @app_commands.describe(user="Usuario a expulsar", reason="Razón de la expulsión")
    async def kick(self, interaction: discord.Interaction, user: discord.Member, reason: str = "No se proporcionó una razón"):
        # Verificar permisos del moderador
        if not interaction.user.guild_permissions.kick_members:
            await interaction.response.send_message("🚫 No tienes permiso para expulsar usuarios.", ephemeral=True)
            return

        # Evitar autokick
        if user.id == interaction.user.id:
            await interaction.response.send_message("❗ No puedes expulsarte a ti mismo.", ephemeral=True)
            return

        # Verificar jerarquía
        if user.top_role >= interaction.user.top_role and interaction.user != interaction.guild.owner:
            await interaction.response.send_message("⚠️ No puedes expulsar a alguien con un rol igual o superior al tuyo.", ephemeral=True)
            return

        if user.top_role >= interaction.guild.me.top_role:
            await interaction.response.send_message("⚠️ No puedo expulsar a este usuario. Mi r_
