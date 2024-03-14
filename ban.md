	if message.content.startswith (prefix + 'ban'):
			if message.author == message.guild.owner:
				try:
					userb = (message.content[4:23].format(message))
					reason = ((message.content[24:].format(message)))
					userc = await client.fetch_user(userb)
					await message.guild.ban(user = userc, reason = 'Banned by server owner', delete_message_days = 0)
					success = await message.channel.send(f'Successfully banned {userc.name}#{userc.discriminator} from the server. REASON: **{reason}**')
					embedVar = discord.Embed(title="Parrot Bot Ban", color=0x00ff00)
					embedVar.add_field(name = "Server", value=f'''
{message.author.guild}''', inline=False)
					embedVar.add_field(name = "Moderator", value=message.author.mention, inline=False)
					embedVar.add_field(name = "Banned User", value=f"{userc.name}#{userc.discriminator}", inline=False)
					embedVar.add_field(name = "Reason", value=reason, inline=False)
					await message.channel.send(embed = embedVar)
					try:
						await userc.send(f'You have been banned from {message.guild.name} by {userc.name}#{userc.discriminator}.')
					except:
						await success.edit(f'Successfully banned {userc.name}#{userc.discriminator} from the server. Was not able to dm the user!')
					try:
						lchannel = discord.utils.get(message.guild.text_channels, name = 'logging')
						await lchannel.send(embed = embedVar)	
					except:
						nologging = ('true')
						print(nologging)
				except:
					await message.channel.send('I was not able to ban the user. Check the user id again and make sure my role is hoisted above the user.')
			else:
				await message.channel.send('Currently only the server owner can ban!')