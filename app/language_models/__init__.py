from typing import List

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory

from app.language_models.anthropic import model
from app.language_models.history.sqlite import get_session_history
from app.language_models.output_parsers.raw_posts_container import RawPostsContainer


prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You're a professional content writer who specialises in social media",
        ),
        (
            "human",
            "{format_instructions}\n"
            "Please do not use any other text in the response apart from the JSON object"
        ),
        MessagesPlaceholder(variable_name="history"),
        (
            "human",
            "{prompt}"
        ),
    ]
)

parser = JsonOutputParser(pydantic_object=RawPostsContainer)


chain = RunnableWithMessageHistory(
    prompt_template | model,
    get_session_history,
    input_messages_key="prompt",
    history_messages_key="history",
) | parser


def get_raw_posts(conversation_id: str, prompt: str, count: int) -> List[str]:
    raw_posts_container = chain.invoke(
        {
            'prompt': prompt,
            'format_instructions': parser.get_format_instructions(),
            'count': count
        },
        config={
            "configurable":
                {
                    "session_id": conversation_id
                }
        }
    )
    return raw_posts_container['posts']
