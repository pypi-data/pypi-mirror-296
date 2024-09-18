import numpy as np
import torch
from numpy.linalg import norm
from transformers import AutoModel, AutoTokenizer, DistilBertModel, DistilBertTokenizer

# let us think of a strategy we can use to generate embeddings for each sentence
# leveraging the power 2 models


class UniversalSentenceSearchReencoder:
    def __init__(self):
        self.distilbert_tokenizer = DistilBertTokenizer.from_pretrained(
            "distilbert-base-uncased"
        )
        self.distilbert_model = DistilBertModel.from_pretrained(
            "distilbert-base-uncased"
        )
        self.all_mini_tokenizer = AutoTokenizer.from_pretrained(
            "sentence-transformers/all-MiniLM-L6-v2"
        )
        self.all_mini_model = AutoModel.from_pretrained(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

    # next step we need to use all-minilm-l6-v2 to represent each word in the sentence
    def all_mini_representation(self, text_input):
        # we need to tokenize the text_input
        semantic_intputs = self.all_mini_tokenizer(
            text_input, return_tensors="pt", padding=True, truncation=True
        )
        # we then use distilbert to get the representation of the sentence
        with torch.no_grad():
            outputs = self.all_mini_model(**semantic_intputs)
            # we then get the pooled output (the [CLS] token embedding)
            sentence_embedding = outputs.last_hidden_state.mean(dim=1)  # Mean pooling
        return sentence_embedding

    # next we use distilbert to represent the full sentence
    def distilbert_representation(self, text_input):
        # we need to tokenize the text_input
        semantic_intputs = self.distilbert_tokenizer(
            text_input, return_tensors="pt", padding=True, truncation=True
        )
        # we then use distilbert to get the representation of the sentence
        with torch.no_grad():
            outputs = self.distilbert_model(**semantic_intputs)
            # we then get the pooled output (the [CLS] token embedding)
            sentence_embedding = outputs.last_hidden_state.mean(dim=1)  # Mean pooling
        return sentence_embedding

    # now we can combine the representations of the sentence and each word
    def combine_and_compress(
        self,
        sentence_embedding,
        all_mini_embedding,
    ):
        # we can use the mean of the vectors to represent the sentence
        # this is a simple way to compress the vectors into a single vector
        combined_vector = torch.cat(
            [sentence_embedding.flatten(), all_mini_embedding.flatten()], dim=0
        )
        return combined_vector

    def generate_embeddings(self, text_input):
        # Ensure vectors are of the same shape before concatenation
        all_mini_embedding = self.all_mini_representation(text_input)

        sentence_embedding = self.distilbert_representation(text_input)
        # get the combined vector
        combined_vector = self.combine_and_compress(
            sentence_embedding, all_mini_embedding
        )

        return combined_vector

    def decompress_embeddings(self, vector):
        distilbert_dim = 768
        all_mini_dim = 384
        # Extract DistilBERT and All MiniLM vectors
        distilbert_vector = vector[:distilbert_dim]
        all_mini_vector = vector[distilbert_dim : distilbert_dim + all_mini_dim]

        return distilbert_vector, all_mini_vector

    def calculate_cosine_similarity(self, vector1, vector2):
        # Calculate cosine similarity between two distilbert vectors
        vector1 = np.array(vector1).flatten()
        vector2 = np.array(vector2).flatten()

        # Compute cosine similarity
        return np.dot(vector1, vector2) / (norm(vector1) * norm(vector2))

    def safe_cosine_similarity(self, vector1, vector2):
        if np.linalg.norm(vector1) == 0 or np.linalg.norm(vector2) == 0:
            return 0  # or return a default value like 0.5 for neutral similarity
        return np.dot(vector1, vector2) / (
            np.linalg.norm(vector1) * np.linalg.norm(vector2)
        )

    def cosine_similarity(self, query_embedding, document_embedding, alpha=0.5):
        query_distilbert_vector, query_all_mini_vector = self.decompress_embeddings(
            query_embedding
        )
        # Decompress document embeddings into DistilBERT and All MiniLM parts
        doc_distilbert_vector, doc_all_mini_vector = self.decompress_embeddings(
            document_embedding
        )
        # Calculate cosine similarity for both DistilBERT and All MiniLM vectors
        distilbert_similarity = self.safe_cosine_similarity(
            query_distilbert_vector, doc_distilbert_vector
        )
        all_mini_similarity = self.safe_cosine_similarity(
            query_all_mini_vector, doc_all_mini_vector
        )

        # Combine scores with weighting (alpha for DistilBERT, 1-alpha for All MiniLM)
        combined_similarity = (
            alpha * all_mini_similarity + (1 - alpha) * distilbert_similarity
        )

        return combined_similarity
