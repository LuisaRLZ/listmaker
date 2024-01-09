from discord.ext import commands
import os
import discord
import asyncio
#from keep_alive import keep_alive

from tokencito import TOKEN

intents = discord.Intents.all()
client = commands.Bot(command_prefix='.', intents=intents)
bot = client

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('Use .list anywhere'))

@client.command()
async def listhelp(ctx):
    embed = discord.Embed(
        title="Maze List Help",
        description="To create a list, please join a voice channel and type `.list` to make a maze list.\n\nIf you instead prefer the old version of list making, please use `.list2`",
        color=0x0DF6EB
    )
    embed.add_field(
        name="Invite the Bot",
        value="Use code `.invite` to invite this Bot to your Discord Server!",
        inline=False
    )
    embed.set_footer(text="Code made and hosted by LuisaRLZ")

    print(f"listhelp command used by: {ctx.author.name}")
    await ctx.send(embed=embed)

@client.command()
async def list(ctx):
    if not ctx.author.voice:
        return await ctx.send('👈 Please join a voice channel first then try again')

    channel = ctx.author.voice.channel
    members = channel.members
    original_names = {member.id: member.display_name for member in members}

    embed = discord.Embed(title="Maze List by Luisa RLZ", color=0x0DF6EB)
    information_line = (
        "**React 🖐️ to get added if you assisted but missed in the list. ❌ To remove yourself. You got 1 hour. Use `.list2` for a list without emoji. Use `.invite` to add this bot to your server.**"
    )
    embed.description = (
        f"{information_line}\n\n**Members:**\n" + '\n'.join(original_names.values()) + "\n\n**----DROPS----**"
    )

    # Send the initial message with the list
    print(original_names)
    print(f"list command used by: {ctx.author.name}")
    msg = await ctx.send(embed=embed)

    # Add the emoji to the message (changed to 🖐️ and ❌)
    await msg.add_reaction("🖐️")
    await msg.add_reaction("❌")

    # Allow continuous updates until a certain condition is met
    while True:
        try:
            # Wait for a reaction or a message with a 1-hour timer
            reaction, user = await client.wait_for('reaction_add', timeout=3600.0)
        except asyncio.TimeoutError:
            break  # Exit the loop if the timeout occurs
        else:
            if str(reaction.emoji) == '🖐️':
                # Add the new name to the original list with the 🖐️ emoji
                original_names[user.id] = f"{ctx.guild.get_member(user.id).display_name} 🖐️"
            elif str(reaction.emoji) == '❌':
                # Handle self-removal reaction
                original_names.pop(user.id, None)

            # Check if the reaction corresponds to the original message
            if reaction.message.id == msg.id:
                # Concatenate the information line, original names, and drops line
                updated_description = (
                    f"{information_line}\n\n**Members:**\n" + '\n'.join(original_names.values()) + "\n\n**----DROPS----**"
                )

                # Edit the original message with the updated list
                embed.description = updated_description
                await msg.edit(embed=embed)

                # await ctx.send(f"List updated with reactions within 1 hour.")

@client.command()
async def list2(ctx):
    if not ctx.author.voice:
        return await ctx.send('👈 Please join a voice channel first then try again')

    channel = ctx.author.voice.channel
    members = channel.members
    memids = [member.display_name for member in members]

    embed = discord.Embed(title="Maze List by Luisa RLZ", color=0x0DF6EB)
    embed.add_field(name="Members:", value='\n'.join(memids), inline=False)
    embed.add_field(name=" ", value="**----DROPS----**", inline=False)

    print(memids)
    print(f"list2 command used by: {ctx.author.name}")
    await ctx.send(embed=embed)

@client.command(name='invite', aliases=['inviteme','invitebot'])
async def invite(ctx):
    invite = discord.Embed(
        title="Invite Me!",
        url=
"https://discord.com/api/oauth2/authorize?client_id=907027337957244988&permissions=8&scope=bot%20applications.commands",
        description=
        "Invite this bot to your Discord Server! You must have inviting permissions. Use `.listhelp` to check out my commands. Also, Invite more useful Bots by [Clicking Here](https://docs.google.com/document/d/1tP7GZiIsLEsTiMTSppM6CwLzo8x8iiHiSl9ikStR3w4/edit?usp=sharing).",
        color=0x0DF6EB)
    invite.set_author(name="Invite this Bot",
                         url="https://discord.com/api/oauth2/authorize?client_id=907027337957244988&permissions=8&scope=bot%20applications.commands",
                         icon_url="https://i.imgur.com/OyBKQAF.png")
    invite.set_thumbnail(url="https://i.imgur.com/OyBKQAF.png")
    invite.add_field(
        name="Invite Link:",
        value=
        "[Click Here](https://discord.com/api/oauth2/authorize?client_id=907027337957244988&permissions=8&scope=bot%20applications.commands)",
        inline=False)
    invite.set_footer(
        text=
        "If you've got any doubt or suggestion on this bot, please message me @luisarlz"
    )
    print(f"invite command used by: {ctx.author.name}")
    await ctx.send(embed=invite)

#try:
    #keep_alive()
client.run(TOKEN)
#except Exception:
    #os.system('kill 1')