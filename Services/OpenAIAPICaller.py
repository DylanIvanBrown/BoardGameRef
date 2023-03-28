import os
import openai
from Models.BotResponse import BotResponse

class OpenAIAPICaller:
    """This is a class for calling the OpenAI API, in this context the default is gpt-4 and for boardgames and card
    games questions answering"""
    def __init__(self, model=None, system_prompt=None):
        self.api_key = os.environ.get("OPEN_API_KEY")
        if model is None:
            model = "gpt-4"
        openai.api_key = self.api_key
        if system_prompt is None:
            system_prompt = {"role": "system",
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
                                             "desired format. Whenever possible provide a reference for where in the "
                                             "rulebook you could find the answer you are giving"}

        self.model = model
        self.system_prompt = system_prompt

    def get_response(self, question, context=None):
        try:
            if context is None:
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        self.system_prompt,
                        {"role": "user", "content": question}
                    ]
                )
            else:
                response = openai.ChatCompletion.create(
                    model=self.model,
                    messages=[
                        self.system_prompt,
                        {"role": "user", "content": "We are talking about: " + context.current_game},
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
                message_model = BotResponse(intent, response_to_user, game)
                return message_model
            else:
                response_to_user = "I didn't get the response I expected from my training, but this is what I do have for " \
                                   "you: " + bot_response

        except openai.error.RateLimitError as exc:
            return BotResponse("ERROR", "Rate limit exceeded. Please try again later.")
