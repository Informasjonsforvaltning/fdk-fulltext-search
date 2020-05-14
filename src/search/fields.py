from src.ingest import IndicesKey

index_title_fields = {
    IndicesKey.INFO_MODEL: ['title.nb', 'title.nn', 'title.no', 'title.en'],
    IndicesKey.DATA_SETS: ['title.nb', 'title.nn', 'title.no', 'title.en']
}

index_description_fields = {
    IndicesKey.INFO_MODEL: ["schema^0.5"],
    IndicesKey.DATA_SETS: ["description.nb", "description.nn", "description.no", "description.en"],
    IndicesKey.ALL: ["description", "definition.text.*", "schema^0.5"]
}

index_fulltext_fields = {
    IndicesKey.DATA_SETS: ["title.*^3", "objective.*", "keyword.*^2", "theme.title.*",
                           "expandedLosTema.*", "description.*", "publisher.name^3",
                           "publisher.prefLabel^3", "accessRights.prefLabel.*^3",
                           "accessRights.code", "subject.prefLabel.*", "subject.altLabel.*",
                           "subject.definition.*"]
}
