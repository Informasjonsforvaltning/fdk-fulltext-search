from src.ingest import IndicesKey

index_title_fields = {
    IndicesKey.INFO_MODEL: ['title.nb', 'title.nn', 'title.no', 'title.en'
                            ]
}

index_description_fields = {
    IndicesKey.INFO_MODEL: ["schema^0.5"],
    IndicesKey.ALL: ["description", "definition.text.*", "schema^0.5"]
}
