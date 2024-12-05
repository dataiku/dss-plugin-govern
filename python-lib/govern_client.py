import dataikuapi
import dataiku

def get_settings(config, plugin_config):
    plugin_config_instance_configuration_preset = plugin_config.get("instance_configuration_preset", None)
    config_instance_configuration_preset = config.get("instance_configuration_preset", None)
    if plugin_config_instance_configuration_preset is None or config_instance_configuration_preset is None:
        return None
    use_govern_integration_settings = plugin_config_instance_configuration_preset.get("use_govern_integration_settings", False)
    govern_host = str(config_instance_configuration_preset.get("govern_host", ""))
    govern_key = str(config_instance_configuration_preset.get("govern_key", ""))
    govern_insecure_tls = config_instance_configuration_preset.get("govern_insecure_tls", False)
    impersonate_govern_user = str(config_instance_configuration_preset.get("impersonate_govern_user", ""))
    return {
        'use_govern_integration_settings': use_govern_integration_settings,
        'govern_host': govern_host,
        'govern_key': govern_key,
        'govern_insecure_tls': govern_insecure_tls,
        'impersonate_govern_user': impersonate_govern_user
    }

def get_govern_client(settings):
    if settings is None:
        raise Exception("Invalid Dataiku Govern instance plugin settings")
    use_govern_integration_settings = settings["use_govern_integration_settings"]
    govern_host = settings["govern_host"]
    govern_key = settings["govern_key"]
    govern_insecure_tls = settings["govern_insecure_tls"]
    impersonate_govern_user = settings["impersonate_govern_user"]
    if use_govern_integration_settings is True:
        govern_client = dataiku.api_client().get_govern_client()
        if govern_client is None:
            raise Exception("Dataiku Govern instance is not enabled or misconfigured")
    else:
        if len(govern_host) <= 0 or len(govern_key) <= 0:
            raise Exception("Dataiku Govern host and API Key must be provided")
        govern_client = dataikuapi.GovernClient(govern_host, govern_key, insecure_tls=govern_insecure_tls)
    if len(impersonate_govern_user) > 0:
        return govern_client.get_user(impersonate_govern_user).get_client_as()
    else:
        return govern_client
