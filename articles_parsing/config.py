import yaml

class Config:
    def __init__(self, config_path):
        self.config_path = config_path
        self.config = self.load_config()

    def load_config(self):
        with open(self.config_path, 'r') as file:
            return yaml.safe_load(file)

    def get(self, section, option, default=None):
        return self.config.get(section, {}).get(option, default)

    def get_server_port(self):
        return self.get('server', 'port', 5000)

    def get_server_host(self):
        return self.get('server', 'host', 'localhost')

    def get_database_host(self):
        return self.get('database', 'host', 'localhost')

    def get_database_port(self):
        return self.get('database', 'port', 3306)

    def get_database_username(self):
        return self.get('database', 'username', 'user')

    def get_database_password(self):
        return self.get('database', 'password', 'pass')