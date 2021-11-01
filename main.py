import discord
import asyncio
import random
from discord.ext import commands
import datetime



token = ("NzcwNjUzMTcxMDQyMjIyMDgw.X5gssg.kZAt1X8eCiRyslT7KFj4JDF0aQo")

client = commands.Bot(command_prefix=["*", "+"])
client.remove_command("help")

start_time = datetime.datetime.utcnow()


@client.command(aliases=["Uptime"])
async def uptime(ctx):
    await ctx.message.delete()
    now = datetime.datetime.utcnow(
    )  # Timestamp of when uptime function is run
    delta = now - start_time
    hours, remainder = divmod(int(delta.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    if days:
        time_format = "**{d}** days, **{h}** hours, **{m}** minutes, and **{s}** seconds."
    else:
        time_format = "**{h}** hours, **{m}** minutes, and **{s}** seconds."
    uptime_stamp = time_format.format(d=days, h=hours, m=minutes, s=seconds)
    await ctx.send(embed=discord.Embed(title=uptime_stamp, color = discord.Colour.blue()))

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title = "Missing Permission",
            description=f"You are missing permissons.",
            color=discord.Colour.red())
        await ctx.send(embed=embed)
    if isinstance(error, commands.CommandNotFound):
      embed  = discord.Embed(
        title = "Command Not Found",
        description = "Type `+help` to see other commands",
        color = discord.Colour.red()
      )
      await ctx.send(embed=embed)
    if isinstance(error, commands.MissingRequiredArgument):
      embed = discord.Embed(
        title = "Missing Requirements",
        description = "You are missing requirements",
        color = discord.Colour.red()
      )
      await ctx.send(embed=embed)
      await ctx.message.delete()


async def status_task():
    while True:
        await client.change_presence(
            status=discord.Status.online,
            activity=discord.Activity(
                type=discord.ActivityType.watching, name=f"+help | +invite | +creators"))
        await asyncio.sleep(10)
        await client.change_presence(
            status=discord.Status.dnd,
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=f"{len(client.guilds)} servers! {len(client.users)} users!"
            ))
        await asyncio.sleep(10)
        await client.change_presence(
            status=discord.Status.idle,
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="discord.ly/galactic"))
        await asyncio.sleep(10)
        await client.change_presence(
            status=discord.Status.idle,
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="https://discord.gg/mWPKNamn3D"))
        await asyncio.sleep(10)


@client.event
async def on_ready():
    print('Galactic Is Online!')
    await status_task()


#########################################
#                                       #
#         MODERATION COMMANDS           #
#                                       #
#########################################

##MEMBERCOUNT##


@client.command(aliases=["Membercount"])
async def membercount(ctx):
    await ctx.message.delete()
    embed = discord.Embed(
        description=f"{ctx.guild.member_count} Members! ",
        color=discord.Colour.blue())
    embed.set_footer(text=f"requested by {ctx.author}")

    await ctx.send(embed=embed)


##MASSUNBAN COMMAND##
@client.command(aliases=["purgebans", "unbanall"])
async def massunban(ctx):
    channel = ctx.channel
    await ctx.message.delete()
    banlist = await ctx.guild.bans()
    for users in banlist:
        try:
            await channel.send(embed = discord.Embed(title="Unbanning Every One In Ban List"))
            await asyncio.sleep(2)
            await ctx.guild.unban(user=users.user)
        except:
            pass


##BAN COMMAND##
@client.command(pass_context=True)
async def ban(ctx, member: discord.Member = None):
    author = ctx.message.author
    channel = ctx.message.channel
    if author.guild_permissions.kick_members:
        if member is None:
            await channel.send(embed=discord.Embed('Please input a user.'))
        else:
            await channel.send(
                embed=discord.Embed("Sucessfully banned {} ".format(member.name)))
            await member.ban()


##MUTE AND UNMUTE Command##


@client.command(aliases=["Mute"])
@commands.has_guild_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member):
    await ctx.message.delete()
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.add_roles(role)
    embed = discord.Embed(
        description=f"muted {member.mention} ", color=discord.Colour.blue())
    embed.set_footer(text=f"requested by {ctx.author}")
    await ctx.send(embed=embed)


@client.command(aliases=["Unmute"])
@commands.has_guild_permissions(manage_roles=True)
async def unmute(ctx, member: discord.Member):
    await ctx.message.delete()
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.remove_roles(role)
    embed = discord.Embed(
        description=f"unmuted {member.mention}.", color=discord.Colour.blue())
    embed.set_footer(text=f"requested by {ctx.author}")
    await ctx.send(embed=embed)


##PURGE COMMAND##


@client.command()
@commands.has_guild_permissions(manage_messages=True)
async def purge(ctx, amount=0):
    await ctx.message.delete()
    await ctx.message.delete()
    await ctx.channel.purge(limit=amount)


#########################################
#                                       #
#           OTHER COMMANDS              #
#                                       #
#########################################

##WHO IS COMMAND##


@client.command(aliases=["Whois"], pass_context=True)
async def whois(ctx, member: discord.Member = None):
    await ctx.message.delete()
    member = ctx.author if not member else member

    roles = [role for role in member.roles]

    embed = discord.Embed(
        colour=member.Colour.blue(), timestamp=ctx.message.created_at)

    embed.set_author(name=f"Account Name | {member}")
    embed.add_field(name="User ID", value=member.id)
    embed.add_field(name="Server Nickname", value=member.display_name)
    embed.add_field(
        name="Account Creation Date",
        value=member.created_at.strftime("%a, %d %B %Y, %I:%M %p UTC"))
    embed.add_field(
        name="Member Joined At",
        value=member.joined_at.strftime("%a, %d %B %Y, %I:%M %p UTC"))
    embed.add_field(
        name=f"Roles({len(roles)})",
        value=" ".join([role.mention for role in roles]))
    embed.set_thumbnail(url=member.avatar_url)
    embed.add_field(name="Bot Detection", value=member.bot)
    embed.set_footer(text=f"requested by {ctx.author}")
    await ctx.send(embed=embed)


##COMMAND COUNT##
@client.command()
async def commandcount(ctx):
    embed = discord.Embed(
        description=f"{len(client.commands)} commands!",
        color=discord.Colour.blue())
    await ctx.send(embed=embed)


## ALL USERS COMMAND ##
@client.command()
async def allusers(ctx):
    embed = discord.Embed(
        description=f"{len(client.member_count)} users!", color=discord.Colour.blue())
    await ctx.send(embed=embed)


##INVITE COMMAND##


@client.command(
    aliases=["invite", "iNVITE", "INVITE", "inv"], pass_context=True)
async def Invite(ctx):
    await ctx.message.delete()
    channel = ctx.message.channel
    embed = discord.Embed(
        description=
        f"**__[invite](https://discord.com/api/oauth2/authorize?client_id=773630957919535145&permissions=8&scope=bot)__**",
        color=discord.Colour.blue())
    embed.add_field(
        name="bot invite",
        value="the invite is used to add the bot into your server.")
    embed.set_footer(text=f"requested by {ctx.author}")
    await channel.send(embed=embed)


embed = discord.Embed(colour=discord.Color.blue())

##SUPPORT COMMAND##


@client.command(aliases=["Support"], pass_context=True)
async def support(ctx):
    await ctx.message.delete()
    channel = ctx.message.channel
    embed = discord.Embed(
        color=discord.Colour.blue(),
        description=
        "**[Galactic Support Server](https://discord.gg/mWPKNamn3D)**")

    embed.add_field(
        name="Support Server",
        value=
        "***If you need any help with Galactic discord bot please join the server linked above.***"
    )
    embed.set_footer(text=f"requested by {ctx.author}")
    await channel.send(embed=embed)


##CREATORS COMMAND##


@client.command(aliases=["Creators", "c", "C"], pass_context=True)
async def creators(ctx):
    await ctx.message.delete()
    channel = ctx.message.channel
    embed = discord.Embed(
        description="**Main Creators** - ¿ Descend.#9422 , Radiuz#9422 ,Rxge#2000 , pine.#9422. **Secondary Creators** - †  , ",
        color=discord.Colour.blue())
    embed.set_footer(text=f"requested by {ctx.author}")
    await channel.send(embed=embed)


##AVATAR COMMAND##


@client.command()
async def av(ctx, *, member: discord.Member = None):
    await ctx.message.delete()
    member = ctx.author if not member else member
    embed = discord.Embed(
        title=f"{member.name}'s avatar",
        color=member.color,
        timestamp=ctx.message.created_at)
    embed.set_image(url=member.avatar_url)
    embed.set_footer(text=f"{ctx.author}", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)


## BOT IFNO COMMAND##
@client.command()
async def info(ctx):
  embed = discord.Embed(
    title = "BotInfo",
    color = discord.Colour.blue())
  embed.add_field(name="Developers", value="Rxge, Pine, Aries & RDZ", inline=False)
  embed.add_field(name="Bot Language", value="Python", inline=False)
  embed.add_field(name="Servers", value=f"{len(client.guilds)} Servers!", inline=False)
  embed.add_field(name="Users", value=f"{len(client.users)} Users!", inline=False)
  embed.add_field(name="Commands", value=f"{len(client.commands)} Commands!", inline=False)
  embed.add_field(name="Prefix", value="Bot Prefixes : + & *", inline=False)
  await ctx.send(embed=embed)
  await ctx.message.delete()
##PING COMMAND##


@client.command(aliases=["Ping", "ping", "Latency"])
async def latency(ctx):
    await ctx.message.delete()
    embed = discord.Embed(
        description=f'Pong! {round(client.latency * 1000)}ms',
        color=discord.Colour.blue())
    embed.set_footer(text=f"requested by {ctx.author}")
    await ctx.send(embed=embed)


##SERVER COUNT##


@client.command()
async def servercount(ctx):
    await ctx.message.delete()
    embed = discord.Embed(
        description=f"{len(client.guilds)} servers!",
        color=discord.Colour.blue())
    embed.set_footer(text=f"requested by {ctx.author}")
    await ctx.send(embed=embed)


##SERVERINFO COMMAND##
@client.command()
async def serverinfo(ctx):
    await ctx.message.delete()
    members = ctx.guild.member_count
    date_format = "%a, %d %b %Y %I:%M %p"
    embed = discord.Embed(
        title=f"{ctx.guild.name}",
        description=
        f"{members} Members\n {len(ctx.guild.roles)} Roles\n {len(ctx.guild.text_channels)} Text-Channels\n {len(ctx.guild.voice_channels)} Voice-Channels\n {len(ctx.guild.categories)} Categories",
        timestamp=datetime.datetime.utcnow(),
        color=discord.Color.red())
    embed.add_field(
        name="Server created at",
        value=f"{ctx.guild.created_at.strftime(date_format)}")
    embed.add_field(name="Server Owner", value=f"{ctx.guild.owner}")
    embed.add_field(name="Server Region", value=f"{ctx.guild.region}")
    embed.add_field(name="Server ID", value=f"{ctx.guild.id}")
    embed.set_thumbnail(url=f"{ctx.guild.icon_url}")
    embed.set_footer(text=f"requested by {ctx.author}")
    await ctx.send(embed=embed)


#########################################
#                                       #
#           MUSIC COMMDANDS             #
#                                       #
#########################################

#########################################
#                                       #
#         ANTI-RAID / ANTI-NUKE         #
#                                       #
#########################################


@client.event
async def on_member_join(member):
    if member.bot:
      await member.ban(reason="Anti Bot is on")


#########################################
#                                       #
#             FUN COMMANDS              #
#                                       #
#########################################

## SAY COMMAND ##


@client.command(aliases=["s", "Say"], pass_context=True)
async def say(ctx, *, text):
    await ctx.message.delete()
    embed = discord.Embed(description=text, color=discord.Colour.blue())
    embed.set_footer(text=f"requested by {ctx.author.name}")
    await ctx.send(embed=embed)


## PENIS COMMAND ##


@client.command(aliases=["PP", "Penis", "penis"], pass_context=True)
async def pp(ctx, member: discord.Member = None):
    await ctx.message.delete()
    ppsize = random.randint(0, 21)
    pp = ""

    if member == None:
        for i in range(0, ppsize):
            pp += "="
        embed = discord.Embed(
            description=f"{ctx.author.mention} pp size: B{pp}D",
            color=discord.Colour.blue())
        embed.set_footer(text=f"requested by {ctx.author}")
        await ctx.send(embed=embed)

    for i in range(0, ppsize):
        pp += "="
        embed = discord.Embed(
            description=f" {member.mention}'s pp size: B{pp}D",
            color=discord.Colour.blue())
    embed.set_footer(text=f"requested by {ctx.author}")
    await ctx.send(embed=embed)



## SIMP COMMAND##
@client.command()
async def simp(ctx, member: discord.Member=None):
  simp = random.randint(1, 100)
  if member == None:
    embed = discord.Embed(
    description=f"{ctx.author.mention} is {simp}% a simp",
    color=discord.Colour.blue())
    await ctx.send(embed=embed)
  embed = discord.Embed(
  description=f"{member.mention} is {simp}% a simp",
  color=discord.Colour.blue())
  await ctx.send(embed=embed)
## RANDOM NUMBER COMMAND ##
@client.command()
async def randomnumber(ctx):
    await ctx.message.delete()
    num = random.randint(1, 10000)
    embed = discord.Embed(description=num, color=discord.Colour.blue())
    embed.set_footer(text=f"requested by {ctx.author}")
    await ctx.send(embed=embed)


## GAY RATE COMMADN##


@client.command(aliases=["Gayrate", "gr", "Gr"])
async def gayrate(ctx, member: discord.Member = None):
    await ctx.message.delete()
    gay = random.randint(0, 100)
    if member == None:
        embed = discord.Embed(
            description=f"{ctx.author.mention} is {gay}% gay",
            color=discord.Colour.blue())
        embed.set_footer(text=f"requested by {ctx.author}")
        await ctx.send(embed=embed)

    embed = discord.Embed(
        description=f"{member.mention} is {gay}% gay",
        color=discord.Colour.blue())
    embed.set_footer(text=f"requested by {ctx.author}")
    await ctx.send(embed=embed)


#########################################
#                                       #
#               MOD-MAIL                #
#                                       #
#########################################

#########################################
#                                       #
#             Help Commands             #
#                                       #
#########################################


@client.command(aliases=["help", "H", "h"])
async def Help(ctx):
    await ctx.message.delete()
    embed = discord.Embed(
        color=discord.Colour.blue(), timestamp=ctx.message.created_at)

    embed.set_author(name="Galatic Commands", icon_url=ctx.author.avatar_url)

    embed.add_field(
        name="📣  | Other", value="Shows Miscellaneous commands", inline=False)
    embed.add_field(name="⚠  | AntiNuke", value="Shows Anti-Nuke commands")
    embed.add_field(name="<a:blobdance:779332518621085717>  | Fun",
        value="Shows Fun commands",
        inline=False)
    embed.add_field(
        name="<a:Mod:779335470567391233>  | Moderation",
        value="Shows Moderation commands",
        inline=False)
    embed.add_field(
        name=":notes:  | Music", value="Shows Music commands", inline=False)
    embed.add_field(
        name=":incoming_envelope:  | Mod-Mail",
        value="Shows ModMail commands",
        inline=False)
    embed.set_footer(text=f"requested by {ctx.author}")

    await ctx.send(embed=embed)


## HELP OTHER ##


@client.command(aliases=["Other"])
async def other(ctx):
    await ctx.message.delete()
    embed = discord.Embed(
        color=discord.Colour.blue(), timestamp=ctx.message.created_at)

    embed.set_author(
        name="Galactic Commands", icon_url=ctx.author.avatar_url)

    embed.add_field(name="Av", value="Shows mentioned users avatar", inline=False)
    embed.add_field(name="Ping", value="Shows bots ping", inline=False)
    embed.add_field(name="Invite", value="Sends bot invite link", inline=False)
    embed.add_field(name="Creators", value="Shows the creators of the bot", inline=False)
    embed.add_field(name="Support", value="Sends inv to support server", inline=False)
    embed.add_field(name="Botinfo (Under Contruction)",value="Shows bot info",inline=False)
    embed.add_field(name="Serverinfo", value="Shows server info", inline=False)
    embed.add_field(name="Whois", value="Shows server info", inline=False)
    embed.add_field(name="Servercount",value="Shows the amount of servers the bot is in",inline=False)
    embed.add_field(name="allusers",value="shows every servers (that the bots in) member count combined")
    embed.add_field(name="commandcount", value="shows command count", inline=False)

    embed.set_footer(text=f"requested by {ctx.author}")
    await ctx.send(embed=embed)


## ANTI NUKE ##


@client.command(aliases=["antinuke", "an"])
async def AntiNuke(ctx):
    await ctx.message.delete()
    embed = discord.Embed(
        color=discord.Colour.blue(), timestamp=ctx.message.created_at)

    embed.set_author(name="Anti-Nuke", icon_url=ctx.author.avatar_url)

    embed.add_field(name="**Under Construction**",value="Anti-Nuke Will Be Out Soon!",inline=False)

    embed.set_footer(text=f"requested by {ctx.author}")
    await ctx.send(embed=embed)

## MUSIC##

@client.command(aliases=["music"])
async def Music(ctx):
    await ctx.message.delete()
    embed = discord.Embed(
        color=discord.Colour.blue(), timestamp=ctx.message.created_at)

    embed.set_author(name="Music Commands", icon_url=ctx.author.avatar_url)

    embed.add_field(name="**Under Construction**",value="Music Will Be Out Soon!",inline=False)

    embed.set_footer(text=f"requested by {ctx.author}")
    await ctx.send(embed=embed)


client.run(token, bot=True)
