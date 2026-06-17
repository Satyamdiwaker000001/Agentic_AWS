from sentence_transformers import SentenceTransformer

from config import MODEL_NAME


class EmbeddingModel:

    def __init__(self):

        self.model = SentenceTransformer(
            MODEL_NAME
        )

    def encode(self, text):

        return self.model.encode(text)