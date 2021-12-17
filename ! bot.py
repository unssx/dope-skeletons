import discord
from discord.ext import commands
import os
from datetime import datetime

client = commands.Bot(command_prefix = '!')
client.remove_command('help')

maincolor=0x2f3136

filtered_words = ["nigger", "nigga", "niggah", "niga", "niger", "nibba", "nibber", "niggar", "gay", "asshole", "hoe"]

@client.event
async def on_ready():
    activity = discord.Activity(type=discord.ActivityType.listening, name="!help")
    await client.change_presence(status=discord.Status.online, activity=activity)
    print('Bot is ready.')

@client.event
async def on_message(msg):
	for word in filtered_words:
		if word in msg.content:
			await msg.delete()

	await client.process_commands(msg)

@client.event
async def on_command_error(ctx,error):
	embedPERMS=discord.Embed(color=maincolor, description=f"***No tienes los permisos para este comando***")
	embedARGS=discord.Embed(color=maincolor, description=f"***Por favor, introduzca todos los argumentos necesarios***")
	embedMNF=discord.Embed(color=maincolor, description=f"***Miembro no encontrado***")
	embedFNF=discord.Embed(color=maincolor, description=f"***Este usuario no ha hecho nada que vaya en contra de las normas***")
	if isinstance(error,commands.MissingPermissions):
		await ctx.reply(embed=embedPERMS)
	elif isinstance(error,commands.MissingRequiredArgument):
		await ctx.reply(embed=embedARGS)
	elif isinstance(error,commands.MemberNotFound):
		await ctx.reply(embed=embedMNF)
	elif isinstance(error,commands.CommandInvokeError):
		pass
	else:
		raise error

@client.command(aliases=['c'])
@commands.has_permissions(manage_messages = True)
async def clear(ctx, amount=2):
    await ctx.channel.purge(limit = amount)

@client.command(aliases=['h'])
async def help(ctx):
    today = datetime.today().strftime('%H:%M')
    embed=discord.Embed(color=maincolor, description=f"**COMMANDOS**\n\n**clear** - Este comando borra todo el texto por encima de su mensaje actual, escriba un número después del comando para elegir cuántos mensajes deben ser borrados\n\n**about** - Utilice este comando para comprobar algunas estadísticas sobre los usuarios de este servidor, puede ser útil\n\n**stats** - Comprueba cuántas veces este usuario ha sido baneado, 'kickeado' y 'muteado' y todo tipo de cosas en contra de las reglas\n\n**kick** - Este comando expulsa al usuario que pongas después de él\n\n**ban** - Utiliza este comando para banear al usuario\n\n**unban** - Desbanea a una persona (contrario del commando 'ban')\n\n**mute** - Le da al usuario un mute\n\n**unmute** - Desmutea a alguien (contrario del commando 'mute')")
    embed.set_footer(text=f"Today {today}")
    await ctx.send(embed=embed)

@client.command(aliases=['a'])
async def about(ctx, member : discord.Member, *,reason=""):
    perm_list = [perm[0] for perm in member.guild_permissions if perm[1]]
    today = datetime.today().strftime('%H:%M')
    embed=discord.Embed(color=maincolor, description=f"{member.mention}")
    embed.set_footer(text=f"ID: {member.id} • Today {today}")
    embed.set_author(name=f"{member}", icon_url=f"{member.avatar_url}")
    embed.set_thumbnail(url=f"{member.avatar_url}")
    embed.add_field(name="Se unió", value=f"{member.joined_at.strftime('%b, %a %d, %Y %H:%M %p')}", inline=True)
    embed.add_field(name="Registrado", value=f"{member.created_at.strftime('%b, %a %d, %Y %H:%M %p')}", inline=True)
    embed.add_field(name=f"Papel más importante", value=f"{member.top_role}", inline=False)
    embed.add_field(name=f"Lista de permisos", value=f"{perm_list}", inline=False)
    await ctx.reply(embed=embed)

@client.command(aliases=['s'])
async def stats(ctx, member : discord.Member, *,reason=""):
        f = open(f"{member.id}.txt", "r")
        today = datetime.today().strftime('%H:%M')
        embed=discord.Embed(color=maincolor, description=f"{member.mention} \n\n {f.read()} \n")
        embed.set_footer(text=f"ID: {member.id} • Today {today}")
        embed.set_author(name=f"{member}", icon_url=f"{member.avatar_url}")
        embed.set_thumbnail(url=f"{member.avatar_url}")
        await ctx.reply(embed=embed)

@client.command(aliases=['k'])
@commands.has_permissions(kick_members = True)
async def kick(ctx, member : discord.Member, *,reason="No se ha proporcionado ninguna razón"):
    embed=discord.Embed(color=maincolor, description=f"***{member} ha sido expulsado***, "+ reason)
    embed2=discord.Embed(color=maincolor, description=f"***Has sido expulsado de Acadèmia culer***, "+ reason)
    await ctx.reply(embed=embed)
    try:
    	await member.send(embed=embed2)
    except:
    	pass

    await member.kick(reason=reason)
    with open(f'{member.id}.txt', 'a+') as f:
        filesize = os.path.getsize(f"{member.id}.txt")
        today = datetime.today().strftime('**%Y-%m-%d**')
        if filesize == 0:
            f.seek(0)
            f.write(f"**Fue expulsado,** {today}")
            f.write("\n")
            f.write(f"{reason}")
        else:
            f.seek(0)
            f.write("\n")
            f.write("\n")
            f.write(f"**Fue expulsado,** {today}")
            f.write("\n")
            f.write(f"{reason}")

@client.command(aliases=['b'])
@commands.has_permissions(ban_members = True)
async def ban(ctx, member : discord.Member, *,reason="No se ha proporcionado ninguna razón"):
    embed=discord.Embed(color=maincolor, description=f"***{member} ha sido expulsado***, "+ reason)
    embed2=discord.Embed(color=maincolor, description=f"***Has sido expulsado***, "+ reason)
    await ctx.reply(embed=embed)
    try:
    	await member.send(embed=embed2)
    except:
    	pass

    await member.ban(reason=reason)
    with open(f'{member.id}.txt', 'a+') as f:
        filesize = os.path.getsize(f"{member.id}.txt")
        today = datetime.today().strftime('**%Y-%m-%d**')
        if filesize == 0:
            f.seek(0)
            f.write(f"**Baneado,** {today}")
            f.write("\n")
            f.write(f"{reason}")
        else:
            f.seek(0)
            f.write("\n")
            f.write("\n")
            f.write(f"**Baneado,** {today}")
            f.write("\n")
            f.write(f"{reason}")

@client.command(aliases=['ub'])
@commands.has_permissions(ban_members = True)
async def unban(ctx, *, member):
    embed=discord.Embed(color=maincolor, description=f"***{member} ha sido desbaneado***, pura suerte...")
    embed2=discord.Embed(color=maincolor, description=f"***Has sido desprotegido***, joinback")
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user
  
    if (user.name, user.discriminator) == (member_name, member_discriminator):
        await ctx.guild.unban(user)
        await ctx.reply(embed=embed)
        await member.send(embed=embed2)
        with open(f'{member.id}.txt', 'a+') as f:
            filesize = os.path.getsize(f"{member.id}.txt")
            today = datetime.today().strftime('**%Y-%m-%d**')
            if filesize == 0:
                f.seek(0)
                f.write(f"**Fue desprohibido,** {today}")
                f.write("\n")
                f.write(f"Tuviste suerte...")
            else:
                f.seek(0)
                f.write("\n")
                f.write("\n")
                f.write(f"**Fue desprohibido,** {today}")
                f.write("\n")
                f.write(f"{reason}")
        return

@client.command(aliases=['m'])
@commands.has_permissions(kick_members = True)
async def mute(ctx, member : discord.Member, reason="No se ha proporcionado ninguna razón"):
    muted_role = ctx.guild.get_role(918975640290623489) #DONT FRGOETDONT FRGOETDONT FRGOETDONT FRGOETDONT FRGOETDONT FRGOETDONT FRGOETDONT FRGOETDONT FRGOETDONT FRG 

    await member.add_roles(muted_role)

    embed=discord.Embed(color=maincolor, description=f"***{member} ha sido muteado***, "+ reason)
    embed2=discord.Embed(color=maincolor, description=f"***Has sido silenciado***, "+ reason)
    await ctx.reply(embed=embed)
    try:
    	await member.send(embed=embed2)
    except:
    	pass

    with open(f'{member.id}.txt', 'a+') as f:
        filesize = os.path.getsize(f"{member.id}.txt")
        today = datetime.today().strftime('**%Y-%m-%d**')
        if filesize == 0:
            f.seek(0)
            f.write(f"**Muteado,** {today}")
            f.write("\n")
            f.write(f"{reason}")
        else:
            f.seek(0)
            f.write("\n")
            f.write("\n")
            f.write(f"**Muteado,** {today}")
            f.write("\n")
            f.write(f"{reason}")

@client.command(aliases=['um'])
@commands.has_permissions(kick_members = True)
async def unmute(ctx, member : discord.Member):
    muted_role = ctx.guild.get_role(918975640290623489) #DONT FRGOETDONT FRGOETDONT FRGOETDONT FRGOETDONT FRGOETDONT FRGOETDONT FRGOETDONT FRGOETDONT FRGOETDONT FRG 

    await member.remove_roles(muted_role)

    embed2=discord.Embed(color=maincolor, description=f"***{member} ya no esta muteado***")
    await ctx.reply(embed=embed2)
    with open(f'{member.id}.txt', 'a+') as f:
        filesize = os.path.getsize(f"{member.id}.txt")
        today = datetime.today().strftime('**%Y-%m-%d**')
        if filesize == 0:
            f.seek(0)
            f.write(f"**Desmuteado,** {today}")
            f.write("\n")
            f.write(f"Ha llegado el momento")
        else:
            f.seek(0)
            f.write("\n")
            f.write("\n")
            f.write(f"**Desmuteado,** {today}")
            f.write("\n")
            f.write(f"Ha llegado el momento")



client.run('OTE4OTQ2MjgxMTM1NjczNDM2.YbOpag.p-3gIHhWV7P-LchxJDP_7pNJfB8')
