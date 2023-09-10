import openai
import discord
import os
from dotenv import load_dotenv
from Services.OpenAIAPICaller import OpenAIAPICaller
from Services.repository import Repository

# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
load_dotenv()

client = discord.Client(intents=discord.Intents.default())


@client.event
async def on_ready():
    print(f'Logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    print(message.content)
    open_ai_caller = OpenAIAPICaller()
    repo = Repository()
    question = message.content

    # See PyCharm help at https://www.jetbrains.com/help/pycharm/
    openai.api_key = os.environ.get("OPEN_API_KEY")
    try:
        context = await repo.get_context(message.author.id)

        bot_response = open_ai_caller.get_response(question, context)

        await repo.update_db_with_message_and_response(message, bot_response)

        await message.channel.send(bot_response.response_to_user)
    except Exception as exc:
        await message.channel.send("Sorry I encountered an error. Please try again later.")


client.run(os.environ.get("DISCORD_KEY"))
