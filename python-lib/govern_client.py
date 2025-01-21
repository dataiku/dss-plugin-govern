import dataikuapi
import dataiku

def get_settings(config):
    config_instance_configuration_preset = config.get("instance_configuration_preset", None)
    if config_instance_configuration_preset is None:
        return None
    govern_host = str(config_instance_configuration_preset.get("govern_host", ""))
    govern_key = str(config_instance_configuration_preset.get("govern_key", ""))
    govern_no_check_certificate = config_instance_configuration_preset.get("govern_no_check_certificate", False)
    impersonate_govern_user = str(config_instance_configuration_preset.get("impersonate_govern_user", ""))
    return {
        'govern_host': govern_host,
        'govern_key': govern_key,
        'govern_no_check_certificate': govern_no_check_certificate,
        'impersonate_govern_user': impersonate_govern_user
    }

def get_govern_client(settings):
    if settings is None:
        raise Exception("Invalid Dataiku Govern instance plugin settings")
    govern_host = settings["govern_host"]
    govern_key = settings["govern_key"]
    govern_no_check_certificate = settings["govern_no_check_certificate"]
    impersonate_govern_user = settings["impersonate_govern_user"]
    if len(govern_host) <= 0 or len(govern_key) <= 0:
        raise Exception("Dataiku Govern host and API Key must be provided")
    govern_client = dataikuapi.GovernClient(govern_host, govern_key)
    if govern_no_check_certificate: # use the old way to make sure it's compatible with most versions of DSS
        govern_client._session.verify = False
    if len(impersonate_govern_user) > 0:
        return govern_client.get_user(impersonate_govern_user).get_client_as()
    else:
        return govern_client
