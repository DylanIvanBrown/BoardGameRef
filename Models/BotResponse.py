class BotResponse:
    """This is a class for tracking the user message, details about the bot understanding of the message, as well as
    the user response to the message. In the context of this project it tracks the intent of the message,
    the game the user is referring to and the response the bot is giving to the user message"""

    def __init__(self, intent: str, response_to_user: str, game="Unknown"):
        self.intent = intent
        self.game = game
        self.response_to_user = response_to_user

    def __str__(self):
        return f"MessageWithResponse(intent='{self.intent}', game='{self.game}', response_to_user='{self.response_to_user}')"
