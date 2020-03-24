import requests
import time


def wait_for_es():
    # wait 1 minute for elasticsearch to be ready
    es_health = requests.get("http://localhost:9200/_cluster/health?wait_for_status=yellow&timeout=50s")
    if es_health.status_code != 200:
        raise Exception('Testcontainers: could not contact ElasticsSearch')
    return


def populate():
    print("populating db")
    harvest_response = requests.post("http://localhost:8080/harvest")
    if harvest_response.status_code != 200:
        raise Exception(
            'Testcontainers: received http status' + harvest_response.status_code + "when attempting to start content harvest")

    timeout = time.time() + 90
    while True:
        response = requests.get("http://localhost:8080/count")
        if response.status_code != 200:
            raise Exception('Testcontainers: request to service returned ' + response.status_code)
        if response.json()['count'] > 100:
            break
        if (time.time() > timeout):
            raise Exception('Testcontainers: timed out while waiting for count response ' + response.status_code)


def clean_es():
    print("cleaning db")
    requests.delete("http://localhost:8080/informationmodels")
    requests.delete("http://localhost:8080/concepts")
    requests.delete("http://localhost:8080/dataservices")
    requests.delete("http://localhost:8080/datasets")


