	if message.content == prefix + 'help':
		page1 = discord.Embed(title = 'Page 1 - General and Research Commands', description = f'''
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

		''', colour = 0x00ff00)
		page2 = discord.Embed(title = 'Page 2 - Moderative And Administrative Commands', description = f'''
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

		''', colour = 0x00ff00)
		page3 = discord.Embed(title = 'Page 3 - Utility and Fun Commands', description = f'''
**Utility and Fun Commands**
{prefix}poll (poll) - Create a yes/no poll
{prefix}suggest (suggestion) - Create a suggestion for the server
{prefix}sus (thing/person/place/anything) - Check how suspicious something is
{prefix}echo (message) - Echo a message
{prefix}timer (length in seconds) - Create a Timer on Parrot
{prefix}fight - Spawn and Fight the Great Parrot boss

**Administrative Commands**
''', colour = 0x00ff00)
    
		pages = [page1, page2, page3]

		messagex = await message.channel.send(embed = page1)
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
					await messagex.edit(embed = pages[i])
			elif str(reaction) == '▶':
				if i < 2:
					i += 1
					await messagex.edit(embed = pages[i])

			try:
				reaction, user = await client.wait_for('reaction_add', timeout = 80, check = check)
				await messagex.remove_reaction(reaction, user)
			except:
				break
		await message.clear_reactions()