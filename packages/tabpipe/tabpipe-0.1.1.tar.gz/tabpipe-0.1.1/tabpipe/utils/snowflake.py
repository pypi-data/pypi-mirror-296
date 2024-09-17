import os
from enum import Enum

import snowflake.snowpark as snow


class SnowflakeSessionParams(Enum):
    """Snowflake session parameters."""

    host = ("SNOWFLAKE_HOST", False)
    account = ("SNOWFLAKE_ACCOUNT", False)
    user = ("SNOWFLAKE_USER", False)
    warehouse = ("SNOWFLAKE_WAREHOUSE", True)
    database = ("SNOWFLAKE_DATABASE", True)
    schema = ("SNOWFLAKE_SCHEMA", True)
    password = ("SNOWFLAKE_PASSWORD", True)
    role = ("SNOWFLAKE_ROLE", True)
    authenticator = ("SNOWFLAKE_AUTHENTICATOR", True)


class SnowflakeConnection:
    """A class to store the Snowflake connection.

    Taken from: https://github.com/Snowflake-Labs/snowpark-devops/
    """

    def __init__(self):
        """Initialize the Snowflake connection."""
        try:
            self._session = snow.context.get_active_session()
        except snow.exceptions.SnowparkSessionException:
            sf_config = {}
            for param in SnowflakeSessionParams:
                param_env, param_optional = param.value
                if not param_optional:
                    sf_config[param.name] = os.environ[param_env]
                else:
                    if param_env in os.environ:
                        sf_config[param.name] = os.environ[param_env]

            if not (
                SnowflakeSessionParams.password.name in sf_config
                or SnowflakeSessionParams.authenticator.name in sf_config
            ):
                raise ValueError(
                    "Either the password or authenticator must be defined."
                )

            self._session = snow.Session.builder.configs(sf_config).create()

    @property
    def session(self) -> snow.Session:
        """Get the Snowflake session."""
        return self._session
