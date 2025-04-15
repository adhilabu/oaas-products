
from os import getenv

ELASTICSEARCH_URL: str = getenv('ELASTICSEARCH_URL', 'http://localhost:9200')
ELASTICSEARCH_API_KEY = getenv('ELASTICSEARCH_API_KEY')
ELASTICSEARCH_USERNAME: str = getenv('ELASTICSEARCH_USERNAME', 'elastic')
ELASTICSEARCH_PASSWORD: str = getenv('ELASTICSEARCH_PASSWORD', 'changeme')
ELASTICSEARCH_INDEX: str = getenv('ELASTICSEARCH_INDEX', 'product-recommendations')
ELASTICSEARCH_CERT_PATH: str = getenv('ELASTICSEARCH_CERT_PATH', 'http_ca.crt')