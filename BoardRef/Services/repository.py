import mysql.connector
import os

from Models.Context import Context


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
        date_time = user_message.created_at
        sql = "INSERT INTO messages (id, userId, intent, game, userMessage, botResponse, timeStamp) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (user_message.id, user, msg_intent, msg_game, messages, bot_message, date_time)
        cursor.execute(sql, val)

        self.mydb.commit()

        context = Context(user_id=user, game=msg_game, user_message=messages)
        await self.upsert_context(context)

        print(cursor.rowcount, "record inserted.")

    async def update_db_with_message_and_response(self, user_message, bot_response):
        msg_intent = bot_response.intent
        game = bot_response.game
        bot_message = bot_response.response_to_user

        await self.update_db_with_new_messages(user_message, msg_intent, game, bot_message)

    async def update_db_with_message_with_response(self, user_message, message_with_response):
        await self.update_db_with_new_messages(user_message, message_with_response.intent, message_with_response.game,
                                               message_with_response.response_to_user)

    async def get_context(self, user_id):
        cursor = self.mydb.cursor()
        sql = "SELECT * FROM context WHERE user_id = %s"
        val = (user_id,)
        cursor.execute(sql, val)
        result = cursor.fetchone()
        if result is None:
            return None
        else:
            context = Context(result[0], result[1], result[2])
            return context

    async def upsert_context(self, new_context):
        cursor = self.mydb.cursor()
        sql = "INSERT INTO context (user_id, game, last_user_message) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE game=%s, last_user_message=%s"
        val = (new_context.user_id, new_context.current_game, new_context.last_user_message, new_context.current_game, new_context.last_user_message)
        cursor.execute(sql, val)
        self.mydb.commit()

