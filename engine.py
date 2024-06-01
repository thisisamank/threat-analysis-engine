import json
from cloudtrail import CloudtrailClient
from mitre_attack_client import MitreAttackClient
from mapping import MitreCloudTrailMapping
import fastapi as FastAPI




class Engine:
    cloudtrail_client: CloudtrailClient
    mitre_attack_data: MitreAttackClient
    mitre_cloudtrail_mapping: MitreCloudTrailMapping

    def __init__(self):
        self.cloudtrail_client = CloudtrailClient(CLOUD_ID, ELASTIC_PASSWORD)
        self.mitre_attack_data = MitreAttackClient()
        self.mitre_cloudtrail_mapping = MitreCloudTrailMapping.init()

    def search(self, attack_id: str):
        technique = self.mitre_attack_data.get_object_by_attack_id(attack_id)
        query = self.mitre_cloudtrail_mapping.get_query_for_attack(attack_id)
        cloudtrail_logs_for_attack = self.cloudtrail_client.search("dyte-cloudtrail-30th-may", query)
        if cloudtrail_logs_for_attack:
            print(f"Found logs for {technique['name']} ({attack_id})")
            return {
                "technique": technique,
                "logs": cloudtrail_logs_for_attack
            }
        return {
            "technique": technique,
            "logs": []
        }


# if __name__ == "__main__":
#     engine = Engine()
#     attack_id = "T1134"
#     result = engine.search(attack_id)
#     print(result)

