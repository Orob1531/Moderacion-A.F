# cogs/moderation/unmute.py

import discord
from discord.ext import commands
from discord import app_commands

class Unmute(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="unmute", description="Quitar el mute de un usuario.")
    @app_commands.describe(user="Usuario al que deseas quitar el mute")
    async def unmute(self, interaction: discord.Interaction, user: discord.Member):
        # Verificar permisos del moderador
        if not interaction.user.guild_permissions.moderate_members:
            await interaction.response.send_message("🚫 No tienes permisos para quitar el mute.", ephemeral=True)
            return

        # Verificar si está muteado
        if not user.timed_out_until:
            await interaction.response.send_message("✅ Este usuario no está muteado.", ephemeral=True)
            return

        # Quitar mute
        try:
            await user.edit(timed_out_until=None, reason=f"Unmute por {interaction.user}")
        except discord.Forbidden:
            await interaction.response.send_message("❌ No tengo permisos para quitar el mute a ese usuario.", ephemeral=True)
            return
        except Exception as e:
            await interaction.response.send_message(f"❌ Error al quitar mute: {e}", ephemeral=True)
            return

        # Embed de respuesta
        embed = discord.Embed(
            title="🔊 Mute retirado",
            description=f"{user.mention} ya puede hablar nuevamente.",
            color=discord.Color.green()
        )
        embed.set_footer(text=f"Acción realizada por {interaction.user}", icon_url=interaction.user.display_avatar.url)

        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Unmute(bot))
