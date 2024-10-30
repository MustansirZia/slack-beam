import os

from langchain_anthropic import ChatAnthropic

model = ChatAnthropic(model=os.environ.get('ANTHROPIC_MODEL_NAME', 'claude-3-5-sonnet-20241022'))


