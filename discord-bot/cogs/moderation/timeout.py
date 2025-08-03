# cogs/moderation/timeout.py

import discord
from discord.ext import commands
from discord import app_commands
from datetime import timedelta
import re

class Timeout(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="timeout", description="Silencia a un usuario por una duración personalizada.")
    @app_commands.describe(
        user="Usuario a silenciar",
        duration="Duración (ej: 30s, 10m, 2h, 1d)",
        reason="Razón del silencio"
    )
    async def timeout(self, interaction: discord.Interaction, user: discord.Member, duration: str, reason: str):
        if not interaction.user.guild_permissions.moderate_members:
            await interaction.response.send_message("🚫 No tienes permiso para aplicar timeout.", ephemeral=True)
            return

        if user == interaction.user:
            await interaction.response.send_message("❗ No puedes silenciarte a ti mismo.", ephemeral=True)
            return

        # Verificar jerarquía
        if user.top_role >= interaction.user.top_role and interaction.user != interaction.guild.owner:
            await interaction.response.send_message("⚠️ No puedes silenciar a alguien con un rol igual o superior al tuyo.", ephemeral=True)
            return

        if user.timed_out_until:
            await interaction.response.send_message("🔇 Este usuario ya está silenciado.", ephemeral=True)
            return

        # Interpretar duración
        match = re.fullmatch(r"(\d+)([smhd])", duration.lower())
        if not match:
            await interaction.response.send_message("❌ Formato de duración inválido. Usa `30s`, `10m`, `2h`, `1d`, etc.", ephemeral=True)
            return

        amount, unit = int(match[1]), match[2]
        if unit == "s":
            delta = timedelta(seconds=amount)
        elif unit == "m":
            delta = timedelta(minutes=amount)
        elif unit == "h":
            delta = timedelta(hours=amount)
        elif unit == "d":
            delta = timedelta(days=amount)
        else:
            await interaction.response.send_message("❌ Unidad de tiempo no válida.", ephemeral=True)
            return

        try:
            await user.timeout(delta, reason=reason)
        except discord.Forbidden:
            await interaction.response.send_message("❌ No tengo permisos para aplicar timeout a ese usuario.", ephemeral=True)
            return
        except Exception as e:
            await interaction.response.send_message(f"❌ Error al aplicar timeout: {e}", ephemeral=True)
            return

        embed = discord.Embed(
            title="⏳ Timeout aplicado",
            color=discord.Color.dark_blue()
        )
        embed.add_field(name="👤 Usuario", value=user.mention, inline=True)
        embed.add_field(name="🕒 Duración", value=f"{amount}{unit}", inline=True)
        embed.add_field(name="📄 Razón", value=reason, inline=False)
        embed.set_footer(text=f"Aplicado por {interaction.user}", icon_url=interaction.user.display_avatar.url)

        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Timeout(bot))
