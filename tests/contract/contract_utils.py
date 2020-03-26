import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time


def wait_for_es():
    # wait 1 minute for elasticsearch to be ready
    retry_strategy = Retry(connect=5, read=5, backoff_factor=2)
    adapter = HTTPAdapter(max_retries=retry_strategy)
    http = requests.Session()
    http.mount("http://", adapter)
    es_health = http.get("http://localhost:9200/_cluster/health?wait_for_status=yellow&timeout=50s")
    if es_health.status_code != 200:
        raise Exception('Test containers: could not contact ElasticsSearch')
    return


def populate():
    print("populating db")
    update_response = requests.put("http://localhost:8080/update")
    if update_response.status_code != 200:
        raise Exception(
            'Test containers: received http status' + str(update_response.status_code) + "when attempting to start "
                                                                                         "content update")

    timeout = time.time() + 90
    while True:
        response = requests.get("http://localhost:8080/count")
        if response.status_code != 200:
            raise Exception('Test containers: request to service returned ' + response.status_code)
        if response.json()['count'] == 130:
            break
        if (time.time() > timeout):
            raise Exception('Test containers: timed out while waiting for count response ' + response.status_code)


def clean_es():
    print("cleaning db")
    requests.delete("http://localhost:8080/informationmodels")
    requests.delete("http://localhost:8080/concepts")
    requests.delete("http://localhost:8080/dataservices")
    requests.delete("http://localhost:8080/datasets")
