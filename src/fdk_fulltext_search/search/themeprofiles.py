from fdk_fulltext_search.search.query_filter_utils import get_field_by_filter_key


class ThemeProfileKeys:
    TRANSPORT = "transport"

    def __init__(self, key_string: str):
        if key_string == self.TRANSPORT:
            self.value = self.TRANSPORT


def theme_profile_filter(key: str) -> dict:
    terms_list = []
    los_filter_key = get_field_by_filter_key("los")
    for path in theme_profile_los_paths[ThemeProfileKeys(key).value]:
        terms_list.append({"term": {los_filter_key: path}})
    return {"bool": {"should": terms_list}}


theme_profile_los_paths = {
    ThemeProfileKeys.TRANSPORT: [
        "trafikk-og-transport/mobilitetstilbud",
        "trafikk-og-transport/trafikkinformasjon",
        "trafikk-og-transport/veg-og-vegregulering",
        "trafikk-og-transport/yrkestransport",
    ]
}
