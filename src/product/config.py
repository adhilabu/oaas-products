from elasticsearch import AsyncElasticsearch, Elasticsearch
from sentence_transformers import SentenceTransformer

from src.product.constants import ELASTICSEARCH_PASSWORD, ELASTICSEARCH_USERNAME, ELASTICSEARCH_URL


asy_es = AsyncElasticsearch(
    hosts=[ELASTICSEARCH_URL],
    basic_auth=(ELASTICSEARCH_USERNAME, ELASTICSEARCH_PASSWORD),
    verify_certs=False,
    timeout=30,
    retry_on_timeout=True,
    max_retries=3,
)

es = Elasticsearch(
    hosts=[ELASTICSEARCH_URL],
    basic_auth=(ELASTICSEARCH_USERNAME, ELASTICSEARCH_PASSWORD),
    verify_certs=False,
    timeout=30,
    retry_on_timeout=True,
    max_retries=3,
)


es.info()

# Initialize Sentence Transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')