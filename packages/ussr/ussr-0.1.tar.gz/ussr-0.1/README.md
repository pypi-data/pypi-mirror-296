# Universal Sentence Search Reencoder

A combined multi-model semantic sentence encoder

## Installation

You can install the library by cloning the repository and using the `setup.py` script.

```bash
pip install ussr
```

```bash
git clone https://github.com/yourusername/ussr.git
cd ussr
pip install .
```

## Usage

```python
from ussr.reencoder import UniversalSentenceSearchReencoder

reencoder = UniversalSentenceSearchReencoder()
# define a query and a corpus
query = "I want to bake a cake"

corpus = [
    "Today is a good day to bake a cake 🥳",
    "I am very happy today",
    "I would love to take a walk in the park",
]
# Generate embeddings for the query
query_embedding = reencoder.generate_embeddings(query)

# Generate embeddings for each sentence in the corpus
for sentence in corpus:
    embedding = reencoder.generate_embeddings(sentence)
    # Calculate cosine similarity between the query and the sentence
    similarity = reencoder.cosine_similarity(query_embedding, embedding)
    print(f"Similarity: {similarity}")
```
