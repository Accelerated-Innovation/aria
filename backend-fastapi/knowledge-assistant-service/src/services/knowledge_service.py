import os
import requests
from dotenv import load_dotenv
from src.utils.langchain_imports import ChatOpenAI, ChatPromptTemplate


load_dotenv()

class KnowledgeService:
    def __init__(self):
        self.rewards_query_service_url = os.getenv("REWARDS_QUERY_SERVICE_URL")
        self.llm = ChatOpenAI(model=os.getenv("CHAT_MODEL"))

        self.prompt_template = ChatPromptTemplate.from_template("""
            You are an assistant for question-answering tasks.
            Use the following pieces of retrieved context to answer the question.
            If you don't know the answer, just say that you don't know.
            Use three sentences maximum and keep the answer concise.
            Question: {question}
            Context: {context}
            Answer:
        """)

    def get_context(self, query: str):
        """
        Get context from the rewards query service using the original query text.
        The rewards-query-service will handle embedding generation internally.
        """
        response = requests.post(
            f"{self.rewards_query_service_url}/rewards/query",
            json={"query": query, "top_k": 3},
            timeout=10
        )
        response.raise_for_status()
        return response.json()["results"]

    def generate_answer(self, question: str, context: list[dict]):
        formatted_context = "\n".join([item["content"] for item in context])

        prompt = self.prompt_template.format_messages(question=question, context=formatted_context)
        result = self.llm.invoke(prompt)

        return result.content.strip()

    def answer_question(self, question: str):
        context = self.get_context(question)
        return self.generate_answer(question, context)
