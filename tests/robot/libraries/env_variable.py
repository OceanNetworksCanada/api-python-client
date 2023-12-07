import os

from dotenv import load_dotenv

from robot.libraries.BuiltIn import BuiltIn, RobotNotRunningError

load_dotenv(override=True)
try:
    robot_val = BuiltIn().get_variable_value("${TOKEN}")
except RobotNotRunningError:
    robot_val = None
token = os.getenv("TOKEN", robot_val)
is_prod = os.getenv("ONC_ENV", "PROD") == "PROD"
