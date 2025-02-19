import concurrent.futures
from time import sleep

from openai import OpenAI


class OpenAiConnector:

    def __init__(
            self,
            api_key,
            model="gpt-4o-mini",
            embedding_model="text-embedding-3-small",
            system_message="You are a helpful assistant."
    ):
        self.embedding_model = embedding_model
        self.model = model
        self.system_message = system_message
        self.client = OpenAI(api_key=api_key)

    def text_completion(self, prompt):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": f"{self.system_message}"},
                {"role": "user", "content": f"{prompt}"},
            ],
        )
        return response.choices[0].message.content

    def embed(self, text):
        response = self.client.embeddings.create(
            input=text, model=self.embedding_model
        )
        return response.data[0].embedding


    def batch_embed(self, texts):
        def embed_text(text):
            return self.embed(text)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            sleep(0.2)
            embeddings = list(executor.map(embed_text, texts))

        return embeddings
