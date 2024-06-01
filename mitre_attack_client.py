from mitreattack.stix20 import MitreAttackData


class MitreAttackClient:
    def __init__(self, filename="enterprise-attack.json"):
        self.mitre_attack_data = MitreAttackData(filename)

    def get_object_by_attack_id(self, attack_id, object_type='attack-pattern'):
        return self.mitre_attack_data.get_object_by_attack_id(attack_id, object_type)
 