import json


class ConfigManager:

    configFile = './resources/config.json'

    config = False

    def __init__(self):

        if self.config is False:

            with open(self.configFile, "r") as jsonfile:
                self.config = json.load(jsonfile)

    def get_config(self):

        return self.config
