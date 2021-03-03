from fdk_fulltext_search.ingest.utils import IndicesKey

index_title_fields = {
    IndicesKey.INFO_MODEL: ["title.nb", "title.nn", "title.no", "title.en"],
    IndicesKey.DATA_SETS: ["title.nb", "title.nn", "title.no", "title.en"],
    IndicesKey.DATA_SERVICES: ["title.nb", "title.nn", "title.en"],
    IndicesKey.CONCEPTS: [
        "prefLabel.nb",
        "prefLabel.nn",
        "prefLabel.no",
        "prefLabel.en",
    ],
    IndicesKey.PUBLIC_SERVICES: ["title.nb", "title.nn", "title.no", "title.en"],
    IndicesKey.EVENTS: ["title.nb", "title.nn", "title.no", "title.en"],
}

index_suggestion_fields = {
    IndicesKey.DATA_SETS: ["title", "uri"],
    IndicesKey.CONCEPTS: [
        "id",
        "identifier",
        "uri",
        "definition",
        "prefLabel",
        "publisher",
    ],
    IndicesKey.DATA_SERVICES: ["id", "uri", "title", "publisher"],
    IndicesKey.INFO_MODEL: ["id", "uri", "title", "publisher"],
}

index_description_fields = {
    IndicesKey.INFO_MODEL: ["schema^0.5"],
    IndicesKey.DATA_SETS: [
        "description.nb",
        "description.nn",
        "description.no",
        "description.en",
    ],
    IndicesKey.DATA_SERVICES: ["description.nb", "description.nn", "description.en"],
    IndicesKey.CONCEPTS: [
        "definition.text.nb",
        "definition.text.nn",
        "definition.text.no",
        "definition.text.en",
    ],
    IndicesKey.PUBLIC_SERVICES: [
        "description.nb",
        "description.nn",
        "description.no",
        "description.en",
    ],
    IndicesKey.EVENTS: [
        "description.nb",
        "description.nn",
        "description.no",
        "description.en",
    ],
    IndicesKey.ALL: ["description", "definition.text.*", "schema^0.5"],
}

index_fulltext_fields = {
    IndicesKey.CONCEPTS: [
        "publisher.name^3",
        "publisher.prefLabel^3",
        "definition.text.*",
        "definition.source.prefLabel.*^3",
        "definition.sourceRelationship",
        "definition.sources.text.*",
        "prefLabel.*^3",
        "subject.*",
    ],
    IndicesKey.DATA_SETS: [
        "title.*^3",
        "objective.*",
        "keyword.*^2",
        "theme.title.*",
        "expandedLosTema.*",
        "description.*",
        "publisher.name^3",
        "publisher.prefLabel^3",
        "accessRights.prefLabel.*^3",
        "accessRights.code",
        "subject.prefLabel.*",
        "subject.altLabel.*",
        "subject.definition.*",
        "distribution.title.*",
        "distribution.format",
    ],
    IndicesKey.DATA_SERVICES: [
        "title.*^3",
        "description.*",
        "publisher.name^3",
        "publisher.prefLabel^3",
        "mediaType.code",
    ],
    IndicesKey.INFO_MODEL: [
        "title.*^3",
        "keyword.*^2",
        "theme.title.*",
        "losTheme.name.^3",
        "description.*",
        "publisher.name^3",
        "publisher.prefLabel^3",
    ],
}
