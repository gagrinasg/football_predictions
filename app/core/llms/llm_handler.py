from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

class LLMHandler:
    def __init__(self):
        self.model = ChatOpenAI(model_name="gpt-3.5-turbo")

    def _create_prompt_template(self):
        str_prompt = """
            This the prediction I get for a football match: {advice}

            Provide me with a message with emojis to post it to my telegram account for my followers to see.

            Example message:
            🔥🔥 Live Bet
            💯Double chance : draw or Celta Vigo
            ✅✅✅✅✅✅

            Try to avoid replicating the example message.
            Τry to use relevant hashtags.
        """

        prompt = ChatPromptTemplate.from_template(str_prompt)

        return prompt

    async def _create_message(self, advice):
        prompt = self._create_prompt_template()
        chain = prompt | self.model

        response = chain.invoke({'advice': advice})

        return response