import json

from dataiku.connector import Connector
import dataikuapi
from dataikuapi.govern.artifact_search import GovernArtifactSearchQuery, GovernArtifactFilterBlueprints

from govern_client import get_govern_client, get_settings

class GovernItemsConnector(Connector):

    def __init__(self, config, plugin_config):
        Connector.__init__(self, config, plugin_config)
        self.govern_client = get_govern_client(get_settings(config))
        self.blueprint_ids = config.get("blueprint_ids", [])
        self.retrieve_bp_bpv = config.get("retrieve_bp_bpv", False)

    def get_read_schema(self):
        columns = [
            {'name': 'artifact_json', 'type': 'string'},
            {'name': 'signoffs_json', 'type': 'string'}
        ]
        if self.retrieve_bp_bpv:
            columns.append({'name': 'blueprint_json', 'type': 'string'})
            columns.append({'name': 'blueprint_version_json', 'type': 'string'})
        return {'columns': columns}

    def generate_rows(self, dataset_schema=None, dataset_partitioning=None,
                            partition_id=None, records_limit = -1):
        request = self.govern_client.new_artifact_search_request(GovernArtifactSearchQuery(artifact_filters=[GovernArtifactFilterBlueprints(blueprint_ids=self.blueprint_ids)]))
        page_size = records_limit if records_limit >= 0 else 1000
        items_count = 0
        while True:
            response = request.fetch_next_batch(page_size=page_size)
            response_hits = response.get_response_hits()
            items_count += len(response_hits)
            for response_hit in response_hits:
                returned_data = {
                    'artifact_json': json.dumps(response_hit.get_raw()['artifact']),
                    'signoffs_json': json.dumps(response_hit.get_raw().get('signoffs', '[]'))
                }
                if self.retrieve_bp_bpv:
                    returned_data['blueprint_json'] = json.dumps(response_hit.get_raw()['blueprint'])
                    returned_data['blueprint_version_json'] = json.dumps(response_hit.get_raw()['blueprintVersion'])
                yield returned_data
            if (records_limit >= 0 and items_count >= records_limit) or not response.get_raw()['hasNextPage']:
                break

    def get_records_count(self, partitioning=None, partition_id=None):
        raise NotImplementedError

    def get_writer(self, dataset_schema=None, dataset_partitioning=None,
                         partition_id=None, write_mode="OVERWRITE"):
        raise NotImplementedError

    def get_partitioning(self):
        raise NotImplementedError

    def list_partitions(self, partitioning):
        return []

    def partition_exists(self, partitioning, partition_id):
        raise NotImplementedError


class CustomDatasetWriter(object):
    def __init__(self):
        pass

    def write_row(self, row):
        raise NotImplementedError

    def close(self):
        pass
