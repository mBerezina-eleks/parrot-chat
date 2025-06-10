import os
from dotenv import load_dotenv

load_dotenv()

openai_api_key = os.environ.get("OPENAI_API_KEY")
azure_endpoint = os.environ.get("AZURE_ENDPOINT")
openai_api_type = os.environ.get("OPENAI_API_TYPE")
deployment_name = os.environ.get("DEPLOYMENT_NAME")
openai_api_version = os.environ.get("OPENAI_API_VERSION")
embedding_deployment_name = os.environ.get("EMBEDDING_DEPLOYMENT_NAME")