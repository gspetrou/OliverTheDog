import os

from oliverthebot import OliverTheBot

# Name of local file containning client token.
CLIENT_TOKEN_FILE_NAME = "./client_token"

# Name of environment variable containning client token.
CLIENT_TOKEN_ENV_VAR_NAME = "OLIVER_THE_BOT_DISCORD_CLIENT_TOKEN"

def get_client_token():
    """Attempts to get the client token. First checks for a local file, then
    checks for an environment variable, then throws a Runetime error is none is
    found."""

    if os.path.exists(CLIENT_TOKEN_FILE_NAME):
        with open(CLIENT_TOKEN_FILE_NAME, 'r+') as file:
            return file.read().strip()

    if CLIENT_TOKEN_ENV_VAR_NAME in os.environ:
        return os.environ[CLIENT_TOKEN_ENV_VAR_NAME]

    raise RuntimeError("No client token found.")

if __name__ == "__main__":
    oliver_the_bot = OliverTheBot()
    oliver_the_bot.run(get_client_token())