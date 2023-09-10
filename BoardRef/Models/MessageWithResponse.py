from datetime import datetime

class MessageWithResponse:
    """This is a class for tracking the user message, details about the bot understanding of the message, as well as
    the user response to the message."""

    def __init__(self, intent: str, game: str, response_to_user: str, user_id: int, timestamp: datetime = None):
        self.intent = intent
        self.game = game
        self.response_to_user = response_to_user
        self.user_id = user_id
        self.timestamp = timestamp if timestamp is not None else datetime.now()

    def __str__(self):
        return f"MessageWithResponse(intent='{self.intent}', game='{self.game}', response_to_user='{self.response_to_user}', user_id={self.user_id}, timestamp={self.timestamp})"
