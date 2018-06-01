import codecs
import json

from django.conf import settings

with codecs.open("config.json", "r", encoding="utf-8") as settings_file:
    settings_data = json.load(settings_file)

CORE_WEBSITE_NAME = getattr(settings, "WEBSITE_NAME", settings_data["WEBSITE_NAME"])
CORE_WEBSITE_SLOGAN = getattr(settings, "WEBSITE_TITLE", settings_data["WEBSITE_SLOGAN"])
