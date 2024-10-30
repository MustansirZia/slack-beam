from langchain_community.chat_message_histories import SQLChatMessageHistory

from app.storage.engines.sqlite import engine


def get_session_history(session_id: str):
    return SQLChatMessageHistory(session_id=session_id, connection=engine)
