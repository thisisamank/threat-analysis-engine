from typing import Dict, List, Any

class MitreCloudTrailMapping:
    query: Dict[str, Any]
    mitre_attack_id: str
    attacks: List['MitreCloudTrailMapping']

    def __init__(self, query: Dict[str, Any], mitre_attack_id: str):
        self.query = query
        self.mitre_attack_id = mitre_attack_id
        self.attacks = []

    def add_attack(self, attack: 'MitreCloudTrailMapping'):
        self.attacks.append(attack)
    
    def get_all_attacks(self) -> List['MitreCloudTrailMapping']:
        return self.attacks

    def get_query_for_attack(self, attack_id: str) -> Dict[str, Any]:
        if self.mitre_attack_id == attack_id:
            return self.query
        for attack in self.attacks:
            query = attack.get_query_for_attack(attack_id)
            if query:
                return query
        return None

    @classmethod
    def init(cls) -> 'MitreCloudTrailMapping':
        # Main instance
        instance = cls(
            query={
                "bool": {
                    "must": [
                        {"match": {"eventSource": "s3.amazonaws.com"}},
                        {"match": {"eventName": "GetBucketAcl"}}
                    ]
                }
            },
            mitre_attack_id="T1134"
        )
        
        # Additional attack mappings
        additional_attacks = [
            cls(
                query={
                    "bool": {
                        "must": [
                            {"match": {"eventSource": "ec2.amazonaws.com"}},
                            {"match": {"eventName": "StartInstances"}}
                        ]
                    }
                },
                mitre_attack_id="T1135"
            ),
            cls(
                query = {
                    "bool": {
                    "must": [
                        { "match": { "eventSource": "cloudtrail.amazonaws.com" } },
                        { "match": { "eventName": "StopLogging" } }
                    ]
                    }
                 },

                mitre_attack_id="TA0005"  
            ),
            cls(
                query = {
                "bool": {
                "must": [
                    { "match": { "eventSource": "cloudtrail.amazonaws.com" } },
                    { "match": { "eventName": "DeleteTrail" } }
                ]
                }
            },

                mitre_attack_id="T1562"  
            ),
             cls(
                query = {
                "bool": {
                "must": [
                    { "match": { "eventSource": "s3.amazonaws.com" } },
                    {
                    "bool": {
                        "should": [
                        { "match": { "eventName": "DeleteBucketPolicy" } },
                        { "match": { "eventName": "DeleteBucketReplication" } },
                        { "match": { "eventName": "DeleteBucketCors" } },
                        { "match": { "eventName": "DeleteBucketEncryption" } },
                        { "match": { "eventName": "DeleteBucketLifecycle" } }
                        ],
                        "minimum_should_match": 1
                    }
                    }
                ]
                }
            },
                mitre_attack_id="T1070"  
            ),
             cls(
                query = {
                "bool": {
                "must": [
                    { "match": { "eventSource": "s3.amazonaws.com" } },
                    { "match": { "eventName": "PutBucketLifecycle" } }
                ]
                }
            },

                mitre_attack_id="T1070"  
            ),
             cls(
                 query = {
                "bool": {
                "must": [
                    { "match": { "eventSource": "s3.amazonaws.com" } },
                    { "match": { "eventName": "AccessDenied" } }
                ]
                }
            },
                mitre_attack_id="TA0040"  
            ),
        ]
        instance.add_attack(additional_attacks)
        return instance
