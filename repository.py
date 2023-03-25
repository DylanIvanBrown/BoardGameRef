import mysql.connector
import os


async def update_db_with_new_messages(user_message, msg_intent, msg_game, bot_message):
    db_password = os.environ.get("DB_PASSWORD")

    mydb = mysql.connector.connect(
        host=os.environ.get("DB_HOST"),
        user=os.environ.get("DB_PASSWORD"),
        password=os.environ.get("DB_USER"),
        database=os.environ.get("DB_NAME")
    )

    cursor = mydb.cursor()
    user = user_message.author.id
    messages = user_message.content
    #sql = "INSERT INTO messages (userId, intent, game, userMessage, botResponse) VALUES (user, msg_intent, msg_game, messages, bot_message)"
    sql = "INSERT INTO messages (id, userId, intent, game, userMessage, botResponse) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (user_message.id, user, msg_intent, msg_game, messages, bot_message)
    #val = (user, msg_intent, msg_game, messages, bot_message)
    cursor.execute(sql, val)

    mydb.commit()

    print(cursor.rowcount, "record inserted.")
