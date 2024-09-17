import pytest
import snowflake.snowpark as snow

from tabpipe.utils.snowflake import SnowflakeConnection


@pytest.fixture(scope='module')
def snowflake_connection() -> snow.Session:
    """Create a Snowflake connection."""
    return SnowflakeConnection().session
