test_hits = {"hits":
    {
        "took": 22,
        "timed_out": "false",
        "_shards": {
            "total": 4,
            "successful": 4,
            "skipped": 0,
            "failed": 0
        },
        "hits": {
            "total": {
                "value": 130,
                "relation": "eq"
            },
            "max_score": 1.2,
            "hits": [
                {
                    "_index": "dataservices",
                    "_type": "document",
                    "_id": "baaeeaf2-a2d0-44d0-a5a9-d040a66993e2",
                    "_score": 1.2,
                    "_source": {
                        "nationalComponent": "true",
                        "isOpenAccess": "true",
                        "isOpenLicense": "true",
                        "isFree": "true",
                        "statusCode": "EXPERIMENTAL",
                        "id": "baaeeaf2-a2d0-44d0-a5a9-d040a66993e2",
                        "title": "Sindres nasjonale opplæringskontorregister API",
                        "publisher": {
                            "id": "910244132",
                            "name": "RAMSUND OG ROGNAN REVISJON",
                            "orgPath": "/ANNET/910244132"
                        }
                    }
                },
                {
                    "_index": "dataservices",
                    "_type": "document",
                    "_id": "7c927741-59b5-4511-855f-54ab52f8baa0",
                    "_score": 1.2,
                    "_source": {
                        "nationalComponent": "true",
                        "isOpenAccess": "true",
                        "isOpenLicense": "true",
                        "isFree": "true",
                        "statusCode": "DEPRECATED",
                        "deprecationInfoExpirationDate": "2019-11-27T23:00:00.000Z",
                        "deprecationInfoReplacedWithUrl": "",
                        "id": "7c927741-59b5-4511-855f-54ab52f8baa0",
                        "title": "Barnehagefakta",
                        "publisher": {
                            "id": "910258028",
                            "name": "LILAND OG ERDAL REVISJON",
                            "orgPath": "/ANNET/910258028"
                        }
                    }
                },
                {
                    "_index": "dataservices",
                    "_type": "document",
                    "_id": "0670b703-e230-42ec-967e-27fe11ed3a69",
                    "_score": 1.2,
                    "_source": {
                        "nationalComponent": "true",
                        "isOpenAccess": "true",
                        "isOpenLicense": "true",
                        "isFree": "true",
                        "statusCode": "EXPERIMENTAL",
                        "id": "0670b703-e230-42ec-967e-27fe11ed3a69",
                        "title": "Åpne Data fra Enhetsregisteret - API Dokumentasjon",
                        "description": "Teknisk beskrivelse av REST-tjenestene i Åpne Data fra Enhetsregisteret - Work in progress\n---\n\n## Ordbok\n### Enhetsregisteret\nRegister over grunndata om juridiske personer og andre enheter. Enhetsregisteret tildeler organisasjonsnummer for entydig identifisering av enheter.\n\n### Organisasjonsnummer\nNisifret nummer som entydig identifiserer enheter i Enhetsregisteret.\n\n### Enhet\nEnhet på øverste nivå i registreringsstrukturen i Enhetsregisteret. Eksempelvis enkeltpersonforetak, foreninger, selskap, sameier og andre som er registrert i Enhetsregisteret. Identifiseres med organisasjonsnummer.\n\n### Underenhet\nEnhet på laveste nivå i registreringsstrukturen i Enhetsregisteret. En underenhet kan ikke eksistere alene og har alltid knytning til en hovedenhet. Identifiseres med organisasjonsnummer.\n\n### Organisasjonsform\nOrganisasjonsform er virksomhetens formelle organisering og gir retningslinjer overfor blant annet ansvarsforhold, skatt, revisjonsplikt, rettigheter og plikter.\n\n### Næringskode\n[Næringskoder]: https://www.brreg.no/bedrift/naeringskoder/\n[Næringskoder] på brreg.no\n\n[Standard for næringsgruppering]: https://www.ssb.no/klass/klassifikasjoner/6\n[Standard for næringsgruppering]\n---\n\n## Versjonering\nDu kan velge major versjon ved å spesifisere HTTP Accept-headeren. Bruk headeren spesifisert i tabellen under. Hvis versjon ikke spesifiseres, vil man få siste versjon.\n\n \n \n API\n Header\n \n \n \n \n /\n application/vnd.enhetsregisteret.v1+json\n \n \n /organisasjonsformer\n application/vnd.enhetsregisteret.organisasjonsform.v1+json\n \n \n\n\n\n### Strategi\nVi skal normalt ikke bryte bakoverkompabiliteten med våre brukere. Likevel kan det være nødvendig i enkelte situasjoner, av for eksempel juridiske årsaker eller vedlikehold, å gjøre endringer som medfører et slikt brudd. Vi vil i dette tilfellet versjonere tjenesten slik at nyeste versjon vil være tilgjengelig sammen med forrige versjon.\n\n#### Dersom man ikke benytter versjonering i accept header, vil man få siste versjon.\n\nEldre versjon vil anses som utdatert/deprecated, og vil på sikt bli tatt bort. Ved behov for denne typen endringer vil vi forsøke å gi bruker god tid, og varsle om endringen i forkant. Se punkt om varsling.\n\n### Når innføres ny versjon\nVi vil innføre en ny versjon når vi introduserer en endring som påvirker bakoverkompabiliteten. Mindre endringer og patcher vil ikke medføre versjonsendring i header.\n\n### Når fjernes en versjon\nVi vil legge ut varsel/driftsmeldinger i god tid på følgende steder:\n- [Driftsmeldinger]: https://www.brreg.no/om-oss/driftsmeldinger/\n[Driftsmeldinger]\n- [RSS-feed]: https://www.brreg.no/produkter-og-tjenester/rss-feed/\n[RSS-feed].\n\nEksempel på endring som medfører versjonering:\n\n- Fjerne eller endre navn på et attributt i HTTP-responsen.\n\n- Fjerne eller endre navn på et REST endepunkt.\n\n---\n\n## Endringslogg\n\n \n \n Versjon\n Dato\n Endring\n \n \n \n \n 1.1.0\n 14. august 2018\n Ny tjeneste /oppdateringer/enheter og /oppdateringer/underenheter\n \n \n 1.0.0\n 6. april 2018\n Produksjonssetting av ny åpne data tjeneste for Enhetsregisteret\n \n \n\n",
                        "descriptionFormatted": "Teknisk beskrivelse av REST-tjenestene i Åpne Data fra Enhetsregisteret - Work in progress\n---\n\n## Ordbok\n### Enhetsregisteret\nRegister over grunndata om juridiske personer og andre enheter. Enhetsregisteret tildeler organisasjonsnummer for entydig identifisering av enheter.\n\n### Organisasjonsnummer\nNisifret nummer som entydig identifiserer enheter i Enhetsregisteret.\n\n### Enhet\nEnhet på øverste nivå i registreringsstrukturen i Enhetsregisteret. Eksempelvis enkeltpersonforetak, foreninger, selskap, sameier og andre som er registrert i Enhetsregisteret. Identifiseres med organisasjonsnummer.\n\n### Underenhet\nEnhet på laveste nivå i registreringsstrukturen i Enhetsregisteret. En underenhet kan ikke eksistere alene og har alltid knytning til en hovedenhet. Identifiseres med organisasjonsnummer.\n\n### Organisasjonsform\nOrganisasjonsform er virksomhetens formelle organisering og gir retningslinjer overfor blant annet ansvarsforhold, skatt, revisjonsplikt, rettigheter og plikter.\n\n### Næringskode\n[Næringskoder]: https://www.brreg.no/bedrift/naeringskoder/\n[Næringskoder]  på brreg.no\n\n[Standard for næringsgruppering]: https://www.ssb.no/klass/klassifikasjoner/6\n[Standard for næringsgruppering]\n---\n\n## Versjonering\nDu kan velge major versjon ved å spesifisere HTTP Accept-headeren. Bruk headeren spesifisert i tabellen under. Hvis versjon ikke spesifiseres, vil man få siste versjon.\n<table>\n  <thead>\n    <tr>\n      <th>API</th>\n      <th>Header</th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <td>/</td>\n      <td>application/vnd.enhetsregisteret.v1+json</td>\n    </tr>\n    <tr>\n      <td>/organisasjonsformer</td>\n      <td>application/vnd.enhetsregisteret.organisasjonsform.v1+json</td>\n    </tr>\n  </tbody>\n</table>\n\n\n### Strategi\nVi skal normalt ikke bryte bakoverkompabiliteten med våre brukere. Likevel kan det være nødvendig i enkelte situasjoner, av for eksempel juridiske årsaker eller vedlikehold, å gjøre endringer som medfører et slikt brudd. Vi vil i dette tilfellet versjonere tjenesten slik at nyeste versjon vil være tilgjengelig sammen med forrige versjon.\n\n#### Dersom man ikke benytter versjonering i accept header, vil man få siste versjon.\n\nEldre versjon vil anses som utdatert/deprecated, og vil på sikt bli tatt bort. Ved behov for denne typen endringer vil vi forsøke å gi bruker god tid, og varsle om endringen i forkant. Se punkt om varsling.\n\n### Når innføres ny versjon\nVi vil innføre en ny versjon når vi introduserer en endring som påvirker bakoverkompabiliteten. Mindre endringer og patcher vil ikke medføre versjonsendring i header.\n\n### Når fjernes en versjon\nVi vil legge ut varsel/driftsmeldinger i god tid på følgende steder:\n- [Driftsmeldinger]: https://www.brreg.no/om-oss/driftsmeldinger/\n[Driftsmeldinger]\n- [RSS-feed]: https://www.brreg.no/produkter-og-tjenester/rss-feed/\n[RSS-feed].\n\nEksempel på endring som medfører versjonering:\n\n- Fjerne eller endre navn på et attributt i HTTP-responsen.\n\n- Fjerne eller endre navn på et REST endepunkt.\n\n---\n\n## Endringslogg\n<table>\n  <thead>\n    <tr>\n      <th>Versjon</th>\n      <th>Dato</th>\n      <th>Endring</th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <td>1.1.0</td>\n      <td>14. august 2018</td>\n      <td>Ny tjeneste /oppdateringer/enheter og /oppdateringer/underenheter</td>\n    </tr>\n    <tr>\n      <td>1.0.0</td>\n      <td>6. april 2018</td>\n      <td>Produksjonssetting av ny åpne data tjeneste for Enhetsregisteret</td>\n    </tr>\n  </tbody>\n</table>\n",
                        "formats": [
                            "application/json",
                            "application/vnd.enhetsregisteret.enhet.v1+json",
                            "application/vnd.enhetsregisteret.organisasjonsform.v1+json"
                        ],
                        "publisher": {
                            "id": "910244132",
                            "name": "RAMSUND OG ROGNAN REVISJON",
                            "orgPath": "/ANNET/910244132"
                        }
                    }
                },
                {
                    "_index": "dataservices",
                    "_type": "document",
                    "_id": "748bf1e8-909a-460f-9e25-d9b8536184e9",
                    "_score": 1.2,
                    "_source": {
                        "nationalComponent": "true",
                        "isOpenAccess": "true",
                        "isOpenLicense": "true",
                        "isFree": "true",
                        "statusCode": "STABLE",
                        "id": "748bf1e8-909a-460f-9e25-d9b8536184e9",
                        "title": "Åpne Data fra Enhetsregisteret - API Dokumentasjon",
                        "description": "Teknisk beskrivelse av REST-tjenestene i Åpne Data fra Enhetsregisteret - Work in progress\n---\n\n## Ordbok\n### Enhetsregisteret\nRegister over grunndata om juridiske personer og andre enheter. Enhetsregisteret tildeler organisasjonsnummer for entydig identifisering av enheter.\n\n### Organisasjonsnummer\nNisifret nummer som entydig identifiserer enheter i Enhetsregisteret.\n\n### Enhet\nEnhet på øverste nivå i registreringsstrukturen i Enhetsregisteret. Eksempelvis enkeltpersonforetak, foreninger, selskap, sameier og andre som er registrert i Enhetsregisteret. Identifiseres med organisasjonsnummer.\n\n### Underenhet\nEnhet på laveste nivå i registreringsstrukturen i Enhetsregisteret. En underenhet kan ikke eksistere alene og har alltid knytning til en hovedenhet. Identifiseres med organisasjonsnummer.\n\n### Organisasjonsform\nOrganisasjonsform er virksomhetens formelle organisering og gir retningslinjer overfor blant annet ansvarsforhold, skatt, revisjonsplikt, rettigheter og plikter.\n\n### Næringskode\n[Næringskoder]: https://www.brreg.no/bedrift/naeringskoder/\n[Næringskoder] på brreg.no\n\n[Standard for næringsgruppering]: https://www.ssb.no/klass/klassifikasjoner/6\n[Standard for næringsgruppering]\n---\n\n## Versjonering\nDu kan velge major versjon ved å spesifisere HTTP Accept-headeren. Bruk headeren spesifisert i tabellen under. Hvis versjon ikke spesifiseres, vil man få siste versjon.\n\n \n \n API\n Header\n \n \n \n \n /\n application/vnd.enhetsregisteret.v1+json\n \n \n /organisasjonsformer\n application/vnd.enhetsregisteret.organisasjonsform.v1+json\n \n \n\n\n\n### Strategi\nVi skal normalt ikke bryte bakoverkompabiliteten med våre brukere. Likevel kan det være nødvendig i enkelte situasjoner, av for eksempel juridiske årsaker eller vedlikehold, å gjøre endringer som medfører et slikt brudd. Vi vil i dette tilfellet versjonere tjenesten slik at nyeste versjon vil være tilgjengelig sammen med forrige versjon.\n\n#### Dersom man ikke benytter versjonering i accept header, vil man få siste versjon.\n\nEldre versjon vil anses som utdatert/deprecated, og vil på sikt bli tatt bort. Ved behov for denne typen endringer vil vi forsøke å gi bruker god tid, og varsle om endringen i forkant. Se punkt om varsling.\n\n### Når innføres ny versjon\nVi vil innføre en ny versjon når vi introduserer en endring som påvirker bakoverkompabiliteten. Mindre endringer og patcher vil ikke medføre versjonsendring i header.\n\n### Når fjernes en versjon\nVi vil legge ut varsel/driftsmeldinger i god tid på følgende steder:\n- [Driftsmeldinger]: https://www.brreg.no/om-oss/driftsmeldinger/\n[Driftsmeldinger]\n- [RSS-feed]: https://www.brreg.no/produkter-og-tjenester/rss-feed/\n[RSS-feed].\n\nEksempel på endring som medfører versjonering:\n\n- Fjerne eller endre navn på et attributt i HTTP-responsen.\n\n- Fjerne eller endre navn på et REST endepunkt.\n\n---\n\n## Endringslogg\n\n \n \n Versjon\n Dato\n Endring\n \n \n \n \n 1.1.0\n 14. august 2018\n Ny tjeneste /oppdateringer/enheter og /oppdateringer/underenheter\n \n \n 1.0.0\n 6. april 2018\n Produksjonssetting av ny åpne data tjeneste for Enhetsregisteret\n \n \n\n",
                        "descriptionFormatted": "Teknisk beskrivelse av REST-tjenestene i Åpne Data fra Enhetsregisteret - Work in progress\n---\n\n## Ordbok\n### Enhetsregisteret\nRegister over grunndata om juridiske personer og andre enheter. Enhetsregisteret tildeler organisasjonsnummer for entydig identifisering av enheter.\n\n### Organisasjonsnummer\nNisifret nummer som entydig identifiserer enheter i Enhetsregisteret.\n\n### Enhet\nEnhet på øverste nivå i registreringsstrukturen i Enhetsregisteret. Eksempelvis enkeltpersonforetak, foreninger, selskap, sameier og andre som er registrert i Enhetsregisteret. Identifiseres med organisasjonsnummer.\n\n### Underenhet\nEnhet på laveste nivå i registreringsstrukturen i Enhetsregisteret. En underenhet kan ikke eksistere alene og har alltid knytning til en hovedenhet. Identifiseres med organisasjonsnummer.\n\n### Organisasjonsform\nOrganisasjonsform er virksomhetens formelle organisering og gir retningslinjer overfor blant annet ansvarsforhold, skatt, revisjonsplikt, rettigheter og plikter.\n\n### Næringskode\n[Næringskoder]: https://www.brreg.no/bedrift/naeringskoder/\n[Næringskoder]  på brreg.no\n\n[Standard for næringsgruppering]: https://www.ssb.no/klass/klassifikasjoner/6\n[Standard for næringsgruppering]\n---\n\n## Versjonering\nDu kan velge major versjon ved å spesifisere HTTP Accept-headeren. Bruk headeren spesifisert i tabellen under. Hvis versjon ikke spesifiseres, vil man få siste versjon.\n<table>\n  <thead>\n    <tr>\n      <th>API</th>\n      <th>Header</th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <td>/</td>\n      <td>application/vnd.enhetsregisteret.v1+json</td>\n    </tr>\n    <tr>\n      <td>/organisasjonsformer</td>\n      <td>application/vnd.enhetsregisteret.organisasjonsform.v1+json</td>\n    </tr>\n  </tbody>\n</table>\n\n\n### Strategi\nVi skal normalt ikke bryte bakoverkompabiliteten med våre brukere. Likevel kan det være nødvendig i enkelte situasjoner, av for eksempel juridiske årsaker eller vedlikehold, å gjøre endringer som medfører et slikt brudd. Vi vil i dette tilfellet versjonere tjenesten slik at nyeste versjon vil være tilgjengelig sammen med forrige versjon.\n\n#### Dersom man ikke benytter versjonering i accept header, vil man få siste versjon.\n\nEldre versjon vil anses som utdatert/deprecated, og vil på sikt bli tatt bort. Ved behov for denne typen endringer vil vi forsøke å gi bruker god tid, og varsle om endringen i forkant. Se punkt om varsling.\n\n### Når innføres ny versjon\nVi vil innføre en ny versjon når vi introduserer en endring som påvirker bakoverkompabiliteten. Mindre endringer og patcher vil ikke medføre versjonsendring i header.\n\n### Når fjernes en versjon\nVi vil legge ut varsel/driftsmeldinger i god tid på følgende steder:\n- [Driftsmeldinger]: https://www.brreg.no/om-oss/driftsmeldinger/\n[Driftsmeldinger]\n- [RSS-feed]: https://www.brreg.no/produkter-og-tjenester/rss-feed/\n[RSS-feed].\n\nEksempel på endring som medfører versjonering:\n\n- Fjerne eller endre navn på et attributt i HTTP-responsen.\n\n- Fjerne eller endre navn på et REST endepunkt.\n\n---\n\n## Endringslogg\n<table>\n  <thead>\n    <tr>\n      <th>Versjon</th>\n      <th>Dato</th>\n      <th>Endring</th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <td>1.1.0</td>\n      <td>14. august 2018</td>\n      <td>Ny tjeneste /oppdateringer/enheter og /oppdateringer/underenheter</td>\n    </tr>\n    <tr>\n      <td>1.0.0</td>\n      <td>6. april 2018</td>\n      <td>Produksjonssetting av ny åpne data tjeneste for Enhetsregisteret</td>\n    </tr>\n  </tbody>\n</table>\n",
                        "formats": [
                            "application/json",
                            "application/vnd.enhetsregisteret.enhet.v1+json",
                            "application/vnd.enhetsregisteret.organisasjonsform.v1+json"
                        ],
                        "publisher": {
                            "id": "910244132",
                            "name": "RAMSUND OG ROGNAN REVISJON",
                            "orgPath": "/ANNET/910244132"
                        }
                    }
                },
                {
                    "_index": "dataservices",
                    "_type": "document",
                    "_id": "d84027ac-fabc-4c50-b729-a61c6e34683b",
                    "_score": 1.2,
                    "_source": {
                        "nationalComponent": "true",
                        "isOpenAccess": "true",
                        "isOpenLicense": "true",
                        "isFree": "true",
                        "statusCode": "STABLE",
                        "id": "d84027ac-fabc-4c50-b729-a61c6e34683b",
                        "title": "National API Directory Search API",
                        "description": "Provides a basic search api against the National API Directory of Norway",
                        "descriptionFormatted": "Provides a basic search api against the National API Directory of Norway",
                        "formats": [
                            "application/json"
                        ],
                        "publisher": {
                            "id": "910244132",
                            "name": "RAMSUND OG ROGNAN REVISJON",
                            "orgPath": "/ANNET/910244132"
                        }
                    }
                },
                {
                    "_index": "datasets",
                    "_type": "document",
                    "_id": "e39269af-85e1-4a10-a60f-9b767f7d2b27",
                    "_score": 1.2,
                    "_source": {
                        "expandedLosTema": [
                            "kultur",
                            "kultur",
                            "culture",
                            "kultur, idrett og fritid",
                            "kultur, idrett og fritid",
                            "culture, sport and recreation",
                            "film og kino",
                            "film og kino",
                            "film and cinema",
                            "musikk- og kulturskule",
                            "musikk- og kulturskole",
                            "music and arts centres",
                            "kulturtilbod",
                            "kulturtilbud",
                            "cultural activities",
                            "museum",
                            "museum",
                            "museums",
                            "kulturbygg",
                            "kulturbygg",
                            "cultural buildings",
                            "festival",
                            "festival",
                            "festivals",
                            "bibliotektenester",
                            "bibliotektjenester",
                            "library services",
                            "kulturminne",
                            "kulturminner",
                            "cultural heritage",
                            "arkiv",
                            "arkiv",
                            "archives",
                            "slektsforsking",
                            "slektsforskning",
                            "genealogy",
                            "idrettsarrangement",
                            "idrettsarrangement",
                            "sports events",
                            "idrett",
                            "idrett",
                            "sport",
                            "kultur, idrett og fritid",
                            "kultur, idrett og fritid",
                            "culture, sport and recreation",
                            "idrettslag",
                            "idrettslag",
                            "sports clubs",
                            "idrettsforening",
                            "idrettsklubb",
                            "idrettslag",
                            "idrett",
                            "idrett",
                            "sport",
                            "kultur, idrett og fritid",
                            "kultur, idrett og fritid",
                            "culture, sport and recreation",
                            "idrett",
                            "idrett",
                            "sport",
                            "kultur, idrett og fritid",
                            "kultur, idrett og fritid",
                            "culture, sport and recreation",
                            "idrettsanlegg",
                            "idrettsanlegg",
                            "sports facilities",
                            "symjehall",
                            "svømmehall",
                            "swimming pool",
                            "doping",
                            "doping",
                            "doping",
                            "idrettsarrangement",
                            "idrettsarrangement",
                            "sports events",
                            "idrettslag",
                            "idrettslag",
                            "sports clubs"
                        ],
                        "losTheme": [
                            {
                                "children": [
                                    "https://psi.norge.no/los/ord/film-og-kino",
                                    "https://psi.norge.no/los/ord/musikk-og-kulturskole",
                                    "https://psi.norge.no/los/ord/kulturtilbud",
                                    "https://psi.norge.no/los/ord/museum",
                                    "https://psi.norge.no/los/ord/kulturbygg",
                                    "https://psi.norge.no/los/ord/festival",
                                    "https://psi.norge.no/los/ord/bibliotektjenester",
                                    "https://psi.norge.no/los/ord/kulturminner",
                                    "https://psi.norge.no/los/ord/arkiv",
                                    "https://psi.norge.no/los/ord/slektsforskning"
                                ],
                                "parents": [
                                    "https://psi.norge.no/los/tema/kultur-idrett-og-fritid"
                                ],
                                "isTema": "true",
                                "losPaths": [
                                    "kultur-idrett-og-fritid/kultur"
                                ],
                                "name": {
                                    "nn": "Kultur",
                                    "nb": "Kultur",
                                    "en": "Culture"
                                },
                                "uri": "https://psi.norge.no/los/tema/kultur",
                                "synonyms": []
                            },
                            {
                                "parents": [
                                    "https://psi.norge.no/los/tema/idrett"
                                ],
                                "isTema": "false",
                                "losPaths": [
                                    "kultur-idrett-og-fritid/idrett/idrettsarrangement"
                                ],
                                "name": {
                                    "nn": "Idrettsarrangement",
                                    "nb": "Idrettsarrangement",
                                    "en": "Sports events"
                                },
                                "uri": "https://psi.norge.no/los/ord/idrettsarrangement",
                                "synonyms": []
                            },
                            {
                                "parents": [
                                    "https://psi.norge.no/los/tema/idrett"
                                ],
                                "isTema": "false",
                                "losPaths": [
                                    "kultur-idrett-og-fritid/idrett/idrettslag"
                                ],
                                "name": {
                                    "nn": "Idrettslag",
                                    "nb": "Idrettslag",
                                    "en": "Sports clubs"
                                },
                                "uri": "https://psi.norge.no/los/ord/idrettslag",
                                "synonyms": [
                                    "Idrettsforening",
                                    "Idrettsklubb",
                                    "Idrettslag"
                                ],
                                "relatedTerms": [
                                    "https://psi.norge.no/los/ord/lag-og-foreninger"
                                ]
                            },
                            {
                                "children": [
                                    "https://psi.norge.no/los/ord/idrettsanlegg",
                                    "https://psi.norge.no/los/ord/svommehall",
                                    "https://psi.norge.no/los/ord/doping",
                                    "https://psi.norge.no/los/ord/idrettsarrangement",
                                    "https://psi.norge.no/los/ord/idrettslag"
                                ],
                                "parents": [
                                    "https://psi.norge.no/los/tema/kultur-idrett-og-fritid"
                                ],
                                "isTema": "true",
                                "losPaths": [
                                    "kultur-idrett-og-fritid/idrett"
                                ],
                                "name": {
                                    "nn": "Idrett",
                                    "nb": "Idrett",
                                    "en": "Sport"
                                },
                                "uri": "https://psi.norge.no/los/tema/idrett",
                                "synonyms": []
                            }
                        ],
                        "id": "e39269af-85e1-4a10-a60f-9b767f7d2b27",
                        "uri": "http://brreg.no/catalogs/910244132/datasets/b3b8a5b2-b88e-4f3d-95be-1cecb4e9b500",
                        "source": "B",
                        "harvest": {
                            "firstHarvested": "2019-04-29T13:29:00+0200",
                            "lastHarvested": "2020-03-17T01:02:53+0100",
                            "lastChanged": "2020-03-17T01:02:53+0100",
                            "changed": [
                                "2019-04-29T13:29:00+0200",
                                "2019-04-29T13:32:05+0200",
                                "2019-04-30T01:01:55+0200",
                                "2019-05-01T01:02:01+0200",
                                "2019-05-02T01:01:55+0200",
                                "2019-05-03T01:01:58+0200",
                                "2019-05-04T01:01:51+0200",
                                "2019-05-05T01:02:03+0200",
                                "2019-05-06T01:02:08+0200",
                                "2019-05-07T01:02:04+0200",
                                "2019-05-08T01:02:12+0200",
                                "2019-05-09T01:02:04+0200",
                                "2019-05-10T01:02:08+0200",
                                "2019-05-11T01:02:24+0200",
                                "2019-05-12T01:02:23+0200",
                                "2019-05-13T01:02:17+0200",
                                "2019-05-14T01:02:10+0200",
                                "2019-05-14T07:11:46+0200",
                                "2019-05-14T07:34:30+0200",
                                "2019-05-14T07:38:29+0200",
                                "2019-05-14T07:43:47+0200",
                                "2019-05-14T07:44:57+0200",
                                "2019-05-14T15:08:40+0200",
                                "2019-05-15T01:02:38+0200",
                                "2019-05-16T01:02:15+0200",
                                "2019-05-17T01:02:13+0200",
                                "2019-05-18T01:02:06+0200",
                                "2019-05-19T01:02:04+0200",
                                "2019-05-20T01:02:03+0200",
                                "2019-05-20T09:29:02+0200",
                                "2019-05-20T09:41:01+0200",
                                "2019-05-20T09:42:30+0200",
                                "2019-05-21T01:02:32+0200",
                                "2019-05-22T01:03:08+0200",
                                "2019-05-23T01:02:25+0200",
                                "2019-05-23T15:39:02+0200",
                                "2019-05-23T15:40:57+0200",
                                "2019-05-24T01:02:21+0200",
                                "2019-05-24T12:34:57+0200",
                                "2019-05-24T12:36:47+0200",
                                "2019-05-25T01:02:50+0200",
                                "2019-05-26T01:02:39+0200",
                                "2019-05-27T01:02:23+0200",
                                "2019-05-28T01:02:17+0200",
                                "2019-05-29T01:02:11+0200",
                                "2019-05-30T01:02:21+0200",
                                "2019-05-31T01:02:21+0200",
                                "2019-06-01T01:02:18+0200",
                                "2019-06-02T01:02:26+0200",
                                "2019-06-24T13:54:56+0200",
                                "2019-06-25T14:11:41+0200",
                                "2019-06-26T01:03:11+0200",
                                "2019-06-27T01:03:01+0200",
                                "2019-06-28T01:02:52+0200",
                                "2019-06-29T01:02:51+0200",
                                "2019-06-30T01:02:46+0200",
                                "2019-07-01T01:02:45+0200",
                                "2019-07-02T01:02:45+0200",
                                "2019-07-03T01:02:54+0200",
                                "2019-07-04T01:02:51+0200",
                                "2019-07-05T01:02:49+0200",
                                "2019-07-06T01:02:52+0200",
                                "2019-07-07T01:02:47+0200",
                                "2019-07-08T01:03:04+0200",
                                "2019-07-09T01:03:09+0200",
                                "2019-07-10T01:03:22+0200",
                                "2019-07-11T01:03:15+0200",
                                "2019-07-12T01:03:21+0200",
                                "2019-07-13T01:02:57+0200",
                                "2019-07-14T01:03:26+0200",
                                "2019-07-15T01:03:00+0200",
                                "2019-07-16T01:03:06+0200",
                                "2019-07-17T01:03:23+0200",
                                "2019-07-18T01:03:12+0200",
                                "2019-07-19T01:03:00+0200",
                                "2019-07-20T01:03:14+0200",
                                "2019-07-21T01:03:19+0200",
                                "2019-07-22T01:03:24+0200",
                                "2019-07-23T01:03:19+0200",
                                "2019-07-24T01:03:47+0200",
                                "2019-07-25T01:03:03+0200",
                                "2019-07-26T01:03:08+0200",
                                "2019-07-27T01:03:19+0200",
                                "2019-07-28T01:03:01+0200",
                                "2019-07-29T01:03:16+0200",
                                "2019-07-30T01:03:11+0200",
                                "2019-07-31T01:03:19+0200",
                                "2019-07-31T14:29:27+0200",
                                "2019-07-31T15:13:55+0200",
                                "2019-08-01T01:03:35+0200",
                                "2019-08-02T01:03:07+0200",
                                "2019-08-03T01:03:06+0200",
                                "2019-08-04T01:03:03+0200",
                                "2019-08-05T01:03:06+0200",
                                "2019-08-06T01:03:02+0200",
                                "2019-08-07T01:03:01+0200",
                                "2019-08-08T01:03:04+0200",
                                "2019-08-09T01:02:58+0200",
                                "2019-08-10T01:02:58+0200",
                                "2019-08-11T01:02:59+0200",
                                "2019-08-12T01:03:09+0200",
                                "2019-08-12T13:47:43+0200",
                                "2019-08-13T01:03:07+0200",
                                "2019-08-14T01:03:09+0200",
                                "2019-08-15T01:03:18+0200",
                                "2019-08-16T01:03:06+0200",
                                "2019-08-17T01:03:09+0200",
                                "2019-08-18T01:03:00+0200",
                                "2019-08-19T01:03:01+0200",
                                "2019-08-20T01:03:06+0200",
                                "2019-08-20T08:16:53+0200",
                                "2019-08-20T08:30:35+0200",
                                "2019-08-21T01:03:13+0200",
                                "2019-08-22T01:03:10+0200",
                                "2019-08-22T12:26:11+0200",
                                "2019-08-23T01:03:08+0200",
                                "2019-08-24T01:03:05+0200",
                                "2019-08-25T01:03:01+0200",
                                "2019-08-26T01:03:06+0200",
                                "2019-08-27T01:03:21+0200",
                                "2019-08-28T01:03:01+0200",
                                "2019-08-29T01:02:55+0200",
                                "2019-08-30T01:02:58+0200",
                                "2019-08-31T01:03:03+0200",
                                "2019-09-01T01:02:58+0200",
                                "2019-09-02T01:02:59+0200",
                                "2019-09-03T01:03:05+0200",
                                "2019-09-03T15:00:09+0200",
                                "2019-09-04T01:03:04+0200",
                                "2019-09-05T01:03:01+0200",
                                "2019-09-06T01:03:06+0200",
                                "2019-09-07T01:02:58+0200",
                                "2019-09-08T01:02:59+0200",
                                "2019-09-09T01:03:00+0200",
                                "2019-09-10T01:03:01+0200",
                                "2019-09-11T01:03:35+0200",
                                "2019-09-12T01:01:05+0200",
                                "2019-09-13T01:01:00+0200",
                                "2019-09-14T01:01:04+0200",
                                "2019-09-15T01:01:12+0200",
                                "2019-09-16T01:01:10+0200",
                                "2019-09-17T01:03:02+0200",
                                "2019-09-18T01:03:04+0200",
                                "2019-09-19T01:03:09+0200",
                                "2019-09-19T13:06:33+0200",
                                "2019-09-19T14:12:47+0200",
                                "2019-09-19T14:18:24+0200",
                                "2019-09-20T01:03:05+0200",
                                "2019-09-20T09:45:57+0200",
                                "2019-09-20T09:51:54+0200",
                                "2019-09-21T01:03:05+0200",
                                "2019-09-22T01:02:53+0200",
                                "2019-09-23T01:03:26+0200",
                                "2019-09-24T01:03:34+0200",
                                "2019-09-25T01:03:20+0200",
                                "2019-09-26T01:02:57+0200",
                                "2019-09-27T01:03:06+0200",
                                "2019-09-28T01:03:19+0200",
                                "2019-09-29T01:02:57+0200",
                                "2019-09-30T01:02:53+0200",
                                "2019-09-30T10:11:38+0200",
                                "2019-09-30T10:20:55+0200",
                                "2019-09-30T10:23:31+0200",
                                "2019-09-30T13:01:24+0200",
                                "2019-09-30T13:28:52+0200",
                                "2019-09-30T13:32:07+0200",
                                "2019-09-30T13:35:00+0200",
                                "2019-10-01T01:03:07+0200",
                                "2019-10-02T01:03:16+0200",
                                "2019-10-03T01:03:09+0200",
                                "2019-10-04T01:02:59+0200",
                                "2019-10-05T01:02:59+0200",
                                "2019-10-06T01:03:16+0200",
                                "2019-10-07T01:02:56+0200",
                                "2019-10-08T01:03:55+0200",
                                "2019-10-09T01:03:06+0200",
                                "2019-10-10T01:03:05+0200",
                                "2019-10-11T01:02:57+0200",
                                "2019-10-12T01:03:23+0200",
                                "2019-10-13T01:03:26+0200",
                                "2019-10-14T01:02:59+0200",
                                "2019-10-14T16:12:18+0200",
                                "2019-10-15T01:03:42+0200",
                                "2019-10-16T01:03:24+0200",
                                "2019-10-17T01:02:57+0200",
                                "2019-10-18T01:02:55+0200",
                                "2019-10-19T01:03:43+0200",
                                "2019-10-20T01:03:10+0200",
                                "2019-10-21T01:03:02+0200",
                                "2019-10-21T13:09:06+0200",
                                "2019-10-21T13:13:38+0200",
                                "2019-10-22T01:03:24+0200",
                                "2019-10-23T01:02:52+0200",
                                "2019-10-24T01:02:50+0200",
                                "2019-10-25T01:03:04+0200",
                                "2019-10-26T01:04:56+0200",
                                "2019-10-27T01:04:52+0200",
                                "2019-10-28T01:05:02+0100",
                                "2019-10-29T01:02:46+0100",
                                "2019-10-30T01:02:49+0100",
                                "2019-10-31T01:02:51+0100",
                                "2019-11-01T01:03:31+0100",
                                "2019-11-01T14:11:25+0100",
                                "2019-11-02T01:03:16+0100",
                                "2019-11-03T01:03:18+0100",
                                "2019-11-04T01:02:54+0100",
                                "2019-11-05T01:03:03+0100",
                                "2019-11-05T09:43:37+0100",
                                "2019-11-05T09:46:40+0100",
                                "2019-11-05T09:51:01+0100",
                                "2019-11-05T10:03:25+0100",
                                "2019-11-06T01:03:25+0100",
                                "2019-11-07T01:03:00+0100",
                                "2019-11-07T14:56:32+0100",
                                "2019-11-08T01:03:51+0100",
                                "2019-11-09T01:03:18+0100",
                                "2019-11-10T01:03:13+0100",
                                "2019-11-12T17:00:51+0100",
                                "2019-11-13T01:03:08+0100",
                                "2019-11-14T01:03:07+0100",
                                "2019-11-15T01:02:54+0100",
                                "2019-11-16T01:03:13+0100",
                                "2019-11-17T01:03:17+0100",
                                "2019-11-18T01:03:12+0100",
                                "2019-11-19T01:03:35+0100",
                                "2019-11-19T14:27:25+0100",
                                "2019-11-19T14:31:37+0100",
                                "2019-11-20T01:03:26+0100",
                                "2019-11-21T01:03:29+0100",
                                "2019-11-22T01:03:08+0100",
                                "2019-11-23T01:03:03+0100",
                                "2019-11-24T01:03:06+0100",
                                "2019-11-25T01:03:19+0100",
                                "2019-11-26T01:03:07+0100",
                                "2019-11-26T12:54:37+0100",
                                "2019-11-27T01:03:37+0100",
                                "2019-11-27T12:21:46+0100",
                                "2019-11-27T14:40:54+0100",
                                "2019-11-28T01:03:54+0100",
                                "2019-11-28T10:39:47+0100",
                                "2019-11-28T10:44:11+0100",
                                "2019-11-29T01:03:36+0100",
                                "2019-11-29T09:47:46+0100",
                                "2019-11-29T11:36:44+0100",
                                "2019-11-30T01:03:30+0100",
                                "2019-12-01T01:03:56+0100",
                                "2019-12-02T01:03:36+0100",
                                "2019-12-03T01:03:08+0100",
                                "2019-12-03T15:43:59+0100",
                                "2019-12-03T16:34:31+0100",
                                "2019-12-04T01:03:24+0100",
                                "2019-12-05T01:03:17+0100",
                                "2019-12-05T14:53:24+0100",
                                "2019-12-06T01:03:25+0100",
                                "2019-12-06T10:34:37+0100",
                                "2019-12-07T01:03:11+0100",
                                "2019-12-08T01:03:12+0100",
                                "2019-12-09T01:03:24+0100",
                                "2019-12-10T01:03:09+0100",
                                "2019-12-11T01:03:26+0100",
                                "2019-12-12T01:03:49+0100",
                                "2019-12-12T14:51:44+0100",
                                "2019-12-12T14:51:54+0100",
                                "2019-12-13T01:03:28+0100",
                                "2019-12-14T01:04:09+0100",
                                "2019-12-15T01:03:14+0100",
                                "2019-12-16T01:03:15+0100",
                                "2019-12-17T01:03:18+0100",
                                "2019-12-18T01:03:05+0100",
                                "2019-12-18T10:01:28+0100",
                                "2019-12-18T10:01:36+0100",
                                "2019-12-18T10:01:44+0100",
                                "2019-12-18T10:01:54+0100",
                                "2019-12-18T10:02:05+0100",
                                "2019-12-18T10:02:13+0100",
                                "2019-12-18T10:02:21+0100",
                                "2019-12-18T10:02:28+0100",
                                "2019-12-18T10:02:39+0100",
                                "2019-12-18T10:02:48+0100",
                                "2019-12-18T10:02:57+0100",
                                "2019-12-18T10:03:06+0100",
                                "2019-12-18T10:03:14+0100",
                                "2019-12-18T10:03:22+0100",
                                "2019-12-18T10:03:30+0100",
                                "2019-12-18T10:03:40+0100",
                                "2019-12-18T10:04:04+0100",
                                "2019-12-18T10:04:13+0100",
                                "2019-12-18T10:04:32+0100",
                                "2019-12-18T10:04:41+0100",
                                "2019-12-18T10:04:53+0100",
                                "2019-12-18T10:05:04+0100",
                                "2019-12-18T10:06:48+0100",
                                "2019-12-18T10:16:05+0100",
                                "2019-12-18T10:16:11+0100",
                                "2020-02-10T08:13:16+0100",
                                "2020-02-11T01:03:28+0100",
                                "2020-02-12T01:03:51+0100",
                                "2020-02-13T01:03:54+0100",
                                "2020-02-14T01:04:18+0100",
                                "2020-02-15T01:03:52+0100",
                                "2020-02-16T01:03:42+0100",
                                "2020-02-17T01:03:30+0100",
                                "2020-02-18T01:03:49+0100",
                                "2020-02-18T09:46:22+0100",
                                "2020-02-18T12:22:16+0100",
                                "2020-02-18T12:22:26+0100",
                                "2020-02-18T12:22:37+0100",
                                "2020-02-18T12:22:46+0100",
                                "2020-02-18T12:22:57+0100",
                                "2020-02-18T12:23:07+0100",
                                "2020-02-18T12:23:17+0100",
                                "2020-02-18T12:23:25+0100",
                                "2020-02-18T12:23:32+0100",
                                "2020-02-18T12:23:39+0100",
                                "2020-02-18T12:23:48+0100",
                                "2020-02-18T12:23:56+0100",
                                "2020-02-18T12:24:06+0100",
                                "2020-02-18T12:24:15+0100",
                                "2020-02-18T12:24:23+0100",
                                "2020-02-18T12:24:30+0100",
                                "2020-02-18T12:24:37+0100",
                                "2020-02-18T12:24:44+0100",
                                "2020-02-18T12:24:51+0100",
                                "2020-02-18T12:26:05+0100",
                                "2020-02-18T12:26:24+0100",
                                "2020-02-18T12:30:24+0100",
                                "2020-02-18T12:32:52+0100",
                                "2020-02-18T12:33:00+0100",
                                "2020-02-18T12:33:10+0100",
                                "2020-02-18T12:33:19+0100",
                                "2020-02-18T12:33:25+0100",
                                "2020-02-18T12:33:32+0100",
                                "2020-02-18T12:33:40+0100",
                                "2020-02-18T12:33:47+0100",
                                "2020-02-18T12:33:53+0100",
                                "2020-02-18T12:34:00+0100",
                                "2020-02-18T12:43:53+0100",
                                "2020-02-18T12:44:05+0100",
                                "2020-02-18T12:44:13+0100",
                                "2020-02-18T12:44:20+0100",
                                "2020-02-18T12:44:28+0100",
                                "2020-02-18T12:44:36+0100",
                                "2020-02-18T12:44:43+0100",
                                "2020-02-19T01:03:52+0100",
                                "2020-02-20T01:05:02+0100",
                                "2020-02-20T10:10:22+0100",
                                "2020-02-20T10:10:31+0100",
                                "2020-02-20T10:10:41+0100",
                                "2020-02-20T10:10:50+0100",
                                "2020-02-20T10:11:02+0100",
                                "2020-02-20T10:11:13+0100",
                                "2020-02-20T10:11:25+0100",
                                "2020-02-20T10:11:34+0100",
                                "2020-02-20T10:11:43+0100",
                                "2020-02-20T10:11:51+0100",
                                "2020-02-20T10:11:59+0100",
                                "2020-02-20T10:12:08+0100",
                                "2020-02-20T10:12:18+0100",
                                "2020-02-20T10:12:28+0100",
                                "2020-02-20T10:12:37+0100",
                                "2020-02-20T10:12:48+0100",
                                "2020-02-20T10:12:55+0100",
                                "2020-02-20T10:13:05+0100",
                                "2020-02-20T10:13:14+0100",
                                "2020-02-20T10:13:23+0100",
                                "2020-02-20T10:13:35+0100",
                                "2020-02-20T10:13:45+0100",
                                "2020-02-20T10:13:52+0100",
                                "2020-02-20T10:14:02+0100",
                                "2020-02-20T10:14:12+0100",
                                "2020-02-20T10:14:21+0100",
                                "2020-02-20T10:14:31+0100",
                                "2020-02-20T10:14:41+0100",
                                "2020-02-20T10:14:49+0100",
                                "2020-02-20T10:14:57+0100",
                                "2020-02-20T10:15:06+0100",
                                "2020-02-20T10:15:15+0100",
                                "2020-02-20T10:15:27+0100",
                                "2020-02-20T10:15:36+0100",
                                "2020-02-20T10:15:45+0100",
                                "2020-02-20T10:37:22+0100",
                                "2020-02-20T10:37:31+0100",
                                "2020-02-20T10:37:39+0100",
                                "2020-02-20T10:37:47+0100",
                                "2020-02-20T10:37:57+0100",
                                "2020-03-03T08:04:45+0100",
                                "2020-03-03T08:05:39+0100",
                                "2020-03-03T08:05:47+0100",
                                "2020-03-03T08:05:56+0100",
                                "2020-03-03T08:06:07+0100",
                                "2020-03-03T08:06:16+0100",
                                "2020-03-03T08:06:26+0100",
                                "2020-03-03T08:06:34+0100",
                                "2020-03-03T08:06:43+0100",
                                "2020-03-04T01:03:54+0100",
                                "2020-03-05T01:03:51+0100",
                                "2020-03-05T13:49:50+0100",
                                "2020-03-05T13:50:10+0100",
                                "2020-03-05T13:50:18+0100",
                                "2020-03-05T14:35:25+0100",
                                "2020-03-06T01:03:06+0100",
                                "2020-03-06T09:56:06+0100",
                                "2020-03-07T01:03:09+0100",
                                "2020-03-08T01:02:54+0100",
                                "2020-03-09T01:03:21+0100",
                                "2020-03-09T08:28:58+0100",
                                "2020-03-09T08:29:04+0100",
                                "2020-03-09T08:29:10+0100",
                                "2020-03-09T08:29:16+0100",
                                "2020-03-09T08:29:21+0100",
                                "2020-03-09T08:29:27+0100",
                                "2020-03-09T08:29:33+0100",
                                "2020-03-09T08:29:43+0100",
                                "2020-03-09T08:30:01+0100",
                                "2020-03-09T13:29:33+0100",
                                "2020-03-09T13:29:39+0100",
                                "2020-03-09T13:30:40+0100",
                                "2020-03-09T13:30:47+0100",
                                "2020-03-09T13:32:35+0100",
                                "2020-03-09T13:32:42+0100",
                                "2020-03-09T13:33:02+0100",
                                "2020-03-09T13:33:08+0100",
                                "2020-03-09T13:33:14+0100",
                                "2020-03-09T13:33:20+0100",
                                "2020-03-09T13:33:26+0100",
                                "2020-03-09T13:33:33+0100",
                                "2020-03-09T13:34:22+0100",
                                "2020-03-09T13:35:41+0100",
                                "2020-03-09T13:35:47+0100",
                                "2020-03-09T14:07:39+0100",
                                "2020-03-09T14:07:53+0100",
                                "2020-03-09T14:08:00+0100",
                                "2020-03-10T01:03:02+0100",
                                "2020-03-10T13:19:27+0100",
                                "2020-03-11T01:02:58+0100",
                                "2020-03-12T01:02:53+0100",
                                "2020-03-13T01:03:01+0100",
                                "2020-03-14T01:03:02+0100",
                                "2020-03-15T01:03:05+0100",
                                "2020-03-16T01:02:55+0100",
                                "2020-03-17T01:02:53+0100"
                            ]
                        },
                        "title": {
                            "nb": "Viking"
                        },
                        "description": {
                            "nb": "Fotballlag frå Stavanger"
                        },
                        "descriptionFormatted": {
                            "nb": "Fotballlag frå Stavanger"
                        },
                        "objective": {
                            "nb": "Prodtest "
                        },
                        "contactPoint": [
                            {
                                "email": "mail@post.no",
                                "organizationUnit": "Avdelingsjæfen",
                                "hasURL": "https://kontakt.no",
                                "hasTelephone": "+4711234566"
                            }
                        ],
                        "publisher": {
                            "type": "no.dcat.datastore.domain.dcat.Publisher",
                            "valid": "false",
                            "uri": "http://data.brreg.no/enhetsregisteret/enhet/910244132",
                            "id": "910244132",
                            "name": "RAMSUND OG ROGNAN REVISJON",
                            "orgPath": "/ANNET/910244132"
                        },
                        "issued": "2019-04-15T00:00:00+0200",
                        "modified": "2019-04-03T00:00:00+0200",
                        "language": [
                            {
                                "uri": "http://publications.europa.eu/resource/authority/language/NOR",
                                "code": "NOR",
                                "prefLabel": {
                                    "nb": "Norsk",
                                    "nn": "Norsk",
                                    "no": "Norsk",
                                    "en": "Norwegian"
                                }
                            }
                        ],
                        "landingPage": [],
                        "theme": [
                            {
                                "id": "https://psi.norge.no/los/tema/kultur"
                            },
                            {
                                "id": "https://psi.norge.no/los/ord/idrettsarrangement"
                            },
                            {
                                "id": "https://psi.norge.no/los/ord/idrettslag"
                            },
                            {
                                "id": "https://psi.norge.no/los/tema/idrett"
                            }
                        ],
                        "distribution": [
                            {
                                "description": {
                                    "nb": "asdasd asdasdasd"
                                },
                                "downloadURL": [],
                                "accessURL": [
                                    "https://vg.no"
                                ],
                                "license": {
                                    "uri": "http://creativecommons.org/publicdomain/zero/1.0/",
                                    "prefLabel": {
                                        "en": "Creative Commons Universal Public Domain Dedication",
                                        "no": "Creative Commons Universal Fristatus-erklæring"
                                    },
                                    "extraType": "http://purl.org/dc/terms/LicenseDocument"
                                },
                                "openLicense": "true",
                                "format": [
                                    "json"
                                ],
                                "type": "API"
                            },
                            {
                                "downloadURL": [],
                                "accessURL": [],
                                "openLicense": "false",
                                "type": "API",
                                "accessService": {
                                    "uri": "http://dataset-catalogue:8080/catalogs/c3b03260-b370-4ec5-bdc4-7e69ffe0b4dd",
                                    "description": {
                                        "nb": "Nasjonalt skoleregister API"
                                    },
                                    "endpointDescription": [
                                        {
                                            "uri": "119f6f04-bc9b-486e-86b3-f74a46f8dccd",
                                            "extraType": "http://xmlns.com/foaf/0.1/Document"
                                        }
                                    ]
                                }
                            }
                        ],
                        "sample": [
                            {
                                "description": {
                                    "nb": "eksempel asd laksjdh pdisfsva adf asdf ADFs "
                                },
                                "downloadURL": [],
                                "accessURL": [
                                    "https://vg.no"
                                ],
                                "openLicense": "false",
                                "format": [
                                    "json"
                                ]
                            }
                        ],
                        "temporal": [
                            {
                                "startDate": "2019-04-01T00:00:00+0200",
                                "endDate": "2019-05-05T00:00:00+0200"
                            }
                        ],
                        "spatial": [
                            {
                                "uri": "https://data.geonorge.no/administrativeEnheter/fylke/id/173142",
                                "code": "https://data.geonorge.no/administrativeEnheter/fylke/id/173142",
                                "prefLabel": {
                                    "no": "Finnmárku"
                                }
                            }
                        ],
                        "accessRights": {
                            "uri": "http://publications.europa.eu/resource/authority/access-right/PUBLIC",
                            "code": "PUBLIC",
                            "prefLabel": {
                                "en": "Public",
                                "nb": "Offentlig",
                                "nn": "Offentlig"
                            }
                        },
                        "hasAccuracyAnnotation": {
                            "inDimension": "http://iso.org/25012/2008/dataquality/Accuracy",
                            "hasBody": {
                                "nb": "nøyaktig"
                            }
                        },
                        "hasCompletenessAnnotation": {
                            "inDimension": "http://iso.org/25012/2008/dataquality/Completeness",
                            "hasBody": {
                                "nb": "komplett"
                            }
                        },
                        "hasCurrentnessAnnotation": {
                            "inDimension": "http://iso.org/25012/2008/dataquality/Currentness",
                            "hasBody": {
                                "nb": "ert"
                            }
                        },
                        "hasAvailabilityAnnotation": {
                            "inDimension": "http://iso.org/25012/2008/dataquality/Availability",
                            "hasBody": {
                                "nb": "tilgjengelig"
                            }
                        },
                        "hasRelevanceAnnotation": {
                            "inDimension": "http://iso.org/25012/2008/dataquality/Relevance",
                            "hasBody": {
                                "nb": "asdasd"
                            }
                        },
                        "references": [
                            {
                                "referenceType": {
                                    "uri": "http://purl.org/dc/terms/isPartOf",
                                    "code": "isPartOf",
                                    "prefLabel": {
                                        "en": "Is Part Of",
                                        "nn": "Er del av",
                                        "nb": "Er en del av"
                                    }
                                },
                                "source": {
                                    "uri": "http://brreg.no/catalogs/910244132/datasets/2468de68-f6e0-4158-a4ab-e3c86034f4a5"
                                }
                            },
                            {
                                "referenceType": {
                                    "uri": "http://purl.org/dc/terms/requires",
                                    "code": "requires",
                                    "prefLabel": {
                                        "en": "Requires",
                                        "nn": "Krevjar",
                                        "nb": "Krever"
                                    }
                                },
                                "source": {
                                    "uri": "http://brreg.no/catalogs/910244132/datasets/5325dea3-eb86-4e89-ac77-12f3c32cfb3f"
                                }
                            }
                        ],
                        "provenance": {
                            "uri": "http://data.brreg.no/datakatalog/provinens/nasjonal",
                            "code": "NASJONAL",
                            "prefLabel": {
                                "en": "Authoritativ source",
                                "nb": "Autoritativ kilde",
                                "nn": "Autoritativ kilde"
                            }
                        },
                        "accrualPeriodicity": {
                            "uri": "http://publications.europa.eu/resource/authority/frequency/ANNUAL",
                            "code": "ANNUAL",
                            "prefLabel": {
                                "de": "jährlich",
                                "lv": "reizi gadā",
                                "bg": "годишен",
                                "nl": "jaarlijks",
                                "sk": "ročný",
                                "no": "årlig",
                                "sv": "årlig",
                                "pl": "roczny",
                                "hr": "godišnje",
                                "sl": "letni",
                                "fi": "vuotuinen",
                                "mt": "annwali",
                                "lt": "kasmetinis",
                                "fr": "annuel",
                                "ga": "bliantúil",
                                "da": "årligt",
                                "et": "aastane",
                                "pt": "anual",
                                "ro": "anual",
                                "es": "anual",
                                "el": "ετήσιος",
                                "en": "annual",
                                "cs": "roční",
                                "it": "annuale",
                                "hu": "évenkénti"
                            }
                        },
                        "subject": [
                            {
                                "uri": "https://fellesdatakatalog.brreg.no/api/concepts/fd0fe2be-c84e-4729-8b54-2a69ec6ab04e",
                                "identifier": "http://begrepskatalogen/begrep/46f4d762-4c6c-11e8-bb3e-005056821322",
                                "prefLabel": {
                                    "nb": "saksbehandleridentifikator"
                                },
                                "definition": {
                                    "nb": "bruker-identifikatoren til den saksbehandleren som har utført en bestemt tilstandsendring i et gitt informasjonselement"
                                }
                            },
                            {
                                "uri": "https://fellesdatakatalog.brreg.no/api/concepts/53187c64-9e2e-4766-8d15-f778dbc94f7d",
                                "identifier": "http://data.brreg.no/begrep/40660",
                                "prefLabel": {
                                    "nb": "term"
                                },
                                "definition": {
                                    "nb": "\"betegnelse for et allmennbegrep som tilhører et fagområde\"\n"
                                }
                            }
                        ],
                        "conformsTo": [
                            {
                                "uri": "https://viking.no",
                                "extraType": "http://purl.org/dc/terms/Standard"
                            }
                        ],
                        "informationModel": [
                            {
                                "uri": "https://infomodell.no",
                                "prefLabel": {
                                    "nb": "Nr"
                                },
                                "extraType": "http://purl.org/dc/terms/Standard"
                            }
                        ],
                        "type": "Data",
                        "catalog": {
                            "id": "910244132",
                            "uri": "http://dataset-catalogue:8080/catalogs/910244132",
                            "title": {
                                "nb": "Datakatalog for RAMSUND OG ROGNAN REVISJON"
                            },
                            "publisher": {
                                "type": "no.dcat.datastore.domain.dcat.Publisher",
                                "valid": "false",
                                "uri": "http://data.brreg.no/enhetsregisteret/enhet/910244132",
                                "id": "910244132",
                                "name": "RAMSUND OG ROGNAN REVISJON",
                                "orgPath": "/ANNET/910244132"
                            }
                        }
                    }
                },
                {
                    "_index": "datasets",
                    "_type": "document",
                    "_id": "6e2804ba-053e-4263-a465-de093fa90d83",
                    "_score": 1.2,
                    "_source": {
                        "id": "6e2804ba-053e-4263-a465-de093fa90d83",
                        "uri": "http://brreg.no/catalogs/910244132/datasets/e89629a3-701f-40f4-acae-fe422029da9f",
                        "source": "B",
                        "harvest": {
                            "firstHarvested": "2019-01-29T14:32:50+0100",
                            "lastHarvested": "2020-03-17T01:02:53+0100",
                            "lastChanged": "2020-03-13T01:03:01+0100",
                            "changed": [
                                "2019-01-29T14:32:50+0100",
                                "2019-02-28T01:01:41+0100",
                                "2019-03-30T01:01:39+0100",
                                "2019-04-02T10:06:35+0200",
                                "2019-05-03T01:01:58+0200",
                                "2019-06-02T01:02:26+0200",
                                "2019-06-24T13:54:56+0200",
                                "2019-07-25T01:03:03+0200",
                                "2019-08-24T01:03:05+0200",
                                "2019-09-23T01:03:26+0200",
                                "2019-10-23T01:02:52+0200",
                                "2019-11-21T01:03:29+0100",
                                "2020-02-10T08:13:16+0100",
                                "2020-02-12T01:03:51+0100",
                                "2020-03-13T01:03:01+0100"
                            ]
                        },
                        "title": {
                            "nb": "Ny informasjonsmodell"
                        },
                        "description": {
                            "nb": "Dagnes beskrivelse "
                        },
                        "descriptionFormatted": {
                            "nb": "Dagnes beskrivelse "
                        },
                        "objective": {
                            "nb": "Formål formål hei hei hei"
                        },
                        "contactPoint": [
                            {
                                "email": "post@post.no",
                                "organizationUnit": "https://vg.no"
                            }
                        ],
                        "publisher": {
                            "type": "no.dcat.datastore.domain.dcat.Publisher",
                            "valid": "false",
                            "uri": "http://data.brreg.no/enhetsregisteret/enhet/910244132",
                            "id": "910244132",
                            "name": "RAMSUND OG ROGNAN REVISJON",
                            "orgPath": "/ANNET/910244132"
                        },
                        "issued": "2019-01-29T00:00:00+0100",
                        "language": [
                            {
                                "uri": "http://publications.europa.eu/resource/authority/language/NOR",
                                "code": "NOR",
                                "prefLabel": {
                                    "nb": "Norsk",
                                    "nn": "Norsk",
                                    "no": "Norsk",
                                    "en": "Norwegian"
                                }
                            }
                        ],
                        "landingPage": [
                            "https://vg.no"
                        ],
                        "theme": [
                            {
                                "id": "http://publications.europa.eu/resource/authority/data-theme/ENVI",
                                "code": "ENVI",
                                "startUse": "2015-10-01",
                                "title": {
                                    "nl": "Milieu",
                                    "lv": "Vide",
                                    "mt": "Ambjent",
                                    "nb": "Miljø",
                                    "lt": "Aplinka",
                                    "ro": "Mediu",
                                    "en": "Environment",
                                    "da": "Miljø",
                                    "cs": "Životní prostředí",
                                    "pt": "Ambiente",
                                    "it": "Ambiente",
                                    "bg": "Околна среда",
                                    "fi": "Ympäristö",
                                    "de": "Umwelt",
                                    "hu": "Környezet",
                                    "es": "Medio ambiente",
                                    "ga": "Comhshaol",
                                    "fr": "Environnement",
                                    "el": "Περιβάλλον",
                                    "sl": "Okolje",
                                    "hr": "Okoliš",
                                    "et": "Keskkond",
                                    "sv": "Miljö",
                                    "pl": "Środowisko",
                                    "sk": "Životné prostredie"
                                },
                                "conceptSchema": {
                                    "id": "http://publications.europa.eu/resource/authority/data-theme",
                                    "title": {
                                        "en": "Dataset types Named Authority List"
                                    },
                                    "versioninfo": "20160921-0",
                                    "versionnumber": "20160921-0"
                                }
                            }
                        ],
                        "sample": [
                            {
                                "description": {
                                    "nb": "asdfghjklø"
                                },
                                "downloadURL": [],
                                "accessURL": [
                                    "https://vg.no"
                                ],
                                "openLicense": "false",
                                "format": [
                                    "application/AML"
                                ]
                            }
                        ],
                        "temporal": [
                            {
                                "startDate": "2019-01-23T00:00:00+0100",
                                "endDate": "2022-01-25T00:00:00+0100"
                            }
                        ],
                        "accessRights": {
                            "uri": "http://publications.europa.eu/resource/authority/access-right/PUBLIC",
                            "code": "PUBLIC",
                            "prefLabel": {
                                "en": "Public",
                                "nb": "Offentlig",
                                "nn": "Offentlig"
                            }
                        },
                        "hasAccuracyAnnotation": {
                            "inDimension": "http://iso.org/25012/2008/dataquality/Accuracy",
                            "hasBody": {
                                "nb": "asdasd"
                            }
                        },
                        "hasCompletenessAnnotation": {
                            "inDimension": "http://iso.org/25012/2008/dataquality/Completeness",
                            "hasBody": {
                                "nb": "asdasd"
                            }
                        },
                        "hasAvailabilityAnnotation": {
                            "inDimension": "http://iso.org/25012/2008/dataquality/Availability",
                            "hasBody": {
                                "nb": "asdasd"
                            }
                        },
                        "hasRelevanceAnnotation": {
                            "inDimension": "http://iso.org/25012/2008/dataquality/Relevance",
                            "hasBody": {
                                "nb": "aasdasd"
                            }
                        },
                        "references": [
                            {
                                "referenceType": {
                                    "uri": "http://purl.org/dc/terms/isPartOf",
                                    "code": "isPartOf",
                                    "prefLabel": {
                                        "en": "Is Part Of",
                                        "nn": "Er del av",
                                        "nb": "Er en del av"
                                    }
                                },
                                "source": {
                                    "uri": "http://brreg.no/catalogs/910244132/datasets/226d50d8-8f53-401f-b368-8879b48a276f"
                                }
                            },
                            {
                                "referenceType": {
                                    "uri": "http://purl.org/dc/terms/isReplacedBy",
                                    "code": "isReplacedBy",
                                    "prefLabel": {
                                        "en": "Is replaced by",
                                        "nn": "Er erstatta av",
                                        "nb": "Er erstattet av"
                                    }
                                },
                                "source": {
                                    "uri": "http://brreg.no/catalogs/910244132/datasets/a1c26cb4-fb8f-449d-bc7c-d502d535ba33"
                                }
                            }
                        ],
                        "provenance": {
                            "uri": "http://data.brreg.no/datakatalog/provinens/nasjonal",
                            "code": "NASJONAL",
                            "prefLabel": {
                                "en": "Authoritativ source",
                                "nb": "Autoritativ kilde",
                                "nn": "Autoritativ kilde"
                            }
                        },
                        "subject": [
                            {
                                "uri": "https://fellesdatakatalog.brreg.no/api/concepts/f0d1288a-bc36-4477-ac5c-4e5a4a4cff96",
                                "identifier": "http://data.brreg.no/begrep/43443",
                                "prefLabel": {
                                    "nb": "saksøkt"
                                },
                                "definition": {
                                    "nb": "den som det blir reist sak mot, eller som en begjæring om tvangsfullbyrdelse er rettet mot"
                                }
                            }
                        ],
                        "conformsTo": [
                            {
                                "uri": "https://vg.no",
                                "prefLabel": {
                                    "nb": "Avis"
                                },
                                "extraType": "http://purl.org/dc/terms/Standard"
                            }
                        ],
                        "informationModel": [
                            {
                                "uri": "https://vg.no",
                                "prefLabel": {
                                    "nb": "APi"
                                },
                                "extraType": "http://purl.org/dc/terms/Standard"
                            }
                        ],
                        "type": "Data",
                        "catalog": {
                            "id": "910244132",
                            "uri": "http://dataset-catalogue:8080/catalogs/910244132",
                            "title": {
                                "nb": "Datakatalog for RAMSUND OG ROGNAN REVISJON"
                            },
                            "publisher": {
                                "type": "no.dcat.datastore.domain.dcat.Publisher",
                                "valid": "false",
                                "uri": "http://data.brreg.no/enhetsregisteret/enhet/910244132",
                                "id": "910244132",
                                "name": "RAMSUND OG ROGNAN REVISJON",
                                "orgPath": "/ANNET/910244132"
                            }
                        }
                    }
                },
                {
                    "_index": "datasets",
                    "_type": "document",
                    "_id": "2ce24a39-de2f-4659-a497-1c565990c9b8",
                    "_score": 1.2,
                    "_source": {
                        "id": "2ce24a39-de2f-4659-a497-1c565990c9b8",
                        "uri": "http://brreg.no/catalogs/910244132/datasets/c32b7a4f-655f-45f6-88f6-d01f05d0f7c2",
                        "source": "B",
                        "harvest": {
                            "firstHarvested": "2018-11-07T01:00:13+0100",
                            "lastHarvested": "2020-03-17T01:02:53+0100",
                            "lastChanged": "2020-03-13T01:03:01+0100",
                            "changed": [
                                "2018-11-07T01:00:13+0100",
                                "2018-11-07T12:11:18+0100",
                                "2018-11-08T01:00:11+0100",
                                "2018-11-16T15:59:23+0100",
                                "2019-01-15T13:10:53+0100",
                                "2019-02-14T01:01:40+0100",
                                "2019-03-16T01:01:55+0100",
                                "2019-04-02T10:06:35+0200",
                                "2019-05-03T01:01:58+0200",
                                "2019-06-02T01:02:26+0200",
                                "2019-06-24T13:54:56+0200",
                                "2019-07-25T01:03:03+0200",
                                "2019-08-24T01:03:05+0200",
                                "2019-09-23T01:03:26+0200",
                                "2019-10-23T01:02:52+0200",
                                "2019-11-21T01:03:29+0100",
                                "2020-02-10T08:13:16+0100",
                                "2020-02-12T01:03:51+0100",
                                "2020-03-13T01:03:01+0100"
                            ]
                        },
                        "title": {
                            "nb": "Fint datasett"
                        },
                        "description": {
                            "nb": "bbbb"
                        },
                        "descriptionFormatted": {
                            "nb": "bbbb"
                        },
                        "contactPoint": [],
                        "publisher": {
                            "type": "no.dcat.datastore.domain.dcat.Publisher",
                            "valid": "false",
                            "uri": "http://data.brreg.no/enhetsregisteret/enhet/910244132",
                            "id": "910244132",
                            "name": "RAMSUND OG ROGNAN REVISJON",
                            "orgPath": "/ANNET/910244132"
                        },
                        "landingPage": [],
                        "theme": [
                            {
                                "id": "http://publications.europa.eu/resource/authority/data-theme/EDUC",
                                "code": "EDUC",
                                "startUse": "2015-10-01",
                                "title": {
                                    "sv": "Utbildning, kultur och sport",
                                    "sk": "Vzdelávanie, kultúra a šport",
                                    "pt": "Educação, cultura e desporto",
                                    "en": "Education, culture and sport",
                                    "fr": "Éducation, culture et sport",
                                    "hr": "Obrazovanje, kultura i sport",
                                    "sl": "Izobraževanje, kultura in šport",
                                    "mt": "Edukazzjoni, kultura u sport",
                                    "de": "Bildung, Kultur und Sport",
                                    "cs": "Vzdělávání, kultura a sport",
                                    "it": "Istruzione, cultura e sport",
                                    "es": "Educación, cultura y deportes",
                                    "nb": "Utdanning, kultur og sport",
                                    "da": "Uddannelse, kultur og sport",
                                    "nl": "Onderwijs, cultuur en sport",
                                    "bg": "Образование, култура и спорт",
                                    "ro": "Educaţie, cultură şi sport",
                                    "fi": "Koulutus, kulttuuri ja urheilu",
                                    "lt": "Švietimas, kultūra ir sportas",
                                    "hu": "Oktatás, kultúra és sport",
                                    "lv": "Izglītība, kultūra un sports",
                                    "el": "Παιδεία, πολιτιστικά θέματα και αθλητισμός",
                                    "ga": "Oideachas, cultúr agus spórt",
                                    "pl": "Edukacja, kultura i sport",
                                    "et": "Haridus, kultuur ja sport"
                                },
                                "conceptSchema": {
                                    "id": "http://publications.europa.eu/resource/authority/data-theme",
                                    "title": {
                                        "en": "Dataset types Named Authority List"
                                    },
                                    "versioninfo": "20160921-0",
                                    "versionnumber": "20160921-0"
                                }
                            }
                        ],
                        "accessRights": {
                            "uri": "http://publications.europa.eu/resource/authority/access-right/PUBLIC",
                            "code": "PUBLIC",
                            "prefLabel": {
                                "en": "Public",
                                "nb": "Offentlig",
                                "nn": "Offentlig"
                            }
                        },
                        "provenance": {
                            "uri": "http://data.brreg.no/datakatalog/provinens/nasjonal",
                            "code": "NASJONAL",
                            "prefLabel": {
                                "en": "Authoritativ source",
                                "nb": "Autoritativ kilde",
                                "nn": "Autoritativ kilde"
                            }
                        },
                        "catalog": {
                            "id": "910244132",
                            "uri": "http://dataset-catalogue:8080/catalogs/910244132",
                            "title": {
                                "nb": "Datakatalog for RAMSUND OG ROGNAN REVISJON"
                            },
                            "publisher": {
                                "type": "no.dcat.datastore.domain.dcat.Publisher",
                                "valid": "false",
                                "uri": "http://data.brreg.no/enhetsregisteret/enhet/910244132",
                                "id": "910244132",
                                "name": "RAMSUND OG ROGNAN REVISJON",
                                "orgPath": "/ANNET/910244132"
                            }
                        }
                    }
                },
                {
                    "_index": "datasets",
                    "_type": "document",
                    "_id": "51109f61-d9e3-465d-9ffa-e5e6b9e78136",
                    "_score": 1.2,
                    "_source": {
                        "id": "51109f61-d9e3-465d-9ffa-e5e6b9e78136",
                        "uri": "http://brreg.no/catalogs/910244132/datasets/a0105569-d731-4eeb-aa09-44db32e4642c",
                        "source": "B",
                        "harvest": {
                            "firstHarvested": "2019-01-07T15:32:46+0100",
                            "lastHarvested": "2020-03-17T01:02:53+0100",
                            "lastChanged": "2020-03-13T01:03:01+0100",
                            "changed": [
                                "2019-01-07T15:32:46+0100",
                                "2019-01-15T13:10:53+0100",
                                "2019-02-14T01:01:40+0100",
                                "2019-03-16T01:01:55+0100",
                                "2019-04-02T10:06:35+0200",
                                "2019-05-03T01:01:58+0200",
                                "2019-06-02T01:02:26+0200",
                                "2019-06-24T13:54:56+0200",
                                "2019-07-25T01:03:03+0200",
                                "2019-08-24T01:03:05+0200",
                                "2019-09-23T01:03:26+0200",
                                "2019-10-23T01:02:52+0200",
                                "2019-11-21T01:03:29+0100",
                                "2020-02-10T08:13:16+0100",
                                "2020-02-12T01:03:51+0100",
                                "2020-03-13T01:03:01+0100"
                            ]
                        },
                        "title": {
                            "nb": "Nå er jula over"
                        },
                        "description": {
                            "nb": "Bare tull"
                        },
                        "descriptionFormatted": {
                            "nb": "Bare tull"
                        },
                        "objective": {
                            "nb": "Test"
                        },
                        "contactPoint": [
                            {
                                "email": "post@post.no",
                                "organizationUnit": "aaa",
                                "hasURL": "http://vg.no",
                                "hasTelephone": "12345678"
                            }
                        ],
                        "publisher": {
                            "type": "no.dcat.datastore.domain.dcat.Publisher",
                            "valid": "false",
                            "uri": "http://data.brreg.no/enhetsregisteret/enhet/910244132",
                            "id": "910244132",
                            "name": "RAMSUND OG ROGNAN REVISJON",
                            "orgPath": "/ANNET/910244132"
                        },
                        "modified": "2019-01-09T00:00:00+0100",
                        "landingPage": [
                            "http://vg.no"
                        ],
                        "theme": [
                            {
                                "id": "http://publications.europa.eu/resource/authority/data-theme/GOVE",
                                "code": "GOVE",
                                "startUse": "2015-10-01",
                                "title": {
                                    "it": "Governo e settore pubblico",
                                    "nb": "Forvaltning og offentlig sektor",
                                    "en": "Government and public sector",
                                    "hr": "Vlada i javni sektor",
                                    "es": "Gobierno y sector público",
                                    "de": "Regierung und öffentlicher Sektor",
                                    "sk": "Vláda a verejný sektor",
                                    "ro": "Guvern şi sector public",
                                    "bg": "Правителство и публичен сектор",
                                    "et": "Valitsus ja avalik sektor",
                                    "el": "Κυβέρνηση και δημόσιος τομέας",
                                    "pl": "Rząd i sektor publiczny",
                                    "cs": "Vláda a veřejný sektor",
                                    "ga": "Rialtas agus earnáil phoiblí",
                                    "pt": "Governo e setor público",
                                    "lt": "Vyriausybė ir viešasis sektorius",
                                    "lv": "Valdība un sabiedriskais sektors",
                                    "mt": "Gvern u settur pubbliku",
                                    "hu": "Kormányzat és közszféra",
                                    "da": "Regeringen og den offentlige sektor",
                                    "fi": "Valtioneuvosto ja julkinen sektori",
                                    "fr": "Gouvernement et secteur public",
                                    "sl": "Vlada in javni sektor",
                                    "sv": "Regeringen och den offentliga sektorn",
                                    "nl": "Overheid en publieke sector"
                                },
                                "conceptSchema": {
                                    "id": "http://publications.europa.eu/resource/authority/data-theme",
                                    "title": {
                                        "en": "Dataset types Named Authority List"
                                    },
                                    "versioninfo": "20160921-0",
                                    "versionnumber": "20160921-0"
                                }
                            }
                        ],
                        "distribution": [
                            {
                                "description": {
                                    "nb": "asdasda"
                                },
                                "downloadURL": [],
                                "accessURL": [
                                    "http://vg.no"
                                ],
                                "license": {
                                    "uri": "http://creativecommons.org/licenses/by/4.0/",
                                    "prefLabel": {
                                        "en": "Creative Commons Attribution 4.0 International",
                                        "no": "Creative Commons Navngivelse 4.0 Internasjonal"
                                    },
                                    "extraType": "http://purl.org/dc/terms/LicenseDocument"
                                },
                                "openLicense": "true",
                                "page": [
                                    {
                                        "uri": "http://vg.no",
                                        "extraType": "http://xmlns.com/foaf/0.1/Document"
                                    }
                                ],
                                "format": [
                                    "application/json"
                                ],
                                "type": "API"
                            }
                        ],
                        "sample": [
                            {
                                "description": {
                                    "nb": "asdasd"
                                },
                                "downloadURL": [],
                                "accessURL": [
                                    "http://vg.no"
                                ],
                                "openLicense": "false"
                            }
                        ],
                        "accessRights": {
                            "uri": "http://publications.europa.eu/resource/authority/access-right/RESTRICTED",
                            "code": "RESTRICTED",
                            "prefLabel": {
                                "nb": "Begrenset",
                                "nn": "Begrenset",
                                "en": "Restricted"
                            }
                        },
                        "hasAccuracyAnnotation": {
                            "inDimension": "http://iso.org/25012/2008/dataquality/Accuracy",
                            "hasBody": {
                                "nb": "asdasd"
                            }
                        },
                        "hasCompletenessAnnotation": {
                            "inDimension": "http://iso.org/25012/2008/dataquality/Completeness",
                            "hasBody": {
                                "nb": "asdasd"
                            }
                        },
                        "hasCurrentnessAnnotation": {
                            "inDimension": "http://iso.org/25012/2008/dataquality/Currentness",
                            "hasBody": {
                                "nb": "Aktuelt så det holder"
                            }
                        },
                        "hasRelevanceAnnotation": {
                            "inDimension": "http://iso.org/25012/2008/dataquality/Relevance",
                            "hasBody": {
                                "nb": "asdasd"
                            }
                        },
                        "references": [
                            {
                                "referenceType": {
                                    "uri": "http://purl.org/dc/terms/hasVersion",
                                    "code": "hasVersion",
                                    "prefLabel": {
                                        "en": "Has version",
                                        "nn": "Har versjon",
                                        "nb": "Har versjon"
                                    }
                                },
                                "source": {
                                    "uri": "http://brreg.no/catalogs/910244132/datasets/c32b7a4f-655f-45f6-88f6-d01f05d0f7c2"
                                }
                            }
                        ],
                        "provenance": {
                            "uri": "http://data.brreg.no/datakatalog/provinens/nasjonal",
                            "code": "NASJONAL",
                            "prefLabel": {
                                "en": "Authoritativ source",
                                "nb": "Autoritativ kilde",
                                "nn": "Autoritativ kilde"
                            }
                        },
                        "subject": [
                            {
                                "uri": "https://fellesdatakatalog.brreg.no/api/concepts/67f7066a-870b-4ddf-8781-31bca01d1228",
                                "identifier": "http://data.brreg.no/begrep/28164",
                                "prefLabel": {
                                    "nb": "saksbehandler"
                                },
                                "definition": {
                                    "nb": "person i organet som er ansvarlig for oppfølging og behandling av ett eller flere dokumenter i en sak"
                                }
                            },
                            {
                                "uri": "https://fellesdatakatalog.brreg.no/api/concepts/f0d1288a-bc36-4477-ac5c-4e5a4a4cff96",
                                "identifier": "http://data.brreg.no/begrep/43443",
                                "prefLabel": {
                                    "nb": "saksøkt"
                                },
                                "definition": {
                                    "nb": "den som det blir reist sak mot, eller som en begjæring om tvangsfullbyrdelse er rettet mot"
                                }
                            }
                        ],
                        "conformsTo": [
                            {
                                "uri": "http://vg.no",
                                "prefLabel": {
                                    "nb": "asdasd"
                                },
                                "extraType": "http://purl.org/dc/terms/Standard"
                            }
                        ],
                        "informationModel": [
                            {
                                "uri": "http://dagbladet.no",
                                "prefLabel": {
                                    "nb": "mr"
                                },
                                "extraType": "http://purl.org/dc/terms/Standard"
                            }
                        ],
                        "type": "Taksonomi",
                        "catalog": {
                            "id": "910244132",
                            "uri": "http://dataset-catalogue:8080/catalogs/910244132",
                            "title": {
                                "nb": "Datakatalog for RAMSUND OG ROGNAN REVISJON"
                            },
                            "publisher": {
                                "type": "no.dcat.datastore.domain.dcat.Publisher",
                                "valid": "false",
                                "uri": "http://data.brreg.no/enhetsregisteret/enhet/910244132",
                                "id": "910244132",
                                "name": "RAMSUND OG ROGNAN REVISJON",
                                "orgPath": "/ANNET/910244132"
                            }
                        }
                    }
                },
                {
                    "_index": "datasets",
                    "_type": "document",
                    "_id": "a8a16564-7b2f-4fb3-9520-2b53516b06a4",
                    "_score": 1.2,
                    "_source": {
                        "expandedLosTema": [
                            "helse og omsorg",
                            "helse og omsorg",
                            "health and care",
                            "helsetenester",
                            "helsetjenester",
                            "health services",
                            "hjelpemiddel",
                            "hjelpemidler",
                            "disability aids",
                            "omsorgstenester",
                            "omsorgstjenester",
                            "care services",
                            "folkehelse",
                            "folkehelse",
                            "public health",
                            "rus og avhengigheit",
                            "rus og avhengighet",
                            "addiction",
                            "pasientrettar",
                            "pasientrettigheter",
                            "patient rights",
                            "svangerskap",
                            "svangerskap",
                            "pregnancy",
                            "avlasting og støtte",
                            "avlastning og støtte",
                            "care relief and support",
                            "akutt hjelp",
                            "akutt hjelp",
                            "emergency help",
                            "helsestasjon",
                            "helsestasjon",
                            "health clinic",
                            "psykisk helse",
                            "psykisk helse",
                            "mental health care",
                            "tryggleik i heimen",
                            "trygghet i hjemmet",
                            "safety at home",
                            "helsesjukepleiar",
                            "helsesykepleier",
                            "health nurse",
                            "helsestasjon for ungdom",
                            "helsestasjon for ungdom",
                            "health station for youth",
                            "fysioterapi",
                            "fysioterapi",
                            "physiotherapy",
                            "svangerskapsomsorg",
                            "svangerskapsomsorg",
                            "prenatal care",
                            "sjukehus",
                            "sykehus",
                            "hospital",
                            "europeisk helsetrygdkort",
                            "europeisk helsetrygdkort",
                            "european health insurance",
                            "tannhelseteneste",
                            "tannhelsetjeneste",
                            "dental health service",
                            "ergoterapi",
                            "ergoterapi",
                            "ergonomics",
                            "sjukeheim",
                            "sykehjem",
                            "nursing home",
                            "fengselshelseteneste",
                            "fengselshelsetjeneste",
                            "prison health service",
                            "sjuketransport",
                            "syketransport",
                            "patient transport",
                            "vaksine",
                            "vaksine",
                            "vaccination",
                            "heimesjukepleie",
                            "hjemmesykepleie",
                            "home nurse",
                            "langvarige helsetenester",
                            "langvarige helsetjenester",
                            "long term health services",
                            "kiropraktikk",
                            "kiropraktikk",
                            "chiropractic services",
                            "friskliv og meistring",
                            "friskliv og mestring",
                            "healthy life and coping",
                            "frikort for helsetenester",
                            "frikort for helsetjenester",
                            "fee exemption card for health services",
                            "behandlingsreise",
                            "behandlingsreise",
                            "journey required to receive medical treatment",
                            "lækjemiddel",
                            "legemiddel",
                            "medicines",
                            "legehjelp",
                            "legehjelp",
                            "medical aid",
                            "skulehelseteneste",
                            "skolehelsetjeneste",
                            "school health service",
                            "alternativ behandling",
                            "alternativ behandling",
                            "alternative treatment",
                            "rørslehjelpemiddel",
                            "bevegelseshjelpemidler",
                            "mobility aid",
                            "høyrselshjelpemiddel",
                            "hørselshjelpemidler",
                            "hearing aid",
                            "synshjelpemiddel",
                            "synshjelpemidler",
                            "visual aid",
                            "kommunikasjon og kognisjon",
                            "kommunikasjon og kognisjon",
                            "commnication and cognition",
                            "eigenbetaling",
                            "egenbetaling",
                            "user fees",
                            "matlevering",
                            "matlevering",
                            "meals on wheels",
                            "tilrettelagd transport",
                            "tilrettelagt transport",
                            "transport services for disabled persons",
                            "heimesjukepleie",
                            "hjemmesykepleie",
                            "home nurse",
                            "bufellesskap",
                            "bofellesskap",
                            "shared housing",
                            "omsorgsbustad",
                            "omsorgsbolig",
                            "sheltererd housing",
                            "heimehjelp",
                            "hjemmehjelp",
                            "home help",
                            "pasient- og brukarombod",
                            "pasient- og brukerombud",
                            "ombudsman for patients",
                            "dagtilbod",
                            "dagtilbud",
                            "daytime activities",
                            "omsorgsstønad",
                            "omsorgsstønad",
                            "carer allowance",
                            "blodgjeving",
                            "blodgiving",
                            "blood donation",
                            "bioteknologi",
                            "bioteknologi",
                            "biotechnology",
                            "skadedyr",
                            "skadedyr",
                            "pests and vermin",
                            "innemiljø",
                            "innemiljø",
                            "indoor environment",
                            "fysisk aktivitet",
                            "fysisk aktivitet",
                            "physical exercise",
                            "ernæring",
                            "ernæring",
                            "nutrition",
                            "allergi",
                            "allergi",
                            "allergies",
                            "strålevern",
                            "strålevern",
                            "radiation",
                            "organdonasjon",
                            "organdonasjon",
                            "organ donation",
                            "tobakk",
                            "tobakk",
                            "tobacco",
                            "radonmåling",
                            "radonmåling",
                            "radon measurement",
                            "livsstil",
                            "livsstil",
                            "lifestyle",
                            "støy",
                            "støy",
                            "noise",
                            "smittevern",
                            "smittevern",
                            "infection prevention and control",
                            "gift",
                            "gift",
                            "poisons",
                            "speleavhengigheit",
                            "spilleavhengighet",
                            "gambling addiction",
                            "doping",
                            "doping",
                            "doping",
                            "aktivitetar og livsmeistring for rusavhengige",
                            "aktiviteter og livsmestring for rusavhengige",
                            "activities and aid for adiction problems",
                            "hjelp ved rusavhengigheit",
                            "hjelp ved rusavhengighet",
                            "aid for drug adiction",
                            "pasientskadeerstatning",
                            "pasientskadeerstatning",
                            "patient compensation",
                            "pasient- og brukarombod",
                            "pasient- og brukerombud",
                            "ombudsman for patients",
                            "klage på helse- og omsorgstenester",
                            "klage på helse- og omsorgstjenester",
                            "complaint about medical care or health services",
                            "ufrivillig barnløyse",
                            "ufrivillig barnløshet",
                            "involuntary childlessness",
                            "abort",
                            "abort",
                            "abortion",
                            "svangerskapsomsorg",
                            "svangerskapsomsorg",
                            "prenatal care",
                            "prevensjon",
                            "prevensjon",
                            "contraception",
                            "tilrettelagd arbeidstilbod",
                            "tilrettelagt arbeidstilbud",
                            "assisted job opportunities",
                            "personleg assistent",
                            "personlig assistent",
                            "personal assistant",
                            "tolketeneste",
                            "tolketjeneste",
                            "interpreter services",
                            "rehabilitering",
                            "rehabilitering",
                            "rehabilitation",
                            "støttekontakt",
                            "støttekontakt",
                            "support person",
                            "korttidsopphald",
                            "korttidsopphold",
                            "temporary stay",
                            "tilrettelagd fritid",
                            "tilrettelagt fritid",
                            "leisure activities for disabled persons",
                            "rettleiing og kurs",
                            "rådgivning og kurs",
                            "consultation and courses",
                            "følgjebevis",
                            "ledsagerbevis",
                            "care assistant certificate",
                            "støtte til familiar",
                            "støtte til familier",
                            "family support",
                            "omsorgsavlasting",
                            "omsorgsavlastning",
                            "care relief",
                            "omsorgsstønad",
                            "omsorgsstønad",
                            "carer allowance",
                            "krisesenter",
                            "krisesenter",
                            "shelter",
                            "legevakt",
                            "legevakt",
                            "accident and emergency unit",
                            "livskriser",
                            "livskriser",
                            "life crises",
                            "hjelp ved overgrep",
                            "hjelp ved overgrep",
                            "help-in-event-of-assault",
                            "ernæring",
                            "ernæring",
                            "nutrition",
                            "matvarer",
                            "mat",
                            "e-stoffer",
                            "grønn resept",
                            "e-stoff",
                            "tilsetningsstoffer",
                            "kosthald",
                            "grøn resept",
                            "næringsmiddel",
                            "kosthold",
                            "tilsettingsstoffer",
                            "tilsetjingsstoff",
                            "næringsmidler",
                            "folkehelse",
                            "folkehelse",
                            "public health",
                            "helse og omsorg",
                            "helse og omsorg",
                            "health and care",
                            "matlevering",
                            "matlevering",
                            "meals on wheels",
                            "matombringing",
                            "matombringning",
                            "omsorgstenester",
                            "omsorgstjenester",
                            "care services",
                            "helse og omsorg",
                            "helse og omsorg",
                            "health and care"
                        ],
                        "losTheme": [
                            {
                                "children": [
                                    "https://psi.norge.no/los/tema/helsetjenester",
                                    "https://psi.norge.no/los/tema/hjelpemidler",
                                    "https://psi.norge.no/los/tema/omsorgstjenester",
                                    "https://psi.norge.no/los/tema/folkehelse",
                                    "https://psi.norge.no/los/tema/rus-og-avhengighet",
                                    "https://psi.norge.no/los/tema/pasientrettigheter",
                                    "https://psi.norge.no/los/tema/svangerskap",
                                    "https://psi.norge.no/los/tema/avlastning-og-stotte",
                                    "https://psi.norge.no/los/tema/akutt-hjelp"
                                ],
                                "isTema": "true",
                                "losPaths": [
                                    "helse-og-omsorg"
                                ],
                                "name": {
                                    "nn": "Helse og omsorg",
                                    "nb": "Helse og omsorg",
                                    "en": "Health and care"
                                },
                                "uri": "https://psi.norge.no/los/tema/helse-og-omsorg",
                                "synonyms": []
                            },
                            {
                                "parents": [
                                    "https://psi.norge.no/los/tema/folkehelse"
                                ],
                                "isTema": "false",
                                "losPaths": [
                                    "helse-og-omsorg/folkehelse/ernaring"
                                ],
                                "name": {
                                    "nn": "Ernæring",
                                    "nb": "Ernæring",
                                    "en": "Nutrition"
                                },
                                "uri": "https://psi.norge.no/los/ord/ernaring",
                                "synonyms": [
                                    "Matvarer",
                                    "Mat",
                                    "E-stoffer",
                                    "Grønn resept",
                                    "E-stoff",
                                    "Tilsetningsstoffer",
                                    "Kosthald",
                                    "Grøn resept",
                                    "Næringsmiddel",
                                    "Kosthold",
                                    "Tilsettingsstoffer",
                                    "Tilsetjingsstoff",
                                    "Næringsmidler"
                                ]
                            },
                            {
                                "parents": [
                                    "https://psi.norge.no/los/tema/omsorgstjenester"
                                ],
                                "isTema": "false",
                                "losPaths": [
                                    "helse-og-omsorg/omsorgstjenester/matlevering"
                                ],
                                "name": {
                                    "nn": "Matlevering",
                                    "nb": "Matlevering",
                                    "en": "Meals on wheels"
                                },
                                "uri": "https://psi.norge.no/los/ord/matlevering",
                                "synonyms": [
                                    "Matombringing",
                                    "Matombringning"
                                ],
                                "relatedTerms": [
                                    "https://psi.norge.no/los/ord/trygghet-i-hjemmet"
                                ]
                            }
                        ],
                        "id": "a8a16564-7b2f-4fb3-9520-2b53516b06a4",
                        "uri": "http://brreg.no/catalogs/910244132/datasets/c6b9e443-12a4-4d29-854a-0f6eda682858",
                        "source": "B",
                        "harvest": {
                            "firstHarvested": "2019-08-22T12:26:11+0200",
                            "lastHarvested": "2020-03-17T01:02:53+0100",
                            "lastChanged": "2020-03-13T01:03:01+0100",
                            "changed": [
                                "2019-08-22T12:26:11+0200",
                                "2019-09-22T01:02:53+0200",
                                "2019-10-21T13:13:38+0200",
                                "2019-11-20T01:03:26+0100",
                                "2019-11-29T01:03:36+0100",
                                "2020-02-10T08:13:16+0100",
                                "2020-02-12T01:03:51+0100",
                                "2020-03-13T01:03:01+0100"
                            ]
                        },
                        "title": {
                            "nb": "Biff er beef"
                        },
                        "description": {
                            "nb": "oversikt over verdens beste biff"
                        },
                        "descriptionFormatted": {
                            "nb": "oversikt over verdens beste biff"
                        },
                        "objective": {
                            "nb": "Finne ut hvilken biff som er verdens beste"
                        },
                        "contactPoint": [
                            {
                                "email": "biff@steak.no",
                                "organizationUnit": "biff.no",
                                "hasURL": "http://steak.com",
                                "hasTelephone": "1337"
                            }
                        ],
                        "publisher": {
                            "type": "no.dcat.datastore.domain.dcat.Publisher",
                            "valid": "false",
                            "uri": "http://data.brreg.no/enhetsregisteret/enhet/910244132",
                            "id": "910244132",
                            "name": "RAMSUND OG ROGNAN REVISJON",
                            "orgPath": "/ANNET/910244132"
                        },
                        "landingPage": [
                            "https://en.wikipedia.org/wiki/Steak"
                        ],
                        "theme": [
                            {
                                "id": "https://psi.norge.no/los/tema/helse-og-omsorg"
                            },
                            {
                                "id": "https://psi.norge.no/los/ord/ernaring"
                            },
                            {
                                "id": "https://psi.norge.no/los/ord/matlevering"
                            }
                        ],
                        "distribution": [
                            {
                                "downloadURL": [],
                                "accessURL": [],
                                "license": {
                                    "uri": "http://creativecommons.org/publicdomain/zero/1.0/",
                                    "prefLabel": {
                                        "no": "Creative Commons Universal Fristatus-erklæring",
                                        "en": "Creative Commons Universal Public Domain Dedication"
                                    },
                                    "extraType": "http://purl.org/dc/terms/LicenseDocument"
                                },
                                "openLicense": "false",
                                "format": [
                                    "biff",
                                    "bouf",
                                    "beef"
                                ],
                                "type": "API"
                            }
                        ],
                        "sample": [
                            {
                                "description": {
                                    "nb": "biff"
                                },
                                "downloadURL": [],
                                "accessURL": [
                                    "http://www.eksempelbiffen.no"
                                ],
                                "openLicense": "false",
                                "format": [
                                    "bouff",
                                    "baouff",
                                    "boauff"
                                ]
                            }
                        ],
                        "accessRights": {
                            "uri": "http://publications.europa.eu/resource/authority/access-right/PUBLIC",
                            "code": "PUBLIC",
                            "prefLabel": {
                                "en": "Public",
                                "nb": "Offentlig",
                                "nn": "Offentlig"
                            }
                        },
                        "hasAccuracyAnnotation": {
                            "inDimension": "http://iso.org/25012/2008/dataquality/Accuracy",
                            "hasBody": {
                                "nb": "Veldig nøyaktig"
                            }
                        },
                        "hasCompletenessAnnotation": {
                            "inDimension": "http://iso.org/25012/2008/dataquality/Completeness",
                            "hasBody": {
                                "nb": "Veldig komplett"
                            }
                        },
                        "hasRelevanceAnnotation": {
                            "inDimension": "http://iso.org/25012/2008/dataquality/Relevance",
                            "hasBody": {
                                "nb": "Veldig relevant"
                            }
                        },
                        "references": [
                            {
                                "referenceType": {
                                    "uri": "http://purl.org/dc/terms/isPartOf",
                                    "code": "isPartOf",
                                    "prefLabel": {
                                        "en": "Is Part Of",
                                        "nn": "Er del av",
                                        "nb": "Er en del av"
                                    }
                                },
                                "source": {
                                    "uri": "http://brreg.no/catalogs/910244132/datasets/17ed5a7d-1a22-49f4-a1d6-25f7d90dfa6d"
                                }
                            }
                        ],
                        "provenance": {
                            "uri": "http://data.brreg.no/datakatalog/provinens/nasjonal",
                            "code": "NASJONAL",
                            "prefLabel": {
                                "en": "Authoritativ source",
                                "nb": "Autoritativ kilde",
                                "nn": "Autoritativ kilde"
                            }
                        },
                        "accrualPeriodicity": {
                            "uri": "http://publications.europa.eu/resource/authority/frequency",
                            "prefLabel": {
                                "en": "Frequency"
                            }
                        },
                        "subject": [
                            {
                                "uri": "https://fellesdatakatalog.brreg.no/api/concepts/11a9cb05-d60f-4ff4-9228-5d3fd483de93",
                                "identifier": "http://data.brreg.no/begrep/55561",
                                "prefLabel": {
                                    "nb": "transport"
                                },
                                "definition": {
                                    "nb": "overføring av panterett til ny rettighetshaver"
                                }
                            },
                            {
                                "uri": "https://fellesdatakatalog.brreg.no/api/concepts/b9066a91-0e03-4512-8b0b-88c5d64fabbd",
                                "identifier": "http://begrepskatalogen/begrep/8ea2df46-7662-11e6-a74e-7e18b36b3fd9",
                                "prefLabel": {
                                    "nb": "matpenger i forbindelse med overtid"
                                },
                                "definition": {
                                    "nb": "utgiftsgodtgjørelse for merkostnader til kost i forbindelse med overtid"
                                }
                            },
                            {
                                "uri": "https://fellesdatakatalog.brreg.no/api/concepts/81b49255-8168-451a-9d7c-3a38c27b872d",
                                "identifier": "http://begrepskatalogen/begrep/8ea2df49-7662-11e6-a74e-7e18b36b3fd9",
                                "prefLabel": {
                                    "nb": "overnatting"
                                },
                                "definition": {
                                    "nb": "den skattepliktige tilbringer natten borte fra hjemmet på grunn av arbeid, virksomhet eller annen inntektsgivende aktivitet"
                                }
                            }
                        ],
                        "type": "Testdata",
                        "catalog": {
                            "id": "910244132",
                            "uri": "http://dataset-catalogue:8080/catalogs/910244132",
                            "title": {
                                "nb": "Datakatalog for RAMSUND OG ROGNAN REVISJON"
                            },
                            "publisher": {
                                "type": "no.dcat.datastore.domain.dcat.Publisher",
                                "valid": "false",
                                "uri": "http://data.brreg.no/enhetsregisteret/enhet/910244132",
                                "id": "910244132",
                                "name": "RAMSUND OG ROGNAN REVISJON",
                                "orgPath": "/ANNET/910244132"
                            }
                        }
                    }
                }
            ]
        },
        "aggregations": {
            "los": {
                "doc_count_error_upper_bound": 1,
                "sum_other_doc_count": 329,
                "buckets": [
                    {
                        "key": "doping",
                        "doc_count": 2
                    },
                    {
                        "key": "tilrettelagd transport",
                        "doc_count": 2
                    },
                    {
                        "key": "tilrettelagt transport",
                        "doc_count": 2
                    },
                    {
                        "key": "traffic and transport",
                        "doc_count": 2
                    },
                    {
                        "key": "trafikk og transport",
                        "doc_count": 2
                    },
                    {
                        "key": "transport services for disabled persons",
                        "doc_count": 2
                    },
                    {
                        "key": "abort",
                        "doc_count": 1
                    },
                    {
                        "key": "abortion",
                        "doc_count": 1
                    },
                    {
                        "key": "accident and emergency unit",
                        "doc_count": 1
                    },
                    {
                        "key": "activities and aid for adiction problems",
                        "doc_count": 1
                    }
                ]
            },
            "orgPath": {
                "doc_count_error_upper_bound": 1,
                "sum_other_doc_count": 82,
                "buckets": [
                    {
                        "key": "/ANNET/910244132",
                        "doc_count": 12
                    },
                    {
                        "key": "/STAT/972417866/961181399",
                        "doc_count": 7
                    },
                    {
                        "key": "/ANNET/910258028",
                        "doc_count": 3
                    },
                    {
                        "key": "/STAT/872417842/970018131",
                        "doc_count": 3
                    },
                    {
                        "key": "/STAT/972417858/991825827",
                        "doc_count": 3
                    },
                    {
                        "key": "/KOMMUNE/964338531",
                        "doc_count": 2
                    },
                    {
                        "key": "/KOMMUNE/964968063",
                        "doc_count": 1
                    },
                    {
                        "key": "/PRIVAT/817244742",
                        "doc_count": 1
                    },
                    {
                        "key": "/PRIVAT/832554332",
                        "doc_count": 1
                    },
                    {
                        "key": "/PRIVAT/837886252",
                        "doc_count": 1
                    }
                ]
            },
            "accessRights": {
                "doc_count_error_upper_bound": 0,
                "sum_other_doc_count": 0,
                "buckets": [
                    {
                        "key": "PUBLIC",
                        "doc_count": 9
                    },
                    {
                        "key": "RESTRICTED",
                        "doc_count": 1
                    }
                ]
            },
            "isOpenAccess": {
                "doc_count_error_upper_bound": 0,
                "sum_other_doc_count": 0,
                "buckets": [
                    {
                        "key": 1,
                        "key_as_string": "true",
                        "doc_count": 5
                    },
                    {
                        "key": 0,
                        "key_as_string": "false",
                        "doc_count": 2
                    }
                ]
            }
        }
    }
}
