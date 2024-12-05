from govern_client import get_govern_client, get_settings
import json

def do(payload, config, plugin_config, inputs):
    settings = get_settings(config, plugin_config)
    if settings is None:
        return {"choices": []}
    else:
        client = get_govern_client(settings)
        blueprints = client.list_blueprints()
        choices = [{
            'value': bp.get_raw()['blueprint']['id'],
            'label': bp.get_raw()['blueprint']['name'] + ' (' + bp.get_raw()['blueprint']['id'] + ')'
        } for bp in blueprints]
        return {"choices": choices}
