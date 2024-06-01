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
    
    def fetch_all_events(self, index: str, page_size: int = 1000):
        all_events = []
        query = {
            "match_all": {}
        }

        search_after = None
        while True:
            body = {
                "size": page_size,
                "query": query,
                "sort": [
                    {"@timestamp": "asc"}  
                ]
            }
            
            if search_after:
                body["search_after"] = search_after
            
            results = self.search(index, body)
            if not results:
                break

            all_events.extend(results)
            search_after = results[-1].get("sort")

        return all_events


