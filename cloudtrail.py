from elasticsearch import Elasticsearch
import json

class CloudtrailClient:
    cloud_id: str
    elastic_password: str
    client: Elasticsearch

    def __init__(self, cloud_id: str, elastic_password: str):
        self.cloud_id = cloud_id
        self.elastic_password = elastic_password
        self.client = Elasticsearch(
            cloud_id=cloud_id,
            basic_auth=("elastic", elastic_password)
        )
    
    def search(self, index: str, query: dict):
        print(f"Searching in index {index} with query {query}")
        results = self.client.search(index=index, query=query)
        return results.body.get("hits", {}).get("hits", [])


