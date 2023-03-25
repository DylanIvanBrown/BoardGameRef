import openai
import discord
import os
import repository
from dotenv import load_dotenv

# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
load_dotenv()
openAiKey = os.environ.get("OPEN_API_KEY")


client = discord.Client(intents=discord.Intents.default())


@client.event
async def on_ready():
    print(f'Logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    question = message.content

    # See PyCharm help at https://www.jetbrains.com/help/pycharm/
    openai.api_key = os.environ.get("OPEN_API_KEY")
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system",
                 "content": "You are a board game and card game assistant. Your role is to answer questions about "
                            "board-game and card game rules in a polite and helpful manner.Only answer questions "
                            "about board-games and card games, keep your responses strictly to that domain.Be clear "
                            "and succinct in your answers. Always put all of your response in the following format:["
                            "User intent;Game in question;Response]. for example [Player count; The Mind; The Mind is "
                            "a game for 2-4 players.]If you don't know about a game, respond with: [User intent;Game "
                            "in question;Sorry, that game is not within my knowledge base, I'll ask my developers to "
                            "teach me about it.] where the user intent is the intent from the user and the game in "
                            "question is the game the user was asking about. For example: [Game Inquiry;Star wars "
                            "deck-building game;Sorry, that game is not within my knowledge base, I'll ask my "
                            "developers to teach me about it.] If no game is mentioned then still respond in the "
                            "desired format."},
                {"role": "user", "content": question}
            ]
        )
        bot_response = response.choices[0].message.content

        if bot_response[0] == "[":
            bot_response = bot_response[1:-1]
        split_response = bot_response.split(";")
        if len(split_response) == 3:
            intent = split_response[0]
            game = split_response[1]
            response_to_user = split_response[2]
        else:
            response_to_user = "I didn't get the response I expected from my training, but this is what I do have for " \
                               "you: " + bot_response

        await repository.update_db_with_new_messages(message, intent, game, response_to_user)

        await message.channel.send(response_to_user)
    except openai.error.RateLimitError as exc:
        await message.channel.send("Rate limit exceeded. Please try again later.")
    except Exception as exc:
        await message.channel.send("Sorry I encountered an error. Please try again later.")


client.run(os.environ.get("DISCORD_KEY"))



