import discord
import datetime
import dateutil.parser
from discord import app_commands
from discord.ext import commands
from webserver import keep_alive
import os

token = os.environ['token']

client = commands.Bot(command_prefix="¿", intents=discord.Intents.all())

@client.event
async def on_ready():
    print("bot is ready as {0.user}".format(client))
    try:
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

def get_discord_since_text(user):
    created_at = dateutil.parser.parse(str(user.created_at))
    created_at = created_at.replace(tzinfo=None)
    now = datetime.datetime.now()
    discord_since = now - created_at
    return f"{discord_since.days} Tagen"

def get_month_name(month):
    months = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]
    return months[month - 1]

@client.tree.command(name="view")
@app_commands.describe(username = "@everyone")
async def view(interaction: discord.Interaction, username: discord.User):
    user = username
    server = interaction.guild
    embed = discord.Embed(
        color = 0x738adb,
        timestamp=datetime.datetime.utcnow(),
        title=f"**__Informationen über {user.name}__**"
    )

    embed.set_footer(text=server.name, icon_url=server.icon.url if server.icon else discord.Embed.Empty)
    embed.set_thumbnail(url=user.display_avatar.url)
  
    embed.add_field(name="Client-ID", value=user.id, inline=False)
    embed.add_field(name="", value="", inline=False)
  
    joined_at = user.joined_at.strftime("%d.%m.%Y")
    joined_at_parts = joined_at.split(".")
    joined_at_parts[1] = get_month_name(int(joined_at_parts[1]))
    joined_at_str = " ".join(joined_at_parts)
  
    embed.add_field(name="Mitglied seit", value=joined_at_str, inline=True)
    embed.add_field(name="", value="", inline=True)
  
    embed.add_field(name="Benutzt Discord seit", value=get_discord_since_text(user), inline=True)
    embed.add_field(name="", value="", inline=False)

    roles = user.roles
    if len(roles) > 1:  # Überprüfung, ob der Benutzer Rollen hat (außer @everyone)
        roles_text = ", ".join(role.name for role in roles if role.name != "@everyone")
    else:
        roles_text = "*Noch keine Rollen*"

    embed.add_field(name="Rollen", value=roles_text, inline=False)
    embed.add_field(name="", value="", inline=False)
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

keep_alive()

client.run(token)
