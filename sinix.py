from asyncio.tasks import wait_for
from os import name
import discord
from discord import message
from discord import reaction
from discord import member
from discord import guild
from discord import utils
from discord import emoji
from discord import user
from discord import embeds
from discord.colour import Color
from discord.embeds import Embed
from discord.ext import commands
from discord.ext.commands.core import check
from discord.permissions import make_permission_alias
import time
import youtube_dl
import asyncio
from discord.ext import tasks
from discord_buttons_plugin import *
import requests


intents = discord.Intents().all()
bot = commands.Bot(command_prefix="sinix/", intents=intents, help_command=None)
musics = {}
ytdl = youtube_dl.YoutubeDL()
buttons = ButtonsClient(bot)



@bot.event
async def on_ready():
    print("[------------- CONECTED -------------]")
    bot.my_current_task = live_status.start()


class config:
    guildID = 879672405612699648


@tasks.loop()
async def live_status(seconds=75):
    Dis = bot.get_guild(config.guildID) #Int


    activity = discord.Activity(type=discord.ActivityType.watching, name=f'👥 {Dis.member_count}')
    await bot.change_presence(activity=activity)
    await asyncio.sleep(15)

    activity = discord.Activity(type=discord.ActivityType.watching, name=f'YOLTIX#1647')
    await bot.change_presence(activity=activity)
    await asyncio.sleep(15)

    activity = discord.Activity(type=discord.ActivityType.watching, name=f'Sinix leaks')
    await bot.change_presence(activity=activity)
    await asyncio.sleep(15)

    activity = discord.Activity(type=discord.ActivityType.watching, name=f'Developper par Yoltix')
    await bot.change_presence(activity=activity)
    await asyncio.sleep(15)







@bot.command()
async def sug(ctx, *texte):
    embed = discord.Embed(title="Voici la suggestion :", color=0xE0ED12)
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/769485806641217539/831206278177095771/ampoule_1.png")
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    embed.add_field(name=" ".join(texte), value=ctx.author.name, inline=False)
    message = await ctx.send(embed=embed)
    await message.add_reaction("✅")
    await message.add_reaction("❌")
    await ctx.message.delete()



@bot.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member, raison):
    log = discord.utils.get(ctx.guild.channels, id=int("879672537926209566"))
    await ctx.message.delete()
    role = discord.utils.get(ctx.guild.roles, id=int("879753185974173777"))
    await member.add_roles(role)
    await ctx.send(f"{member.mention} C'est fait mute", )
    embed = discord.Embed(title="Mute", description=f"{member.mention} C'est fait mute par {ctx.message.author.mention} pour {raison}", color=0xB22E00)
    await log.send(embed=embed)


@bot.command()
@commands.has_permissions(manage_roles=True)
async def umute(ctx, member: discord.Member):
    log = discord.utils.get(ctx.guild.channels, id=int("879672537926209566"))
    await ctx.message.delete()
    role = discord.utils.get(ctx.guild.roles, id=int("879753185974173777"))
    await member.remove_roles(role)
    await ctx.send(f"{member.mention}, c'est fait demute")
    embed = discord.Embed(title="Umute", description=f"{member.mention} C'est fait umute par {ctx.message.author.mention}", color=0x17FF00)
    await log.send(embed=embed)

@bot.command()
@commands.has_guild_permissions(ban_members=True)
async def ban(ctx, user: discord.User, reason):
    log = discord.utils.get(ctx.guild.channels, id=int("879672537926209566"))    
    await ctx.message.delete()
    reason = " ".join(reason)
    await ctx.guild.ban(user, reason=reason)
    await ctx.send(f"{user} à été ban pour")
    embed = discord.Embed(title="Ban", description=f"{user.mention} C'est fait ban par {ctx.message.author.mention} pour {reason}", color=0xFF001F)
    await log.send(embed=embed)    


class Video:
    def __init__(self, link):
        video = ytdl.extract_info(link, download=False)
        video_format = video["formats"][0]
        self.url = video["webpage_url"]
        self.stream_url = video_format["url"]

@bot.command()
async def leave(ctx):
    client = ctx.guild.voice_client
    await client.disconnect()
    musics[ctx.guild] = []

@bot.command()
async def resume(ctx):
    client = ctx.guild.voice_client
    if client.is_paused():
        client.resume()


@bot.command()
async def pause(ctx):
    client = ctx.guild.voice_client
    if not client.is_paused():
        client.pause()


@bot.command()
async def skip(ctx):
    client = ctx.guild.voice_client
    client.stop()


def play_song(client, queue, song):
    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(song.stream_url
        , before_options = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"))

    def next(_):
        if len(queue) > 0:
            new_song = queue[0]
            del queue[0]
            play_song(client, queue, new_song)
        else:
            asyncio.run_coroutine_threadsafe(client.disconnect(), bot.loop)

    client.play(source, after=next)


@bot.command()
async def play(ctx, url):
    print("play")
    client = ctx.guild.voice_client

    if client and client.channel:
        video = Video(url)
        musics[ctx.guild].append(video)
    else:
        channel = ctx.author.voice.channel
        video = Video(url)
        musics[ctx.guild] = []
        client = await channel.connect()
        await ctx.send(f"Je lance : {video.url}")
        play_song(client, musics[ctx.guild], video)



@bot.command(aliases= ['purge','delete'])
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount : int):
   if amount == None:
       await ctx.channel.purge(limit=1000000)
   else:
       await ctx.channel.purge(limit=amount)




@bot.command()
async def invite(ctx):
	invite = "https://discord.gg/SbrM7qgNrz"
	await ctx.send(f"Voici le lien d'invitation {invite}")



@bot.command()
async def myid(ctx):
	await ctx.send(f"Ton id est {ctx.author.id}")

@bot.command()
@commands.has_guild_permissions(manage_messages=True)
async def lock(ctx):
    log = discord.utils.get(ctx.guild.channels, id=int("879672537926209566"))    
    role = discord.utils.get(ctx.guild.roles, id=int("879806404989452329"))
    everyone = discord.utils.get(ctx.guild.roles, id=int("879672405612699648"))
    membre = discord.utils.get(ctx.guild.roles, id=int("879806430943784970"))
    await ctx.channel.set_permissions(everyone, read_messages=True, send_messages=False)
    await ctx.channel.set_permissions(role, send_messages=True, read_messages=True)
    await ctx.channel.set_permissions(membre, read_messages=True, send_messages=False)
    await ctx.channel.send("Channel Lock")
    embed = discord.Embed(title="Lock", description=f"{ctx.message.author.mention} A lock le channel {ctx.message.channel.mention}", color=0x001FFE)
    embed.set_author(name="Copyright © 2021 Yoltix. Tous droits réservés")
    await log.send(embed=embed)    


@bot.command()
@commands.has_guild_permissions(manage_messages=True)
async def unlock(ctx):
    log = discord.utils.get(ctx.guild.channels, id=int("879672537926209566"))    
    role = discord.utils.get(ctx.guild.roles, id=int("879806404989452329"))
    everyone = discord.utils.get(ctx.guild.roles, id=int("879672405612699648"))
    membre = discord.utils.get(ctx.guild.roles, id=int("879806430943784970"))
    await ctx.channel.set_permissions(everyone, read_messages=True, send_messages=True)
    await ctx.channel.set_permissions(role, send_messages=True, read_messages=True)
    await ctx.channel.set_permissions(membre, read_messages=True, send_messages=True)
    await ctx.channel.send("Channel Unlock")
    embed = discord.Embed(title="Unlock", description=f"{ctx.message.author.mention} A unlock le channel {ctx.message.channel.mention}", color=0xC134CD)
    embed.set_author(name="Copyright © 2021 Yoltix. Tous droits réservés")
    await log.send(embed=embed)  

@bot.command()
@commands.has_guild_permissions(kick_members=True)
async def kick(ctx, user: discord.User, reason):
    log = discord.utils.get(ctx.guild.channels, id=int("879672537926209566"))    
    await ctx.message.delete()
    reason = " ".join(reason)
    await ctx.guild.kick(user, reason=reason)
    await ctx.send(f"{user} à été kick .")
    embed = discord.Embed(title="Kick", description=f"{user.mention} C'est fait kick par {ctx.message.author.mention}", color=0x34CDC8)
    embed.set_author(name="Copyright © 2021 Yoltix. Tous droits réservés")
    await log.send(embed=embed) 




@clear.error
async def clear_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send("il faut donner un nombre.")

@ban.error
async def ban_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send("il faut donner une raison")

@kick.error
async def kick_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send("il faut donner une raison")








@buttons.click
async def button_one(ctx):
    role = discord.utils.get(ctx.guild.roles, id=int("879806404989452329"))
    overwrites = {
        role: discord.PermissionOverwrite(read_messages=True),
        ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=True,
                                                            read_message_history=True),
        ctx.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True, read_message_history=True),
        ctx.member : discord.PermissionOverwrite(read_messages=True, send_messages=True,
                                                        read_message_history=True),
    }
    channel = await ctx.guild.create_text_channel(name=f"Ticket-{ctx.member.name}",  category=bot.get_channel(879672635292778556), overwrites=overwrites)
    await ctx.reply(f"Votre ticket a ete cree {channel.mention}", flags = MessageFlags().EPHEMERAL)
    embed = discord.Embed(title="Ticket", description="Appuyez sur le bouton pour fermer le ticket")
    await buttons.send(
        content = None,
        embed = embed,
        channel = channel.id,
        components = [
            ActionRow([
                Button(
                    label="Close", 
                    style=ButtonType().Primary, 
                    custom_id="button_close"          
                )
            ])
        ]
    )


closemess = 0

@buttons.click
async def button_close(ctx):
     closemess = await buttons.send(
        content = f"Ete vous sur de vouloir fermer le ticket ? {ctx.member.mention}",
        channel = ctx.channel.id,
        components = [
            ActionRow([
                Button(
                    label="Oui", 
                    style=ButtonType().Danger, 
                    custom_id="button_closesur"
                    
                ), Button(
			   label="Non",
			   style=ButtonType().Primary,
			   custom_id="button_noclose"        
		 )
            ])
        ]
    )

@buttons.click
async def button_closesur(ctx):
        await ctx.channel.send("Ce ticket va s'auto detruire dans 5 secondes")
        time.sleep(1.0)
        time.sleep(1.0)
        time.sleep(1.0)
        time.sleep(1.0)
        time.sleep(1.0)
        await ctx.channel.delete()

@buttons.click
async def button_noclose(ctx):
       global closemess
       await ctx.message.delete()


embed = discord.Embed(title="Ticket", description="Appuyez sur le bouton pour ouvrir le ticket")
embed.set_author(name="Copyright © 2021 Yoltix. Tous droits réservés")

@bot.command()
async def createe(ctx):

 	await buttons.send(
	    content = None,
        embed = embed,
		channel = ctx.channel.id,
		components = [
			ActionRow([
				Button(
					label="Cree un Tickets", 
					style=ButtonType().Primary, 
					custom_id="button_one"          
				)
			])
		]
	)    



@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.MissingPermissions):
		await ctx.send("Vous n'avez pas les permissions pour faire cette commande.")




@bot.event
async def on_member_join(member):
    role=  discord.utils.get(member.guild.roles,id=int("879806430943784970"))
    embed = discord.Embed(title=f"Oh ! {member.name}, viens de rejoindre le discord ! :)", color=0x7f00ff)
    embed.set_image(
        url=f"{member.avatar_url}")
    embed.set_footer(text=f"Nous somme maintenant {member.guild.member_count}")
    embed.set_author(name="Copyright © 2021 Yoltix. Tous droits réservés")


    await bot.get_channel(879753146849705994).send(embed=embed)
    await member.add_roles(role)



embed1 = discord.Embed(title="**Commande**", description ="Voici les commande disponible", color=0x34CDC8)
embed1.add_field(name="sinix/sug", value=" Pemet de faire une suggestion", inline=False)
embed1.add_field(name="sinix/invite", value="Permet d'avoir le lien d'invite de votre discord", inline=False)
embed1.add_field(name="sinix/myid", value="Permet de voir ton id", inline=False)
embed1.set_footer(text="Page 1/4")
embed1.set_author(name="Copyright © 2021 Yoltix. Tous droits réservés")

embed2 = discord.Embed(title="Commande D'administration", description ="Voici les commande disponible", color=0xFF6C00)
embed2.add_field(name="sinix/clear", value="Clear un nombre de message", inline=False)
embed2.add_field(name="sinix/mute", value="Mute un membre", inline=False)
embed2.add_field(name="sinix/umute", value="Umute un membre", inline=False)
embed2.add_field(name="sinix/ban", value="Ban un membre", inline=False)
embed2.add_field(name="sinix/kick", value="Kick un membre", inline=False)
embed2.add_field(name="sinix/lock", value="lock un channel", inline=False)
embed2.add_field(name="sinix/unlock", value="unlock un channel", inline=False)
embed2.set_footer(text="Page 2/4")
embed2.set_author(name="Copyright © 2021 Yoltix. Tous droits réservés")


embed3 = discord.Embed(title="Commande Musique", description ="Voici les commande disponible", color=0xECFF00)
embed3.add_field(name="__sinix/play__", value="Permet de lancer une musique", inline=False)
embed3.add_field(name="__sinix/leave__", value="permet de deconnecter le bot", inline=False)
embed3.add_field(name="__sinix/pause__", value="Mettre pause a la musique", inline=False)
embed3.add_field(name="__sinix/resume__", value="Mettre play a la musique", inline=False)
embed3.add_field(name="__sinix/skip__", value="Passer au son suivant", inline=False)
embed3.set_footer(text="Page 3/4")
embed3.set_author(name="Copyright © 2021 Yoltix. Tous droits réservés")

embed4 = discord.Embed(title="Commande Invisible", description ="Voici les commande disponible", color=0xECFF00)
embed4.set_author(name="Copyright © 2021 Yoltix. Tous droits réservés")
embed4.add_field(name="Message de bienvenue", value="Un message quand une personne rejoins", inline=False)
embed4.add_field(name="Status qui change tout seul", value="Le status du bot change selon vos envie", inline=False)
embed4.add_field(name="Ticket", value="Syteme de ticket", inline=False)
embed4.set_footer(text="Page 4/4")

bot.help_pages = [embed1, embed2, embed3, embed4]

@bot.command()
async def help(ctx):
    buttons = [u"\u25C0", u"\u25B6"]
    current = 0
    message = await ctx.send(embed=bot.help_pages[current])

    for button in buttons:
        await message.add_reaction(button)


    while True:
        try:
            reaction, user = await bot.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons, timeout = 60.0)
        except asyncio.TimeoutError:
            print("fin du temp")

        else:
            previous_page = current

            if reaction.emoji == u"\u25C0":
                if current > 0:
                    current -= 1
            elif reaction.emoji == u"\u25B6":
                if current < len(bot.help_pages)-1:
                    current += 1


            for button in buttons:
                await message.remove_reaction(button, ctx.author)
            if current !=  previous_page:
                await message.edit(embed=bot.help_pages[current])

bot.run("TOKEN")


