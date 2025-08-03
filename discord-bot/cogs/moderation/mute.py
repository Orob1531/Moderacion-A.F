# cogs/moderation/mute.py

import discord
from discord.ext import commands
from discord import app_commands
from datetime import timedelta

class Mute(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="mute", description="Silencia a un usuario por un tiempo con una razón.")
    @app_commands.describe(user="Usuario a mutear", duration="Duración en minutos", reason="Razón del muteo")
    async def mute(self, interaction: discord.Interaction, user: discord.Member, duration: int, reason: str):
        # Verificar permisos del moderador
        if not interaction.user.guild_permissions.moderate_members:
            await interaction.response.send_message("🚫 No tienes permisos para mutear usuarios.", ephemeral=True)
            return

        # Evitar autocomandos
        if user.id == interaction.user.id:
            await interaction.response.send_message("❗ No puedes mutearte a ti mismo.", ephemeral=True)
            return

        # Verificar jerarquía
        if user.top_role >= interaction.user.top_role and interaction.user != interaction.guild.owner:
            await interaction.response.send_message("⚠️ No puedes mutear a alguien con rol igual o superior al tuyo.", ephemeral=True)
            return

        # Verificar si ya está muteado
        if user.timed_out_until:
            await interaction.response.send_message("🔇 Este usuario ya está muteado.", ephemeral=True)
            return

        # Aplicar mute
        try:
            await user.timeout(timedelta(minutes=duration), reason=reason)
        except discord.Forbidden:
            await interaction.response.send_message("❌ No tengo permisos para mutear a ese usuario.", ephemeral=True)
            return
        except Exception as e:
            await interaction.response.send_message(f"❌ Error al aplicar mute: {e}", ephemeral=True)
            return

        # Embed de respuesta
        embed = discord.Embed(
            title="🔇 Usuario silenciado",
            color=discord.Color.dark_orange()
        )
        embed.add_field(name="👤 Usuario", value=f"{user.mention}", inline=True)
        embed.add_field(name="🕒 Duración", value=f"{duration} minutos", inline=True)
        embed.add_field(name="📄 Razón", value=reason, inline=False)
        embed.set_footer(text=f"Silenciado por {interaction.user}", icon_url=interaction.user.display_avatar.url)

        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Mute(bot))
