import mysql.connector
import os

class Repository:

    def __init__(self):
        self.mydb = mysql.connector.connect(
            host=os.environ.get("DB_HOST"),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD"),
            database=os.environ.get("DB_NAME")
        )

    async def update_db_with_new_messages(self, user_message, msg_intent, msg_game, bot_message):
        cursor = self.mydb.cursor()
        user = user_message.author.id
        messages = user_message.content
        sql = "INSERT INTO messages (id, userId, intent, game, userMessage, botResponse) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (user_message.id, user, msg_intent, msg_game, messages, bot_message)
        cursor.execute(sql, val)

        self.mydb.commit()

        print(cursor.rowcount, "record inserted.")

    async def update_db_with_message_and_response(self, user_message, bot_response):
        msg_intent = bot_response.intent
        game = bot_response.game
        bot_message = bot_response.response_to_user

        await self.update_db_with_new_messages(user_message, msg_intent, game, bot_message)

    async def update_db_with_message_with_response(self, user_message, message_with_response):
        await self.update_db_with_new_messages(user_message, message_with_response.intent, message_with_response.game,
                                               message_with_response.response_to_user)
