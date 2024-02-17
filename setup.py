#!/usr/bin/python

import shutil

ENV_SRC_PATH = "./templates/.env.template"
ENV_DEST_PATH = "./.env"

CONFIG_SRC_PATH = "./templates/config.yaml.template"
CONFIG_DEST_PATH = "./bot/resources/config.yaml"

try:
    shutil.copyfile(ENV_SRC_PATH, ENV_DEST_PATH)
    print(f"Copied {ENV_SRC_PATH} to {ENV_DEST_PATH}.")
except Exception as e:
    print(f"Unable to copy {ENV_SRC_PATH} to {ENV_DEST_PATH}: {e}")

try:
    shutil.copyfile(CONFIG_SRC_PATH, CONFIG_DEST_PATH)
    print(f"Copied {CONFIG_SRC_PATH} to {ENV_DEST_PATH}.")
except Exception as e:
    print(f"Unable to copy {CONFIG_SRC_PATH} to {CONFIG_DEST_PATH}: {e}")