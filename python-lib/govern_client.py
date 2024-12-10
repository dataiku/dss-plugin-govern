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
    govern_no_check_certificate = config_instance_configuration_preset.get("govern_no_check_certificate", False)
    impersonate_govern_user = str(config_instance_configuration_preset.get("impersonate_govern_user", ""))
    return {
        'use_govern_integration_settings': use_govern_integration_settings,
        'govern_host': govern_host,
        'govern_key': govern_key,
        'govern_no_check_certificate': govern_no_check_certificate,
        'impersonate_govern_user': impersonate_govern_user
    }

def get_govern_client(settings):
    if settings is None:
        raise Exception("Invalid Dataiku Govern instance plugin settings")
    use_govern_integration_settings = settings["use_govern_integration_settings"]
    govern_host = settings["govern_host"]
    govern_key = settings["govern_key"]
    govern_no_check_certificate = settings["govern_no_check_certificate"]
    impersonate_govern_user = settings["impersonate_govern_user"]
    if use_govern_integration_settings is True:
        dss_client = dataiku.api_client()
        if not "get_govern_client" in dir(dss_client):
            raise Exception("Cannot enable the use_govern_integration_settings option because DSS version is lower than v13.3.2")
        govern_client = dss_client.get_govern_client()
        if govern_client is None:
            raise Exception("Dataiku Govern integration is not enabled or misconfigured in Dataiku DSS general settings")
    else:
        if len(govern_host) <= 0 or len(govern_key) <= 0:
            raise Exception("Dataiku Govern host and API Key must be provided")
        govern_client = dataikuapi.GovernClient(govern_host, govern_key)
        if govern_no_check_certificate: # use the old way to make sure it's compatible with most versions of DSS
            govern_client._session.verify = False
    if len(impersonate_govern_user) > 0:
        return govern_client.get_user(impersonate_govern_user).get_client_as()
    else:
        return govern_client
