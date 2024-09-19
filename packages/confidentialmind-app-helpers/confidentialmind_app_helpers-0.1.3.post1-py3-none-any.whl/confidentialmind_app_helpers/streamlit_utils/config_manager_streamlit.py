import streamlit as st
from confidentialmind_core.config_manager import ConfigManager, ConnectorSchema


# Note: ConfigManager must be initialized before it can be used
@st.cache_resource
def get_config_manager():
    """
    Retrieve a cached instance of the ConfigManager.

    This function leverages Streamlit's caching mechanism to ensure that only one instance of ConfigManager is created
    per session, optimizing resource usage and performance.

    Returns:
        ConfigManager: An initialized and cached ConfigManager instance.
    """
    return ConfigManager()


# This non-caching function exists to make sure the id is used in the cache key
# and to make the parameter names nicer (no underscores)
# Note: the id parameter no longer exists in the ConfigManager constructor. This function is now redundant except for
#  the nicer parameter names.
def init_config_manager(
    config_model,
    connectors: list[ConnectorSchema] = None,
):
    """
    Initialize a ConfigManager instance with the given parameters.

    This function is designed to ensure that certain parameters, such as 'id', are included in the cache key for
    Streamlit's caching mechanism. It also provides a more user-friendly interface than the private `_init_config_manager`
    function.

    Args:
        config_model (type): The model class used by ConfigManager.
        connectors (list[ConnectorSchema], optional): List of ConnectorSchema instances to initialize with.

    Returns:
        ConfigManager: An initialized and potentially cached ConfigManager instance.
    """
    config_manager = _init_config_manager(
        _config_model=config_model,
        _connectors=connectors,
    )
    return config_manager


# Underscored parameters are not used in cache key
# TODO: implement hash function for custom objects if needed
@st.cache_resource
def _init_config_manager(
    _config_model,
    _connectors: list[ConnectorSchema] = None,
):
    """
    Initialize a ConfigManager instance, intended for internal use.

    This function is similar to `init_config_manager`, but with parameters prefixed by an underscore. These parameters
    are not included in the cache key since they may be complex objects like classes or lists of custom objects, which
    could complicate caching logic.

    Args:
        _config_model (type): The app config model class used by ConfigManager.
        _connectors (list[ConnectorSchema], optional): List of connectors the app may use.

    Returns:
        ConfigManager: An initialized ConfigManager instance.
    """
    config_manager = ConfigManager()

    config_manager.init_manager(
        config_model=_config_model,
        connectors=_connectors,
    )
    return config_manager
