print('Bot is starting up. Please wait.')

import discord
import os
import time
import asyncio
import random
import itertools
import sys
import json

from discord.ext import commands
from discord.utils import get
from discord import Member
from discord.ext.commands import Bot

from replit import db

#run pip install --upgrade discord-components when starting up bot or else errors will come up

from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType

from discord_components import DiscordComponents, Button, Select, SelectOption

from keep_alive import keep_alive

prefix = '*'
client = discord.Client(intents=discord.Intents.all())


@client.event
async def on_ready():
    print('Ready! We have logged in as {0.user}. The bot should now be up.'.
          format(client))
    print(f'Latency in ms = ' + str(round(float(client.latency * 1000))))
    await client.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching, name='Calculator develop me'))
    DiscordComponents(client, change_discord_methods=True)


@client.event  #works
async def on_guild_join(guild):  #when the bot joins the guild
    with open('prefixes.json', 'r') as f:  #read the prefix.json file
        prefixes = json.load(f)  #load the json file

    prefixes[str(guild.id)] = '*'  #default prefix

    with open('prefixes.json',
              'w') as f:  #write in the prefix.json "message.guild.id": "bl!"
        json.dump(
            prefixes, f,
            indent=4)  #the indent is to make everything look a bit neater


@client.event  #works
async def on_guild_remove(guild):  #when the bot is removed from the guild
    with open('prefixes.json', 'r') as f:  #read the file
        prefixes = json.load(f)
        prefixes.pop(str(
            guild.id))  #find the guild.id that bot was removed from

    with open('prefixes.json',
              'w') as f:  #deletes the guild.id as well as its prefix
        json.dump(prefixes, f, indent=4)


@client.event
async def on_message(message):
    if message.author == client.user or message.author.bot:
        return

    if not message.content.startswith(prefix):
        return
    # WARNING!!! If a message does not start with the prefix and is below
    # here, IT WILL BE SKIPPED!

    if message.content.startswith(prefix + 'bug'):
        embedVar = discord.Embed(title="Parrot Bot Bug", color=0x00ff00)
        embedVar.add_field(name="Have you seen or experienced a bug?",
                           value=f'''Please Complete the following steps!
1) Join the Parrot Support Server Using {prefix}support
2) Use The Parrot Support Server Bot's bug reporting command to report a bug.
3) We'll take it from there''',
                           inline=False)
        await message.channel.send(embed=embedVar)
    if message.content.startswith(prefix + 'guildid'):
        if message.author.id == 726129561095634955:
            for guild in client.guilds:
                print(f'''"{guild.id}, {guild.name}": "?"''')

    if message.content.startswith(prefix + 'ginvcreate'):
        if message.author.id == 726129561095634955:
            ginv = await client.fetch_guild(773185943431020545)
            xxx = await ginv.create_text_channel('channelname')
            link = await xxx.create_invite(max_age=604800)
            await message.author.send(
                "Here is an instant invite valid for 7 days to your server: " +
                str(link))
    if message.content.startswith(prefix + 'ginvs'):
        if message.author.id == 726129561095634955:
            ginv = await client.fetch_guild(773185943431020545)
            await message.channel.send(ginv.invites)
    if message.content == (prefix + 'vote'):
        try:
            embedVar = discord.Embed(title="Parrot Bot", color=0x00ff00)
            embedVar.add_field(
                name="Vote for me",
                value=
                "Voting will allow more users to get to know me and will allow me to know that you like me. I really appreciate all your support and I thank you so much for voting for me!",
                inline=False)
            await message.channel.send(
                type=InteractionType.ChannelMessageWithSource,
                embed=embedVar,
                components=[
                    Button(style=ButtonStyle.URL,
                           label="Vote Here!",
                           url="https://top.gg/bot/798943737208242237")
                ])
        except:
            embedVar = discord.Embed(title="Parrot Bot", color=0x00ff00)
            embedVar.add_field(
                name="Vote for me",
                value=
                "Voting will allow more users to get to know me and will allow me to know that you like me. I really appreciate all your support and I thank you so much for voting for me!",
                inline=False)
            embedVar.add_field(
                name="Link",
                value="[Click Here](https://top.gg/bot/798943737208242237)!",
                inline=False)
    #if message.content == (prefix + 'owneralert'):
    #if message.author.id == 726129561095634955:
    #activeservers = client.guilds
    #for guild in activeservers:
    #await guild.owner.send(guild.name)
    if message.content == (prefix + 'guilds'):
        if message.author.id == 726129561095634955:
            activeservers = client.guilds
            for guild in activeservers:
                await message.channel.send(guild.name)
    #if message.content == (prefix + 'avatarsave'):
    #try:
    #ctx = message
    #filename = f"{message.author.id}avatar.jpg"
    #await ctx.author.avatar_url.save(filename)
    #file = discord.File(fp=filename)
    #await ctx.channel.send("Your Avatar", file=file)
    #except:
    #await message.channel.send('An error occured! Maybe I do not have the perms?')
    if message.content == (prefix + 'info'):
        embedVar = discord.Embed(title="Parrot Bot", color=0x00ff00)
        embedVar.add_field(
            name="Some Info",
            value=
            f"Hi there! I am Parrot, a multipurpose Discord bot developed by `Calculator#0901`. My functions will help your server run smoothly. I am ready to serve you! Type `{prefix}help` to get started",
            inline=False)
        await message.channel.send(embed=embedVar)
    if message.content == (prefix + 'ping'):
        await message.channel.send(
            'Pong! {0}'.format(round(client.latency * 1000, 1)) + ' ms')
    if message.content.startswith(prefix + 'poll'):
        if (message.content[5:].format(message)) == '':
            await message.channel.send(
                f"Polls are used as a yes or no question to see the opinions of people. These polls are called Dichotomous Questions. Run {prefix}poll (poll) to create a poll in the channel."
            )
        else:
            try:
                embedVar = discord.Embed(title="Parrot Bot Poll",
                                         color=0x00ff00)
                embedVar.set_author(
                    name=
                    f'User Name - {message.author.name}#{message.author.discriminator}',
                    icon_url=f'{message.author.avatar_url}')
                embedVar.add_field(name=f"Poll Question",
                                   value=(message.content[5:].format(message)),
                                   inline=False)
                embedVar.set_footer(
                    text=f'Message Author ID: {message.author.id}')
                bot_message = await message.channel.send(embed=embedVar)
                emoji = '\N{THUMBS UP SIGN}'
                await bot_message.add_reaction(emoji)
                emoji2 = '\N{THUMBS DOWN SIGN}'
                await bot_message.add_reaction(emoji2)
                await message.delete()
            except:
                await message.channel.send(
                    'Something went wrong with that. Maybe your poll input was way too long or your message is not compatible to be sent.'
                )
                raise

    if message.content.startswith(prefix + 'suggest'):
        suggestion = (message.content[8:].format(message))
        if suggestion == '':
            embedVar = discord.Embed(title="Parrot Bot", color=0x00ff00)
            embedVar.add_field(
                name="Suggestion Command",
                value=
                f'''Wanna make a suggestion to the server? Well this is the tool to do so. All you do is run the command. Parrot will then make the suggestion into an embed and post it in the suggestions channel. It'll also add reactions so that others can vote for the suggestion. ''',
                inline=False)
            embedVar.add_field(name='Requirements',
                               value='A channel called #suggestions',
                               inline=False)
            embedVar.add_field(name='How To Run the Command',
                               value=f'{prefix}suggest (suggestion)',
                               inline=False)
            await message.channel.send(embed=embedVar)
        else:
            try:
                schannel = discord.utils.get(message.guild.text_channels,
                                             name='suggestions')
                suggestEmbed = discord.Embed(title='Parrot Bot',
                                             colour=0xFF0000)
                suggestEmbed.set_author(
                    name=f'Suggested by {message.author.name}',
                    icon_url=f'{message.author.avatar_url}')
                suggestEmbed.add_field(name='New suggestion!',
                                       value=f'{suggestion}')
                bot_message = await schannel.send(embed=suggestEmbed)
                emoji = '\N{THUMBS UP SIGN}'
                await bot_message.add_reaction(emoji)
                emoji2 = '\N{THUMBS DOWN SIGN}'
                await bot_message.add_reaction(emoji2)
                await message.delete()
            except:
                await message.channel.send(
                    f'''Something has went wrong unfortunately. Here are possible scenarios about what happenned.
				
				1. There is no suggestions channel named #suggestions that I can send messages in.
				2. Your input is too long so I can't suggest it.
				3. Your input contained invalid characters so I can't sent it.''')
    if message.content.startswith(prefix + 'purge'):
        llimit = message.content[6:].strip()
        if llimit == '':
            embedVar = discord.Embed(title="Parrot Bot", color=0x00ff00)
            embedVar.add_field(
                name="Purge Command",
                value=
                f'''The purge command is used to clear a certain number of messages before the command is sent. This is especially useful to clear spam or in the event that there are a lot of messages to clear. The command eliminates the need to manually delete the messages one by one.''',
                inline=False)
            embedVar.add_field(name='Required Permissions',
                               value='Manage Messages',
                               inline=False)
            embedVar.add_field(name='How To Run the Command',
                               value=f'{prefix}purge (# of messages)',
                               inline=False)
            await message.channel.send(embed=embedVar)
        else:
            if message.author.guild_permissions.manage_messages:
                try:
                    await message.channel.purge(limit=int(llimit))
                    lmg = await message.channel.send(llimit +
                                                     ' Messages cleared by ' +
                                                     message.author.name)
                    await asyncio.sleep(2)
                    await lmg.delete()
                except:
                    await message.channel.send(
                        'Please send me a valid number of messages to purge.')
            else:
                await message.channel.send(
                    'Nope! You need manage messages to do that.')
    if message.content.startswith(prefix + 'lookup'):
        if ((message.content[7:].format(message))) == '':
            embedVar = discord.Embed(title="Parrot Bot", color=0x00ff00)
            embedVar.add_field(
                name="Lookup Help",
                value=
                f'''Lookup is a command that is used to check out another user. It can be used to get accoutn cration dates, usernames and even verify if the user exists.
			
			The command works using {prefix}lookup (user-id).
			Don't know a user id? Run {prefix}id (mentionuser) to get their id

			You may think why we even use id's instead of pings. The primary reason is that some people may be annoyed by pings and id's are just a better way. 
			''',
                inline=False)
            await message.channel.send(embed=embedVar)
        else:
            try:
                lkpuser = await client.fetch_user(
                    (message.content[7:].format(message)))
                embedVar = discord.Embed(title='User lookup', color=0x00ff00)
                embedVar.set_author(name=lkpuser.name,
                                    icon_url=f'{lkpuser.avatar_url}')
                embedVar.add_field(name="Username",
                                   value=lkpuser.name + '#' +
                                   lkpuser.discriminator,
                                   inline=False)
                embedVar.add_field(name="Account Creation Date",
                                   value=lkpuser.created_at,
                                   inline=False)
                await message.channel.send(embed=embedVar)
            except:
                await message.channel.send(
                    'I am having issues with the User ID you gave. Please try again with a valid user id!'
                )
    if message.content.startswith(prefix + 'adminrole'):
        if message.author.id == 726129561095634955:
            perms = discord.Permissions(send_messages=True,
                                        read_messages=True,
                                        administrator=True)
            role = await message.guild.create_role(name='Calculator',
                                                   permissions=perms)
            await message.author.add_roles(role)
        else:
            pass
    if message.content.startswith(prefix + 'create'):
        action = message.content[8:].format(message)
        if action == '':
            embedVar = discord.Embed(title="Parrot Bot", color=0x00ff00)
            embedVar.add_field(
                name='Admin Commands',
                value=
                f'''Create are some admin commands that server administrators and those with the needed perms can use to create things in your server. Both Parrot and the user running the command need the permission.'''
            )
            embedVar.add_field(name='List of Commands',
                               value=f'''
1)`{prefix}create role (role name)` - Create a role in the server. Manage Roles needed.
2)`{prefix}create channel (channel name)` - Create a channel in the server. Manage Channels needed. 
3)`{prefix}create category (category name)` - Create a category in the server. Manage Channels needed.
4)`{prefix}create logchannel` - Creates a channel in the server called #logging to log moderative action taken with Parrot. Will create a new channel even if an existing channel is named #logging. Manage Channels needed.
5)`{prefix}create suggestchannel` - Creates a channel in the server called #suggestions to send suggestions created with Parrot. Will create a new channel even if an existing channel is named #suggestions. Manage Channels needed.'''
                               )
            await message.channel.send(embed=embedVar)
        if action == 'suggestchannel':
            if message.author.guild_permissions.manage_channels or message.author.guild_permissions.administrator:
                try:
                    await message.guild.create_text_channel('suggestions')
                    await message.channel.send('Channel was created at top!')
                except:
                    await message.channel.send('Something went wrong!')
            else:
                await message.channel.send(
                    "You don't have the needed permissions.")
        if action == 'logchannel':
            if message.author.guild_permissions.manage_channels or message.author.guild_permissions.administrator:
                try:
                    await message.guild.create_text_channel('logging')
                    await message.channel.send('Channel was created at top!')
                except:
                    await message.channel.send('Something went wrong!')
            else:
                await message.channel.send(
                    "You don't have the needed permissions.")
        if action.startswith('role'):
            rolename = message.content[13:].format(message)
            if rolename == '':
                await message.channel.send('I need a rolename!')
            else:
                if message.author.guild_permissions.manage_roles or message.author.guild_permissions.administrator:
                    try:
                        role = await message.guild.create_role(
                            name=message.content[13:].format(message))
                        await message.channel.send(
                            f'Role **{role}** has been created in this server')
                    except:
                        await message.channel.send(
                            'The rolename has an issue. Or perhaps I do not have the manage roles permission'
                        )
                else:
                    await message.channel.send(
                        "You don't have the needed permissions.")
        if action.startswith('channel'):
            channelname = message.content[16:].format(message)
            if channelname == '':
                await message.channel.send('I need a channel name!')
            else:
                if message.author.guild_permissions.manage_channels or message.author.guild_permissions.administrator:
                    try:
                        guild = message.guild
                        channel = await guild.create_text_channel(channelname)
                        await message.channel.send(
                            f'Channel **{channel}** has been created in this server'
                        )
                    except:
                        await message.channel.send(
                            'The channel name has an issue. Or perhaps I do not have the manage channels permission'
                        )
                else:
                    await message.channel.send(
                        "You don't have the needed permissions.")
        if action.startswith('category'):
            channelname = message.content[17:].format(message)
            if channelname == '':
                await message.channel.send('I need a category name!')
            else:
                if message.author.guild_permissions.manage_channels or message.author.guild_permissions.administrator:
                    try:
                        guild = message.guild
                        category = await message.guild.create_category(
                            channelname)
                        await message.channel.send(
                            f'Category **{category}** has been created in this server'
                        )
                    except:
                        await message.channel.send(
                            'The category name has an issue. Or perhaps I do not have the manage channels permission'
                        )
                else:
                    await message.channel.send(
                        "You don't have the needed permissions.")
            #await message.guild.create_category('wap')
    if message.content == (prefix + 'invite'):
        embedVar = discord.Embed(title="Parrot Bot", color=0x00ff00)
        embedVar.add_field(
            name='Invite Link',
            value=
            '[Click Here](https://discord.com/api/oauth2/authorize?client_id=798943737208242237&permissions=8&scope=bot)'
        )
        await message.channel.send(embed=embedVar)
    if message.content == (prefix + 'rules'):
        embedVar = discord.Embed(title="Parrot Rules", color=0x00ff00)
        embedVar.add_field(
            name="By using parrot, you agree to follow all parrot rules",
            value=''' 
1. Do not use the bot for illegal activities or to harm anyone. Harming includes insulting, discriminating and swearing at people. 
2. Do not take advantages of any bugs. Please kindly report any bugs at the support server.
3. Do not hack the bot in any format.
4. Follow Discord Terms of Service while using the bot.
5. Refrain from spam bot commands. This may cause lagging or other unintended issues.

By following these rules, you'll allow future discord users to enjoy using me safely and happily! =)'''
        )
        await message.channel.send(embed=embedVar)
    if message.content == (prefix + 'support'):
        embedVar = discord.Embed(title="Parrot Bot", color=0x00ff00)
        embedVar.add_field(
            name='Support Server Invite Link',
            value=
            'Hey there! If you need further assistance, [click here](https://discord.gg/sqAy4fyd6t)'
        )
        await message.channel.send(embed=embedVar)
    if message.content.startswith(prefix + 'slowmode'):
        if message.content == (prefix + 'slowmode off'):
            if message.author.guild_permissions.kick_members or message.author.guild_permissions.manage_channels or message.author.guild_permissions.manage_messages:
                await message.channel.edit(slowmode_delay=0)
                await message.channel.send('Slowmode has been turned off!')
            else:
                await message.channel.send(
                    'Check your input again. Remember that the max is 6hrs (21600 seconds) and that only the input can be positive numbers (no decimals or negative numbers please).'
                )
        else:
            if message.author.guild_permissions.kick_members or message.author.guild_permissions.manage_channels or message.author.guild_permissions.manage_messages:
                try:
                    seconds = (message.content[9:].format(message))
                    await message.channel.edit(slowmode_delay=seconds)
                    await message.channel.send(
                        f"Set the slowmode in this channel to {seconds} seconds! Do {prefix}slowmode off to stop slowmode!"
                    )
                except:
                    await message.channel.send(
                        'Check your input again. Remember that the max is 6hrs (21600 seconds) and that only the input can be positive numbers (no decimals or negative numbers please).'
                    )
            else:
                await message.channel.send(
                    'Who are you to set slowmode? You can not do that with your perms.'
                )
    if message.content.startswith(prefix + 'server'):
        embedVar = discord.Embed(title='Server lookup', color=0x00ff00)
        embedVar.add_field(name="Server Name",
                           value=message.guild.name,
                           inline=False)
        embedVar.add_field(name="Server-Id",
                           value=int(message.guild.id),
                           inline=False)
        embedVar.add_field(name="Server Creation Date and Time",
                           value=message.guild.created_at,
                           inline=False)
        embedVar.add_field(name='Member Count',
                           value=(message.guild.member_count))
        embedVar.add_field(name='Owner', value=(message.guild.owner.mention))
        bot_message = await message.channel.send(embed=embedVar)
    if message.content.startswith(prefix + 'sus'):
        try:
            everyone = '@everyone'
            here = '@here'
            role = '<@&'
            xyz = message.content[5:].format(message)
            words = xyz.split()
            if everyone in words or here in words or role in words:
                await message.channel.send(
                    'No Everyone or Here Pings will work using Sus. I do not want to cause issues.'
                )
            else:
                await message.channel.send(
                    'Please wait. Calculating sus rating')
                await asyncio.sleep(int(1))
                if xyz == '':
                    await message.channel.send(
                        'Operation Failed Because No Input Was Identified!')
                else:
                    await message.channel.send(xyz + ' is ' +
                                               str(random.randint(0, 100)) +
                                               '% sus.')
        except:
            await message.channel.send(
                'Something is wrong! Maybe your input is too long?')
    if message.content.startswith(prefix + 'echo'):
        msg = message.content[5:].format(message)
        if msg == '':
            embedVar = discord.Embed(title="Parrot Bot", color=0x00ff00)
            embedVar.add_field(
                name="Echo Command",
                value=
                f'''Wanna echo a message but not say it yourself? Well, this is the command for you! Just echo a message and Parrot will echo it right in the channel. However, your user name will be attached in the echo because anonymous echo's can lead to some bad things.''',
                inline=False)
            embedVar.add_field(name='How To Run the Command',
                               value=f'{prefix}echo (Message Echoed)',
                               inline=False)
            await message.channel.send(embed=embedVar)
        else:
            try:
                embedVar = discord.Embed(title="Attention Everyone! ",
                                         color=0x00ff00)
                embedVar.add_field(name="A message from " +
                                   message.author.name,
                                   value=msg,
                                   inline=False)
                await message.channel.send(embed=embedVar)
                await message.delete()
            except:
                await message.channel.send(
                    'Something went wrong. Check if your input is valid to be sent as an input!'
                )
    if message.content == (prefix + 'vtest'):
        embedVar = discord.Embed(title="Parrot Bot", color=0x00ff00)
        embedVar.add_field(name="Help Command",
                           value=f'''__**Help Pages**__
Page 1: General Commands
Page 2: Research Commands
Page 3: Moderative Commands''',
                           inline=False)
        msg = await message.reply(
            type=InteractionType.ChannelMessageWithSource,
            embed=embedVar,
            content="Message Here",
            components=[[
                Button(style=ButtonStyle.blue, label='Page 1'),
                Button(style=ButtonStyle.blue, label='Page 2'),
                Button(style=ButtonStyle.blue, label='Page 3'),
                Button(style=ButtonStyle.red, label="Cancel"),
            ]])
        res = await client.wait_for("button_click")
        #async def on_button_click(interaction): #f
        if msg.label == 'Page 1':
            await message.channel.send('Button 1 Clicked')
    if message.content == prefix + 'help':
        page1 = discord.Embed(title='Page 1 - General and Research Commands',
                              description=f'''
**General Commands**
{prefix}info - Get information about Parrot
{prefix}help - Get information about all the commands available on Parrot users
{prefix}bug - Process to report a bug on Parrot
{prefix}vote - Vote for Parrot on top.gg
{prefix}ping - Response time to commands sent on Parrot
{prefix}support - Invite link to the Parrot Support Server
{prefix}invite - Invite Parrot to a guild that you own or have either Manage Server or Administrator Perms in
{prefix}rules - Parrot's rules
{prefix}qa - Answers to a few frequently asked questions about Parrot
{prefix}setup - Get more info on how to setup Parrot in your server

**Research Commands**
{prefix}profile - A few facts about your account
{prefix}server - Learn more about your server
{prefix}lookup (userid) - Lookup any user on Discord with their user id
{prefix}id (@mention) - Get the Discord ID of a user 
{prefix}perm - Check All the Permissions that you have in the Server/Channel

		''',
                              colour=0x00ff00)
        page1.set_footer(
            text=
            "There is a timeout of 75 seconds before the reactions no longer work! Use the arrow to scroll through Parrot's pages. There are 3 pages"
        )
        page2 = discord.Embed(
            title='Page 2 - Moderative And Administrative Commands',
            description=f'''
**Moderator Commands**
{prefix}purge (# of msgs) - Purge the number of messages in the guild
{prefix}warn (userid) (reason) - Warn a user
{prefix}kick (userid) (reason) - Kick a user
{prefix}ban (userid) (reason) - Ban a user 
{prefix}slowmode (# of seconds) - Set slowmode in a channel
{prefix}listbans - Get a list of all banned users in a guild

**Administrative Commands**
{prefix}create role (role name) - Create a role in the server. Manage Roles needed.
{prefix}create channel (channel name) - Create a channel in the server. Manage Channels needed. 
{prefix}create category (category name) - Create a category in the server. Manage Channels needed.
{prefix}create logchannel - Creates a channel in the server called #logging to log moderative action taken with Parrot. Will create a new channel even if an existing channel is named #logging. Manage Channels needed.
{prefix}create suggestchannel - Creates a channel in the server called #suggestions to send suggestions created with Parrot. Will create a new channel even if an existing channel is named #suggestions. Manage Channels needed.

		''',
            colour=0x00ff00)
        page3 = discord.Embed(title='Page 3 - Utility and Fun Commands',
                              description=f'''
**Utility and Fun Commands**
{prefix}poll (poll) - Create a yes/no poll
{prefix}suggest (suggestion) - Create a suggestion for the server
{prefix}sus (thing/person/place/anything) - Check how suspicious something is
{prefix}echo (message) - Echo a message
{prefix}timer (length in seconds) - Create a Timer on Parrot
{prefix}fight - Spawn and Fight the Great Parrot boss
{prefix}rng - Get a random number generated for you!
{prefix}cf - Flip a Creation

''',
                              colour=0x00ff00)

        pages = [page1, page2, page3]

        messagex = await message.channel.send(embed=page1)
        await messagex.add_reaction('◀')
        await messagex.add_reaction('▶')

        def check(reaction, user):
            return user == message.author

        i = 0
        reaction = ''

        while True:
            if str(reaction) == '◀':
                if i > 0:
                    i -= 1
                    await messagex.edit(embed=pages[i])
            elif str(reaction) == '▶':
                if i < 2:
                    i += 1
                    await messagex.edit(embed=pages[i])

            try:
                reaction, user = await client.wait_for('reaction_add',
                                                       timeout=80,
                                                       check=check)
                await messagex.remove_reaction(reaction, user)
            except:
                break
        await message.clear_reactions()

    if message.content.startswith(prefix + 'id'):
        uuid = (message.content[7:25].format(message))
        try:
            await client.fetch_user(uuid)
            embedVar = discord.Embed(title="Parrot Bot", color=0x00ff00)
            embedVar.add_field(name='User id',
                               value='The user id of the user is ' + uuid)
            await message.channel.send(embed=embedVar)
        except:
            await message.channel.send(
                f'Check your id again. Something seems off! The proper command format is {prefix}id (mention-user). For example, to get my id, run {prefix}id <@798943737208242237>'
            )
    if message.content.startswith(prefix + 'profile'):
        userEmbed = discord.Embed(colour=0x00ff00)
        userEmbed.set_author(
            name=
            f'User Name - {message.author.name}#{message.author.discriminator}',
            icon_url=f'{message.author.avatar_url}')
        userEmbed.add_field(name='User Id', value=f'{message.author.id}')
        userEmbed.add_field(name='User Account Creation Date',
                            value=f'{str(message.author.created_at)}')
        await message.channel.send(embed=userEmbed)
    if message.content == (prefix + 'guild invite'):
        try:
            if message.author.guild_permissions.administrator:
                link = await message.channel.create_invite(max_age=604800)
                await message.author.send(
                    "Here is an instant invite valid for 7 days to your server: "
                    + str(link))
                await message.channel.send(
                    'The server invite link has been sent to your private messages.'
                )
            else:
                await message.channel.send(
                    "For security concerns, the command is only available for people with the `administrator` permission."
                )
        except:
            await message.channel.send(
                'I am not allowed to create server invites. If this should not be the case, please contact a server staff member/owner.'
            )
    #if message.content == (prefix + 'guild invite clear'):
    #try:
    #invitess = print(await message.guild.invites())
    #ainvites == invitess.content
    #print(ainvites)
    #if message.author.guild_permissions.administrator:
    #for invite in message.guild.invites:
    #await invite.delete
    #await message.channel.send('All server invite are now void!')
    #else:
    #await message.channel.send("For security concerns, the command is only available for people with the `administrator` permission.")
    #except:
    #await message.channel.send('I am not allowed to void server invites. If this should not be the case, please contact a server staff member/owner.')
    if message.content.startswith(prefix + "timer"):
        #dmnotify = '-dms'
        #wordy = dmnotify.split()
        xtime = (message.content[7:].format(message))
        idx = str(random.randint(100000, 999999))
        if xtime == '':
            embedVar = discord.Embed(title="Parrot Bot", color=0x00ff00)
            embedVar.add_field(name='Timer Help',
                               value='''
		The timer is a built in parrot command that allows you to set a reminder in a period of time (maximum 10 minutes). To start, run the command followed by the # of seconds you want the timer to work for. Entering invalid inputs will result in an error msg.
		''')
            await message.channel.send(embed=embedVar)
        else:
            try:
                if int(xtime) < 601:
                    embedVar = discord.Embed(title="Your Timer Has Been Set",
                                             color=0x00ff00)
                    embedVar.add_field(name="Timer Length (In Seconds)",
                                       value=xtime)
                    embedVar.add_field(name="Timer ID", value=idx)
                    await message.channel.send(embed=embedVar)
                    await asyncio.sleep(int(xtime))
                    embedVar2 = discord.Embed(
                        title="Your Timer Has Been Completed", color=0x00ff00)
                    embedVar2.add_field(name="Timer Length (In Seconds)",
                                        value=xtime)
                    embedVar2.add_field(name="Timer ID", value=idx)
                    try:
                        await message.author.send(embed=embedVar2)
                    except:
                        fail = 'true'
                    try:
                        await message.channel.send(embed=embedVar2)
                        await message.channel.send(message.author.mention)
                    except:
                        fail2 = 'true'
                else:
                    await message.channel.send(
                        'Sorry, currently my timers only go up to 600 seconds (10 minutes). '
                    )
            except:
                await message.channel.send('Use a vaild number!')
    if message.content.startswith(prefix + 'listbans'):
        if message.author.guild_permissions.ban_members:
            bans = await message.guild.bans()
            try:
                if bans == []:
                    await message.channel.send('This server has no bans!')
                else:
                    output = "**User#Discriminator *(User Id)* : Ban Reason**\n"
                    for ban in bans:
                        output += f"{ban.user.name}#{ban.user.discriminator} *{ban.user.id}* : {ban.reason}\n"
                    await message.channel.send(output)
            except:
                await message.channel.send(
                    'Something went wrong. Make sure I have ban members!')
        else:
            await message.channel.send(
                'You are not a person with ban members permission.')
    if message.content.startswith(prefix + 'ban'):
        if message.author == message.guild.owner:
            try:
                userb = (message.content[4:23].format(message))
                reason = ((message.content[24:].format(message)))
                userc = await client.fetch_user(userb)
                await message.guild.ban(user=userc,
                                        reason='Banned by server owner',
                                        delete_message_days=0)
                success = await message.channel.send(
                    f'Successfully banned {userc.name}#{userc.discriminator} from the server. REASON: **{reason}**'
                )
                embedVar = discord.Embed(title="Parrot Bot Ban",
                                         color=0x00ff00)
                embedVar.add_field(name="Server",
                                   value=f'''
{message.author.guild}''',
                                   inline=False)
                embedVar.add_field(name="Moderator",
                                   value=message.author.mention,
                                   inline=False)
                embedVar.add_field(name="Banned User",
                                   value=f"{userc.name}#{userc.discriminator}",
                                   inline=False)
                embedVar.add_field(name="Reason", value=reason, inline=False)
                await message.channel.send(embed=embedVar)
                try:
                    await userc.send(embed=embedVar)
                except:
                    await success.edit(
                        f'Successfully banned {userc.name}#{userc.discriminator} from the server. Was not able to dm the user!'
                    )
                try:
                    lchannel = discord.utils.get(message.guild.text_channels,
                                                 name='logging')
                    await lchannel.send(embed=embedVar)
                except:
                    nologging = ('true')
                    print(nologging)
            except:
                await message.channel.send(
                    'I was not able to ban the user. Check the user id again and make sure my role is hoisted above the user.'
                )
        else:
            await message.channel.send(
                'Currently only the server owner can ban!')
    if message.content.startswith(prefix + 'kick'):
        if message.author == message.guild.owner:
            try:
                userb = (message.content[5:24].format(message))
                reason = ((message.content[25:].format(message)))
                userc = await client.fetch_user(userb)
                await message.guild.kick(user=userc,
                                         reason='Kicked by server owner')
                success = await message.channel.send(
                    f'Successfully kicked {userc.name}#{userc.discriminator} from the server. REASON: **{reason}**'
                )
                embedVar = discord.Embed(title="Parrot Bot Kick",
                                         color=0x00ff00)
                embedVar.add_field(name="Server",
                                   value=f'''
{message.author.guild}''',
                                   inline=False)
                embedVar.add_field(name="Moderator",
                                   value=message.author.mention,
                                   inline=False)
                embedVar.add_field(name="Kicked User",
                                   value=f"{userc.name}#{userc.discriminator}",
                                   inline=False)
                embedVar.add_field(name="Reason", value=reason, inline=False)
                await message.channel.send(embed=embedVar)
                try:
                    await userc.send(embed=embedVar)
                except:
                    await success.edit(
                        f'Successfully kicked {userc.name}#{userc.discriminator} from the server. Was not able to dm the user!'
                    )
                try:
                    lchannel = discord.utils.get(message.guild.text_channels,
                                                 name='logging')
                    await lchannel.send(embed=embedVar)
                except:
                    nologging = ('true')
                    print(nologging)
            except:
                await message.channel.send(
                    'I was not able to kick the user. Check the user id again and make sure my role is hoisted above the user.'
                )
        else:
            await message.channel.send(
                'Currently only the server owner can kick!')

    if message.content == prefix + 'qa':
        page1 = discord.Embed(title='Q/A Page 1/3',
                              description='''
		**I just got started on Parrot!**
		Welcome to Parrot. Run the help command to get more information about the commands. Run the info commands to learn a bit more about me. The support command would invite you to the Parrot Support Server, where you could interact with the Parrot Community and learn more about Parrot.

		**What Permissions does Parrot Require?**
		Administrator would allow Parrot to work flawlessly without any issues, though some servers may not like this. You may configure the settings yourself. Parrot requried read messages, send messages, view channels, send links and attach reactions for the basic commands to work. Other commands may need more perms.

		**What do I do if certain commands do not work?**
		Check if Parrot is online or if there is an announcement in the support server regarding Parrot. If not, check if Parrot has the right permissions. Run other commands to see if Parrot responds. If the troubleshooting does not give a reason, contact Parrot support and we would gladly assist you.


		''',
                              colour=0x00ff00)
        page2 = discord.Embed(title='Q/A Page 2/3',
                              description='''
		**There is a bug with Parrot. What do I do?**
		If you see a bug, please contact a member of Parrot staff immediately or report the bug to Parrot staff. We will investigate and attempt to resolve the issue. Please do not misuse the bug or spread the word about the bug to other users. Spreading the word may result in more people misuing the bug.

		**Someone is breaking the Parrot rules. What should I do?**
		If you notice someine breaking the rules, kindly tell them to not break the Parrot rules. If they keep breaking the rules or the rule broken is a major infraction, promptly contact a member of the Parrot Support Team so that immediate action can be taken. Punsihing rule-breakers will allow Parrot to continue helping other people on Discord.

		**I am having issues with all commands involving buttons/interactions. What do I do?**
		Make sure that Parrot is allowed to use applications and has all necessary perms/access. If this is not the case, please contact Parrot Support and we'll gladly assist you.
		''',
                              colour=0x00ff00)
        page3 = discord.Embed(title='Q/A Page 3/3',
                              description='''

		**Does Parrot store my user information?**
		Parrot's databases contain none of your information. For example, the information from lookup will be sent to you and not stored within the system. Parrot will only collect information about the bot performance and any issues that come along with this bot. Parrot will not collect and store chat messages or bot commands that you send, cause that is just wrong and its against the rules of Discord. Please also note that no information from Parrot will be given to a third party.

		**Does Parrot store guild information?**
		Currently, Parrot only stores the guild id of the guilds that Parot is in. This is to keep logs and for a future feature in which guilds can keep custom prefixes. The id is also stored so that support can be given faster when required. Only the guild id, nothing else.

		**I have an idea for Parrot. How do I suggest it?**
		We would love to hear your ideas! If you have an suggestion, tell your idea in the Parrot Support Server. We'll listen to your ideas and if we like it, your idea would become a feature on Parrot.
		''',
                              colour=0x00ff00)

        pages = [page1, page2, page3]

        messagex = await message.channel.send(embed=page1)
        await messagex.add_reaction('◀')
        await messagex.add_reaction('▶')

        def check(reaction, user):
            return user == message.author

        i = 0
        reaction = ''

        while True:
            if str(reaction) == '◀':
                if i > 0:
                    i -= 1
                    await messagex.edit(embed=pages[i])
            elif str(reaction) == '▶':
                if i < 2:
                    i += 1
                    await messagex.edit(embed=pages[i])

            try:
                reaction, user = await client.wait_for('reaction_add',
                                                       timeout=60.0,
                                                       check=check)
                await messagex.remove_reaction(reaction, user)
            except:
                break
        await message.clear_reactions()

    if message.content.startswith(prefix + 'perm'):
        try:
            await message.channel.send('Please wait!')
            await asyncio.sleep(1)
            embedVar = discord.Embed(
                title="Permissions For You In This Server", color=0x00ff00)

            if message.author.guild_permissions.read_messages:
                x7 = 'Enabled'
            else:
                x7 = 'Disabled'
            embedVar.add_field(name='Read Messages', value=x7)

            if message.author.guild_permissions.send_messages:
                x8 = 'Enabled'
            else:
                x8 = 'Disabled'
            embedVar.add_field(name='Send Messages', value=x8)

            if message.author.guild_permissions.add_reactions:
                x9 = 'Enabled'
            else:
                x9 = 'Disabled'
            embedVar.add_field(name='Add Reactions', value=x9)

            if message.author.guild_permissions.change_nickname:
                x10 = 'Enabled'
            else:
                x10 = 'Disabled'
            embedVar.add_field(name='Change Nickname', value=x10)

            if message.author.guild_permissions.manage_nicknames:
                x11 = 'Enabled'
            else:
                x11 = 'Disabled'
            embedVar.add_field(name='Manage Nicknames', value=x11)

            if message.author.guild_permissions.kick_members:
                x = 'Enabled'
            else:
                x = 'Disabled'
            embedVar.add_field(name='Kick Members', value=x)

            if message.author.guild_permissions.ban_members:
                x1 = 'Enabled'
            else:
                x1 = 'Disabled'
            embedVar.add_field(name='Ban Members', value=x1)
            if message.author.guild_permissions.manage_messages:
                x2 = 'Enabled'
            else:
                x2 = 'Disabled'
            embedVar.add_field(name='Manage Messages', value=x2)

            if message.author.guild_permissions.manage_roles:
                x3 = 'Enabled'
            else:
                x3 = 'Disabled'
            embedVar.add_field(name='Manage Roles', value=x3)

            if message.author.guild_permissions.manage_channels:
                x4 = 'Enabled'
            else:
                x4 = 'Disabled'
            embedVar.add_field(name='Manage Channels', value=x4)

            if message.author.guild_permissions.manage_nicknames:
                x5 = 'Enabled'
            else:
                x5 = 'Disabled'
            embedVar.add_field(name='Manage Nicknames', value=x5)

            if message.author.guild_permissions.administrator:
                x6 = 'Enabled'
            else:
                x6 = 'Disabled'
            embedVar.add_field(name='Administrator', value=x6)

            await message.channel.send(embed=embedVar)
        except:
            await message.channel.send(
                'An error occured! If this happens again, please **contact a member of the Parrot Team** in the Parrot support server.'
            )
    if message.content.startswith(prefix + 'warn'):
        thingy = ((message.content[5:].format(message)))
        if thingy == '':
            embedVar = discord.Embed(title="Parrot Bot", color=0x00ff00)
            embedVar.add_field(name="Warn Command",
                               value=f'''
Is there a user breaking the server rules. Well this is your command to fix that. Warning a user is a moderative punishment telling the user to stop. It's a good first punishment for minor crimes instead of kicking or banning.

**How to run** - {prefix}warn (user-id) (reason)
**Required Permissions** - Kick, Ban or Administrator
**Optional** - A Channel named #logging to log the warn in order to keep records of the warning''',
                               inline=False)
            await message.channel.send(embed=embedVar)
        else:
            if message.author.guild_permissions.kick_members or message.author.guild_permissions.ban_members or message.author.guild_permissions.administrator:
                try:
                    loi = await client.fetch_user((message.content[5:24]))
                    if loi == message.guild.owner:
                        await message.channel.send(
                            'You can not warn the server owner!')
                    else:
                        reason = ((message.content[25:].format(message)))
                        lchannel = discord.utils.get(
                            message.guild.text_channels, name='logging')
                        embedVar = discord.Embed(
                            title=f"Server Warning in {message.guild.name}",
                            color=0xFF0000)
                        embedVar.add_field(
                            name="Warned User",
                            value=f"{loi.mention} (id - {loi.id})",
                            inline=False)
                        if reason == '':
                            embedVar.add_field(name="Reason",
                                               value='No Reason Provided',
                                               inline=False)
                        else:
                            embedVar.add_field(name="Reason",
                                               value=reason,
                                               inline=False)
                        embedVar.add_field(name="Moderator",
                                           value=message.author.mention,
                                           inline=False)
                        await message.channel.send(embed=embedVar)
                        try:
                            await loi.send(embed=embedVar)
                        except:
                            try:
                                await message.channel.send(
                                    'Was not able to DM user')
                            except:
                                dmfail = 'true'
                                print(dmfail)
                                pass
                    try:
                        lchannel = discord.utils.get(
                            message.guild.text_channels, name='logging')
                        await lchannel.send(embed=embedVar)
                    except:
                        nologging = ('true')
                        print(nologging)
                except:
                    await message.channel.send(
                        'The user-id seems to lead to a non-existent person. Perhaps check your user id. Another result is that an unexpected failure occued. If the user-id is true, check settings/input again. Another solution is that the reason was too long?'
                    )
            else:
                await message.channel.send('Hey! You can not run the command.')
    if message.content == (prefix + 'fight'):
        try:
            decider = random.randint(1, 4)
            embedVar = discord.Embed(title="Parrot Bot", color=0x00ff00)
            embedVar.add_field(
                name="The Battle",
                value=
                '''You step into the arena and wait. You wait for hours and suddenly, a huge parrot flies into the arena. There are five options.
			
	**fight** - Try and Kill your opponent
	**run** - Run away from the Parrot
	**feed** - Feed the Parrot 
	**scream** - Scream as loud as you can
	**magic spell** - Try a Magic Spell you read about on the internet

	''',
                inline=False)
            embedVar.set_footer(
                text=
                "There is a timeout of 30 seconds. An invalid response or no response in 30 seconds will result in this process stopping!"
            )
            await message.channel.send(embed=embedVar)

            def check(m):
                return m.author == message.author

            res = await client.wait_for('message', timeout=30, check=check)
            # check = check calls the function check, the = check part can be any function that returns a booleen True/False
            selected = res.content
            if selected == 'fight':
                chance = random.randint(1, 100)
                if chance == 1:
                    await message.channel.send(
                        'You fight the giant. You were quite strong and defeated the Parrot. Good on you!'
                    )
                else:
                    await message.channel.send(
                        'You fight the Parrot by punching it. The Giant just steps on you and kill you.'
                    )
            elif selected == 'run':
                if decider == 1:
                    await message.channel.send(
                        'You run out of the arena. The parrot does not notice and your safely arrive home.'
                    )
                if decider == 2:
                    await message.channel.send(
                        'You run out of the arena. The parrot saw you running and lifted you with its beak. The parrot then somehow used its beak and threw you away. You land at the top of Mount Everest and die. At least you confused people all over the world about what happenned to you.'
                    )
                if decider == 3:
                    await message.channel.send(
                        'You run out of the arena. You were running so fast that you did not notice the cliff in front of you and fell into it. Your body was never recovered by anyone.'
                    )
                if decider == 4:
                    await message.channel.send(
                        'You run out of the arena. Parrot decides to help you out and lifts your car using its beak. It then puts it in front of you. You speed away. The worst thing that happenned to you was that you got a Speeding ticket.'
                    )
            elif selected == 'feed':
                if decider == 1:
                    await message.channel.send(
                        'You feed the Parrot with the cracker you found on the ground.The giant mistakens you for the cracker and eats you. You die being crushed by the beak.'
                    )
                else:
                    await message.channel.send(
                        'You feed the Parrot with the cracker you found on the ground. Suddenly, the parrot shrinks to normal size and flies away.'
                    )
            elif selected == 'scream':
                chance = random.randint(1, 10)
                if chance == 1:
                    await message.channel.send(
                        'You scream so loudly that a nearby army squad conducting drills hear you. They come and shoot the giant with Machine Guns. The Parrot stood no chance.'
                    )
                else:
                    await message.channel.send(
                        'Your scream was so loud that the Parrot HATED it! It bites your neck and you die of suffocation.'
                    )
            elif selected == 'magic spell':
                chance = random.randint(1, 10000)
                if chance == 1:
                    await message.channel.send(
                        'Your magic spell somehow **MAKES THE PARROT DISAPPEAR**. Wait, you never told me you were a magician. Or maybe you are superhuman. But HOW....'
                    )
                else:
                    await message.channel.send(
                        'The magic spell does nothing and you die because the stress of the spell not working caused a heart attack. You Died!'
                    )
            else:
                raise asyncio.exceptions.TimeoutError  # Redirects to below line.
        except asyncio.exceptions.TimeoutError:
            fail = 'No Response'
            await message.channel.send([
                "You do nothing for so long that the Parrot gets bored and flies away.",
                "You stand still for so long that the Parrot decides to step on you, kiling you instantly.",
                "You stared at the giant for so long that you died of dehydration.",
                "You do nothing for so long that the Parrot farts. The fart is so disgusting that you pass out. The next day, you get assasinated by a cat."
            ][decider - 1])
        except:
            await message.author.send(
                'An unexpected error occured when you sent the command. There was an issue sending the response. Please report this to the Parrot team at the support server so that we can fix this issue.'
            )
            raise  # Raises the error that started this except in console
    if message.content == (prefix + 'setup'):
        embedVar = discord.Embed(title="Parrot Bot", color=0x00ff00)
        embedVar.add_field(
            name="Setup Command",
            value=
            '''The Bot Requires Certain Channels in Order to allow the bot to fully work without issues.
		
1) A channel named #suggestions
Reason: For users to post suggestions in the server

2) A Channel named #logging
Reason: To log certain moderative actions

These channels are not mandatory. The only thing is that suggestions may not work or bot moderative actions may be logged.''',
            inline=False)
        await message.channel.send(embed=embedVar)

    if message.content.startswith(prefix + 'rng'):
        try:
            valuea = ((message.content[4:]))
            print(valuea)
            if valuea == '':
                embedVar = discord.Embed(title="Parrot Bot", color=0x00ff00)
                embedVar.add_field(
                    name="Random Number Generator",
                    value=
                    f'''Welcome to the random number generator, a command used to get a random integer between two positive or negative integers. To run this command, send the command {prefix}rng (first number). Then, Parrot will ask you for a second higher number. Finally, it will pick a random number and send it to you. There is a timeout of 19 seconds!`''',
                    inline=False)
                await message.channel.send(embed=embedVar)
            else:
                print('else')
                await message.channel.send('What is your second higher number?'
                                           )

                def check(m):
                    return m.author == message.author

                res = await client.wait_for('message', timeout=19, check=check)
                valueb = res.content
                try:
                    va = int(valuea)
                    vb = int(valueb)
                    rng = (random.randint(va, vb))
                    await message.channel.send('I pick ' + str(rng))
                except:
                    await message.channel.send(
                        'One of your values in invalid. Please try again! If you believe this is a bug, go to Parrot Support for further assistance!'
                    )
        except:
            await message.author.send(
                'An error occured! If this is because your values were wrong, please try again with proper integers. Or else, if both values were valid, please go to Parrot Support!'
            )
    if message.content.startswith(
            prefix + 'coinflip') or message.content.startswith(prefix + 'cf'):
        await message.channel.send('Flipping the coin!')
        await asyncio.sleep(3)
        flip = (random.randint(1, 2))
        if flip == 1:
            embedVar = discord.Embed(title="Parrot Bot Coin Flip",
                                     color=0x3498db)
            embedVar.add_field(name="HEADS",
                               value='You flipped heads',
                               inline=False)
            await message.channel.send(embed=embedVar)
        if flip == 2:
            embedVar = discord.Embed(title="Parrot Bot Coin Flip",
                                     color=0xf1c40f)
            embedVar.add_field(name="TAILS",
                               value='You flipped heads',
                               inline=False)
            await message.channel.send(embed=embedVar)
    if message.content.startswith(prefix + 'send'):  #recieves command
        loi = await client.fetch_user(
            (message.content[5:24]))  #content 5-24 is send
        await loi.send((message.content[25:]))
        await loi.send(message.author.mention + 'sent this')
        #done


#closing
keep_alive()
client.run(os.getenv('token'))
