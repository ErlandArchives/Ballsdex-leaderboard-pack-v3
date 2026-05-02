import discord
from discord import app_commands, Embed, Color
from discord.ext import commands
from bd_models.models import Player
from django.db.models import Count, Q
from ballsdex.core.bot import BallsDexBot
from ballsdex.settings import settings
from asgiref.sync import sync_to_async
from ballsdex.core.utils.transformers import (
    BallEnabledTransform,
)


class Leaderboard(commands.Cog):
    """
    Leaderboard command :skull:
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="leaderboard", description=f"Shows the top players of {settings.bot_name}!")
    async def leaderboard(self, interaction: discord.Interaction["BallsDexBot"], economy: bool = False, ephemeral: bool = False, amount: int = 10, collectible: BallEnabledTransform | None = None,):
        """
        Displays the most addicted i mean best players of this dex
        """
        await interaction.response.defer(ephemeral=ephemeral, thinking=True)

        if economy:
            if not settings.currency_name:
                await interaction.followup.send("Currency is __not__ enabled on this bot.")
                return
        
        if not economy:
            if not collectible:
                players = await sync_to_async(
                    lambda: list(
                        Player.objects.annotate(ball_count=Count("balls")).order_by("-ball_count")[:amount]
                    )
                )()
            else:
                players = await sync_to_async(
                    lambda: list(
                        Player.objects.annotate(ball_count=Count("balls", filter=Q(balls__ball=collectible))).order_by("-ball_count")[:amount]
                    )
                )()  
        else:
            players = await sync_to_async(
                lambda: list(
                    Player.objects.order_by("-money")[:amount]
                )
            )()

        if not players:
            await interaction.followup.send("No players found.", ephemeral=True)
            return
        if not collectible:
            embed = discord.Embed(
                title=f"Top {amount} players of {settings.bot_name}",
                color=discord.Color.gold()
            )
        else:
            embed = discord.Embed(
                title=f"Top {amount} players that have {collectible}",
                color=discord.Color.gold()
            )
        text = ""
        if economy == False:
            if not collectible:
                for i, player in enumerate(players, start=1):
                    user = self.bot.get_user(player.discord_id) or await self.bot.fetch_user(player.discord_id)
                    text += f"**{i}. {user.name}** {settings.plural_collectible_name}: {player.ball_count}\n"
            else:
                for i, player in enumerate(players, start=1):
                    user = self.bot.get_user(player.discord_id) or await self.bot.fetch_user(player.discord_id)
                    text += f"**{i}. {user.name}** {collectible}(s): {player.ball_count}\n"
        else:
            for i, player in enumerate(players, start=1):
                user = self.bot.get_user(player.discord_id) or await self.bot.fetch_user(player.discord_id)
                if settings.currency_symbol_before == True:
                    text += f"**{i}. {user.name}** {settings.currency_symbol}{player.money}\n"
                else:
                    text += f"**{i}. {user.name}** {player.money}{settings.currency_symbol}\n"

        embed.description = text
        embed.set_footer(text="Made by @unitedstatesoferland")
        embed.set_thumbnail(url=interaction.user.display_avatar.url)

        await interaction.followup.send(embed=embed)



