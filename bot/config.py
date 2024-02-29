import importlib
import yaml

CONFIG_FILE = "./bot/resources/config.yaml"
config = {}

try:
    with open(CONFIG_FILE, "r") as myYaml:
        config.update(yaml.load(myYaml, Loader=yaml.SafeLoader))
except Exception as e:
    print(f"Unable to import file {CONFIG_FILE}. Exception caught: {e}")

# Imports command modules if enabled in config.json
for setting, enabled in config.items():
    if enabled:
        importlib.import_module(f"bot.commands.{setting}")
        print(f"Imported command module {setting}.")