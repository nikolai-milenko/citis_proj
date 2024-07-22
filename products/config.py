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

    def get_marketplaces(self):
        return self.config.get('marketplaces')

    def get_max_websites_count(self):
        return self.config.get('max_websites_count', 7)

    def get_max_results_from_website(self):
        return self.config.get('max_results_from_website', 5)

    def get_headers(self):
        return self.config.get('headers', {})

    def get_website_selectors(self):
        return self.config.get('websites_css_selectors', {})

    def get_server_host(self):
        return self.config.get('server', {})

    def get_database_host(self):
        return self.get('database', 'host', 'localhost')

    def get_database_port(self):
        return self.get('database', 'port', 3306)

    def get_database_username(self):
        return self.get('database', 'username', 'user')

    def get_database_password(self):
        return self.get('database', 'password', 'pass')

    def get_driver_path(self):
        return self.config.get('driverpath', '')

    def get_db_host(self):
        return self.config.get('dbhost', '')

    def get_analytics_host(self):
        return self.config.get('analyticsHost', '')

    def get_update_interval(self):
        return self.config.get('update_interval', 120)
