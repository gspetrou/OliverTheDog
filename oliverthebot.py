import os
import json
from typing import Optional, Any
import discord
from discord.ext import tasks

george_id = 151036859634417664

class ColdStorageData:
    file_path = "./oliver_data.json"
    template = {
        "posture_notice_time_seconds": 1800,    # 30 minutes
        "mention_blacklist": []
    }

    data: dict = None

    def save_data(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.data, file)
    
    def init_from_template_if_not_exists(self):
        if not os.path.exists(self.file_path) or os.path.getsize(self.file_path) == 0:
            with open(self.file_path, 'w') as file:
                json.dump(self.template, file)
    
    def load_data(self):
        cold_storage_data = None
        with open(self.file_path, 'r+') as file:
            cold_storage_data = json.load(file)
        
        if not cold_storage_data:
            raise RuntimeError("Couldn't load/create cold storage file.")

        return cold_storage_data

    def __init__(self):
        self.init_from_template_if_not_exists()
        self.data = self.load_data()

class BotState:
    client_token = 'Nzg4NTc1MzA0MzMxNDI3ODQw.X9lf-w.BEWlc_LDWIrpu2dWT4oWsWySdGc'

    # ID for Memers and Wieners guild.
    memer_guild_id = 229457808695885824

    # ID for bot test channel.
    bot_channel_id = 788574134325215262

    # Will be assigned to Memers and Wieners guild.
    memer_guild = None

    # Will be assigned to bot channel.
    bot_channel = None

    # Voice channels which the bot will not look in for online users.
    blacklisted_voice_channels = set([394285191205748736])    # AFQue?

def setup_client(bot, bot_state, cold_storage):
    @bot.event
    async def on_ready():
        # Init global variable dependent on bot init.
        bot_state.memer_guild = bot.get_guild(bot_state.memer_guild_id)
        bot_state.bot_channel = bot.get_channel(bot_state.bot_channel_id)

        print('We have logged in as {0.user}'.format(bot))

        @tasks.loop(seconds=cold_storage.data["posture_notice_time_seconds"])
        async def posture_check():
            voice_users = get_all_users_in_voice_chat(bot, bot_state)
            users_to_message = []
            for user in voice_users:
                if user.id not in cold_storage.data["mention_blacklist"]:
                    users_to_message.append(user)
            
            if len(users_to_message) == 0:
                return
        
            mention_text = " ".join([user.mention for user in users_to_message])
            mention_text += " fix your posture"
            await bot_state.bot_channel.send(mention_text)
        
        posture_check.start()

    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return

        if message.content.startswith('!posture_toggle'):
            if message.author.id in cold_storage.data["mention_blacklist"]:
                cold_storage.data["mention_blacklist"].remove(message.author.id)
                await message.channel.send("You will now receive posture notifications")
            else:
                cold_storage.data["mention_blacklist"].append(message.author.id)
                await message.channel.send("You wont get posture notifications anymore")
            cold_storage.save_data()
        elif message.content.startswith('!posture_settime'):
            if message.author.id == george_id:
                args = message.content.split(" ")
                if len(args) <= 1:
                    await message.channel.send("Need to provide a time in seconds.")
                    return
                time = args[1]
                try:
                    time = int(time)
                except:
                    await message.channel.send("Invalid time.")

def get_all_users_in_voice_chat(bot, bot_state):
    users_in_voice_channels = []

    for vchannel in bot_state.memer_guild.voice_channels:
        if vchannel.id not in bot_state.blacklisted_voice_channels:
            users_in_voice_channels += vchannel.members

    return users_in_voice_channels

def main():
    # State we intend to use member data.
    intents = discord.Intents.default()
    intents.members = True
    intents.typing = False
    intents.presences = False

    # Init cold storage.
    cold_storage = ColdStorageData()

    # Create the bot.
    bot_state = BotState()
    bot = discord.Client(intents=intents)
    setup_client(bot, bot_state, cold_storage)
    bot.run(bot_state.client_token)

if __name__ == "__main__":
    main()