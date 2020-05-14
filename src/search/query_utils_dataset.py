def autorativ_dataset_query() -> dict:
    return {
        "match": {
            "provenance.code": "NASJONAL"
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
