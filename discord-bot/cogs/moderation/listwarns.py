# cogs/moderation/listwarns.py

import discord
from discord.ext import commands
from discord import app_commands
from utils.supabase import get_warns

class ListWarns(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="listwarns", description="Ver advertencias activas de un usuario.")
    @app_commands.describe(user="Usuario a revisar (opcional)")
    async def listwarns(self, interaction: discord.Interaction, user: discord.Member = None):
        await interaction.response.defer(ephemeral=True)  # Carga mientras obtiene los datos

        target_user_id = str(user.id) if user else None
        guild_id = str(interaction.guild_id)

        try:
            warns = get_warns(guild_id=guild_id, user_id=target_user_id)
        except Exception as e:
            await interaction.followup.send(f"❌ Error al obtener advertencias: {e}", ephemeral=True)
            return

        if not warns:
            await interaction.followup.send("✅ No se encontraron advertencias.", ephemeral=True)
            return

        # Crear Embed
        embed = discord.Embed(
            title="📋 Lista de Advertencias",
            color=discord.Color.red()
        )

        for warn in warns:
            usuario = f"<@{warn['user_id']}>"
            moderador = f"<@{warn['moderator_id']}>"
            razon = warn["reason"]
            embed.add_field(
                name=f"👤 {usuario}",
                value=f"🛡️ Moderador: {moderador}\n📄 Razón: {razon}",
                inline=False
            )

        await interaction.followup.send(embed=embed, ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(ListWarns(bot))
