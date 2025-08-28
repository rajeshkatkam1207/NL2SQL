
\"\"\"Optional LangChain-based agent for multi-turn clarification.
This module will try to use langchain if installed. If not installed, it exposes a
fallback function that raises an informative error.
\"\"\"
from pathlib import Path

def is_langchain_available() -> bool:
    try:
        import langchain  # noqa: F401
        return True
    except Exception:
        return False

if is_langchain_available():
    from langchain.chat_models import ChatOpenAI
    from langchain.chains import ConversationChain
    from langchain.memory import ConversationBufferMemory

    def create_conversational_agent(api_key: str, model: str='gpt-4o'):
        # Create a simple conversational agent with memory for follow-up clarification.
        llm = ChatOpenAI(openai_api_key=api_key, model_name=model, temperature=0.0)
        memory = ConversationBufferMemory(memory_key='chat_history')
        conv = ConversationChain(llm=llm, memory=memory, verbose=False)
        return conv

    def ask_agent(agent, prompt: str) -> str:
        return agent.run(prompt)
else:
    def create_conversational_agent(api_key: str, model: str='gpt-4o'):
        raise RuntimeError('langchain is not installed. Install it to use the LangChain agent.')

    def ask_agent(agent, prompt: str) -> str:
        raise RuntimeError('langchain is not installed. Install it to use the LangChain agent.')
