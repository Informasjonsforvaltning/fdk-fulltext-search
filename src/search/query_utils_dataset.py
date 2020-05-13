def autorativ_dataset_query() -> dict:
    return {
        "match": {
            "provenance.code": "NASJONAL"
        }
    }


def data_sets_default_query() -> dict:
    return {
        "bool": {
            "must": [
                {
                    "match_all": {}
                }
            ],
            "should": [
                autorativ_dataset_query(),
                open_data_query()
            ]
        }
    }


def open_data_query():
    return {
        "bool": {
            "must": [
                {
                    "term": {
                        "accessRights.code.keyword": "PUBLIC"
                    }
                },
                {
                    "term": {
                        "distribution.openLicense": "true"
                    }
                }
            ]
        }
    }
