from inspect import getmembers, isfunction

import discord

from . import oliver_commands
from .oliver_storage import OliverStorage

class OliverTheBot(discord.Client):
    """OliverTheBot discord client."""
    message_prefix = "!"

    def __init__(self, *args, **kwargs):
        # State intents.
        intents = discord.Intents.default()
        intents.members = True
        intents.typing = False
        intents.presences = False
        kwargs["intents"] = intents

        super().__init__(*args, **kwargs)

        # Init cold storage.
        self.storage = OliverStorage()

        # Init chat commands.
        self.message_commands = {}
        for (name, func) in getmembers(oliver_commands, isfunction):
            self.message_commands[name] = func

    def print_init_message(self):
        print('We have logged in as {0.user}'.format(self))

    async def on_ready(self):
        self.print_init_message()

    async def on_message(self, message):
        # Ignore any messages from ourselves.
        if message.author == self.user:
            return
        
        msg = message.content

        # Ignore any messages not starting with the prefix.
        if not msg.startswith(self.message_prefix):
            return
        msg = msg[1:].split(' ')   # Cut off the prefix and split into args.

        # Run the command (or nop).
        command = self.message_commands.get(
            msg[0],
            lambda *args, **kwargs: None)
        command(self, msg, raw_message=message)

# george_id = 151036859634417664

# class BotState:
#     client_token = '<REPLACE>'

#     # ID for Memers and Wieners guild.
#     memer_guild_id = 229457808695885824

#     # ID for bot test channel.
#     bot_channel_id = 788574134325215262

#     # Will be assigned to Memers and Wieners guild.
#     memer_guild = None

#     # Will be assigned to bot channel.
#     bot_channel = None

#     # Voice channels which the bot will not look in for online users.
#     blacklisted_voice_channels = set([394285191205748736])    # AFQue?

# def setup_client(bot, bot_state, cold_storage):
#     @bot.event
#     async def on_ready():
#         # Init global variable dependent on bot init.
#         bot_state.memer_guild = bot.get_guild(bot_state.memer_guild_id)
#         bot_state.bot_channel = bot.get_channel(bot_state.bot_channel_id)

#         print('We have logged in as {0.user}'.format(bot))

#         @tasks.loop(seconds=cold_storage.data["posture_notice_time_seconds"])
#         async def posture_check():
#             voice_users = get_all_users_in_voice_chat(bot, bot_state)
#             users_to_message = []
#             for user in voice_users:
#                 if user.id not in cold_storage.data["mention_blacklist"]:
#                     users_to_message.append(user)
            
#             if len(users_to_message) == 0:
#                 return
        
#             mention_text = " ".join([user.mention for user in users_to_message])
#             mention_text += " fix your posture"
#             await bot_state.bot_channel.send(mention_text)
        
#         posture_check.start()

#     @bot.event
#     async def on_message(message):
#         if message.author == bot.user:
#             return

#         if message.content.startswith('!posture_toggle'):
#             if message.author.id in cold_storage.data["mention_blacklist"]:
#                 cold_storage.data["mention_blacklist"].remove(message.author.id)
#                 await message.channel.send("You will now receive posture notifications")
#             else:
#                 cold_storage.data["mention_blacklist"].append(message.author.id)
#                 await message.channel.send("You wont get posture notifications anymore")
#             cold_storage.save_data()
#         elif message.content.startswith('!posture_settime'):
#             if message.author.id == george_id:
#                 args = message.content.split(" ")
#                 if len(args) <= 1:
#                     await message.channel.send("Need to provide a time in seconds.")
#                     return
#                 time = args[1]
#                 try:
#                     time = int(time)
#                 except:
#                     await message.channel.send("Invalid time.")

# def get_all_users_in_voice_chat(bot, bot_state):
#     users_in_voice_channels = []

#     for vchannel in bot_state.memer_guild.voice_channels:
#         if vchannel.id not in bot_state.blacklisted_voice_channels:
#             users_in_voice_channels += vchannel.members

#     return users_in_voice_channels
