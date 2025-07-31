import json
import os

class Notifier:
    def __init__(self):
        config_path = './notifier_configuration.json'
        if not os.path.exists(config_path):
            with open(config_path, 'w') as file:
                json.dump({"connectors": []}, file, indent=4)
       
        with open(config_path, 'r') as file:
            self.config = json.load(file)
        self.connectors = []

        for connector in self.config.get('connectors', []):
            if connector['type'] == 'telegram' and connector['status'] == 'enabled':
                from NotifierConnectors.TelegramConnector import TelegramConnector
                self.connectors.append(TelegramConnector(connector['params']['bot_token'], connector['params']['chat_id']))
            # TODO: Add discord connector

    def send_notification(self, message):
        for connector in self.connectors:
            print(f"[Notifier] Sending message via {connector.__class__.__name__}")
            success = connector.send_message(message)
            if not success:
                print(f"[Notifier] Failed to send message via {connector.__class__.__name__}")
            
    
    def add_connector(self,connector_name, connector_type, status, params):
        # Check if connector already exists
        for connector in self.config['connectors']:
            if connector['name'] == connector_name:
                print(f"[Notifier] Connector {connector_name} already exists.")
                return False
            
        new_connector = {
            "name": connector_name,
            "type": connector_type,
            "status": status,
            "params": params
        }
        self.config['connectors'].append(new_connector)
        with open('./notifier_configuration.json', 'w') as file:
            json.dump(self.config, file, indent=4)
        print(f"[Notifier] Added new connector: {connector_name}")
        return True

    def get_connectors(self):
        connectors = []
        for connector in self.config.get('connectors', []):
            obfuscated_connector = connector.copy()
            obfuscated_params = {}
            for key, value in connector.get('params', {}).items():
                print(key)
                if isinstance(value, str) and len(value) > 6:
                    obfuscated = value[:3] + '*' * (len(value) - 6) + value[-3:]
                else:
                    obfuscated = '*' * len(str(value))
                obfuscated_params[key] = obfuscated
                obfuscated_connector['params'] = obfuscated_params
            connectors.append(obfuscated_connector)
        return connectors

    def remove_connector(self, connector_name):
        self.config['connectors'] = [c for c in self.config['connectors'] if c['name'] != connector_name]
        with open('./notifier_configuration.json', 'w') as file:
            json.dump(self.config, file, indent=4)
        print(f"[Notifier] Removed connector: {connector_name}")
