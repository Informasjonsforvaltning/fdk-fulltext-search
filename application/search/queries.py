match_all = {
    "query": {
        "match_all": {}
    }
}

all_indices = {

}


def add_size(query: dict, size) -> dict:
    if size is not None:
        query['size'] = size
    return query
