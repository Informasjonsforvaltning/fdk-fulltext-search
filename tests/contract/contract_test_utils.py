from requests import get, post, delete
import time


def wait_for_es():
    # wait for elasticsearch to be ready
    es_health = get("http://localhost:9200/_cluster/health?wait_for_status=yellow&timeout=50s")
    if es_health.status_code != 200:
        raise Exception('Testcontainers: could not contact ElasticsSearch')
    return


def populate():
    print("populating db")
    post("http://localhost:8080/harvest")
    timeout = time.time() + 90
    while True:
        response = get("http://localhost:8080/count")
        if response.status_code != 200:
            raise Exception('Testcontainers: request to service returned ' + response.status_code)
        if response.json()['count'] > 100:
            break
        if (time.time() > timeout):
            raise Exception('Testcontainers: timed out while waiting for count response ' + response.status_code)


def clean_es():
    print("cleaning db")
    delete("http://localhost:8080/informationmodels")
    delete("http://localhost:8080/concepts")
    delete("http://localhost:8080/dataservices")
    delete("http://localhost:8080/datasets")
