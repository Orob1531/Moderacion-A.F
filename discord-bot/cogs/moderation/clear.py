# cogs/moderation/clear.py

import discord
from discord.ext import commands
from discord import app_commands

class Clear(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="clear", description="Elimina mensajes del canal actual.")
    @app_commands.describe(amount="Cantidad de mensajes a eliminar (por defecto: 1)")
    async def clear(self, interaction: discord.Interaction, amount: int = 1):
        # Verificar permisos
        if not interaction.user.guild_permissions.manage_messages:
            await interaction.response.send_message("🚫 No tienes permisos para eliminar mensajes.", ephemeral=True)
            return

        if not interaction.guild.me.guild_permissions.manage_messages:
            await interaction.response.send_message("❌ No tengo permisos para eliminar mensajes en este canal.", ephemeral=True)
            return

        if amount < 1 or amount > 100:
            await interaction.response.send_message("⚠️ El número debe estar entre 1 y 100.", ephemeral=True)
            return

        try:
            deleted = await interaction.channel.purge(limit=amount)
        except Exception as e:
            await interaction.response.send_message(f"❌ Error al eliminar mensajes: {e}", ephemeral=True)
            return

        embed = discord.Embed(
            title="🧹 Mensajes eliminados",
            description=f"Se eliminaron {len(deleted)} mensajes en {interaction.channel.mention}.",
            color=discord.Color.blurple()
        )
        embed.set_footer(text=f"Solicitado por {interaction.user}", icon_url=interaction.user.display_avatar.url)

        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Clear(bot))
