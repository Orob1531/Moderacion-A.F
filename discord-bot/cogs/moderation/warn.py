# cogs/moderation/warn.py

import discord
from discord.ext import commands
from discord import app_commands
from utils.supabase import add_warn
from database import add_warn


class Warn(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="warn", description="Advertir a un usuario con una razón.")
    @app_commands.describe(user="Usuario a advertir", reason="Razón de la advertencia")
    async def warn(self, interaction: discord.Interaction, user: discord.Member, reason: str):
        # Verificar permisos
        if not interaction.user.guild_permissions.ban_members:
            await interaction.response.send_message(
                "🚫 No tienes permisos para usar este comando.", ephemeral=True)
            return

        # Evitar autoadvertencias
        if user.id == interaction.user.id:
            await interaction.response.send_message(
                "❗ No puedes advertirte a ti mismo.", ephemeral=True)
            return

        # Insertar en Supabase
        try:
            add_warn(
                user_id=str(user.id),
                guild_id=str(interaction.guild_id),
                moderator_id=str(interaction.user.id),
                reason=reason
            )
        except Exception as e:
            await interaction.response.send_message(f"❌ Error al guardar la advertencia: {e}", ephemeral=True)
            return

        # Enviar mensaje embed
        embed = discord.Embed(
            title="⚠️ Usuario Advertido",
            color=discord.Color.orange()
        )
        embed.add_field(name="👤 Usuario", value=f"{user.mention} (`{user.id}`)", inline=False)
        embed.add_field(name="🛡️ Moderador", value=f"{interaction.user.mention}", inline=False)
        embed.add_field(name="📄 Razón", value=reason, inline=False)

        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Warn(bot))
