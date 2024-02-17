import importlib
import yaml

config_file = "./bot/resources/config.yaml"
config = {}

with open(config_file, "r") as myYaml:
    config.update(yaml.load(myYaml, Loader=yaml.SafeLoader))

# Imports command modules if enabled in config.json
for setting, enabled in config.items():
    if enabled:
        importlib.import_module(f"bot.commands.{setting}")