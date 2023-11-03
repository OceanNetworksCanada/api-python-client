import os

from dotenv import load_dotenv
from robot.libraries.BuiltIn import BuiltIn

load_dotenv(override=True)
token = os.getenv('TOKEN', BuiltIn().get_variable_value("${TOKEN}"))