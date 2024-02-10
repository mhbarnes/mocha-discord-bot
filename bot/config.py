import json
import importlib

config_file = "./bot/resources/config.json"
config = {}

with open(config_file, 'r') as myJson:
    config.update(json.load(myJson))

# Imports command modules if enabled in config.json
for setting, enabled in config.items():
    if enabled:
        importlib.import_module(f"bot.commands.{setting}")