class Context:
    """This is a class for tracking the context of the conversation, so we can better answer the users questions"""

    def __int__(self, game: str, user_id: int, user_message: str):
        self.current_game = game
        self.last_user_message = user_message
        self.user_id = user_id

    def __str__(self):
        return f"Context(current_game='{self.current_game}', last_user_message='{self.last_user_message}', user_id={self.user_id})"
