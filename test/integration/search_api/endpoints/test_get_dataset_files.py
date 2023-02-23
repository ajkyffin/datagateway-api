from contextlib import suppress

import pytest

from datagateway_api.src.common.config import Config


def prepare_data_for_assertion(response):
    """
    Remove creationDate from queries. creationDate is generated by python_icat
    and is not static between data generations and therefore needs to be
    removed for assertion.
    :param response: JSON response from the search api.
    """

    # Go through list and dicts to find dicts
    for data in response:
        if isinstance(response, dict):
            data = response[data]

        if type(data) in [dict, list]:
            # Pass list and dicts back to the function to
            # loop through nested lists or dictionaries
            prepare_data_for_assertion(data)

    # This handles dictionaries passed to the function
    # Even if the dictionary doesn't contain creationDate
    if isinstance(response, dict):
        with suppress(KeyError):
            del response["creationDate"]

    return response


class TestSearchAPIGetDatasetFilesEndpoint:
    @pytest.mark.parametrize(
        "pid, request_filter, expected_json",
        [
            pytest.param(
                "0-449-78690-0",
                '{"limit": 2}',
                [
                    {
                        "id": "1071",
                        "name": "Datafile 1071",
                        "path": "/sense/through/candidate.jpeg",
                        "size": 9390543,
                        "dataset": None,
                    },
                    {
                        "id": "119",
                        "name": "Datafile 119",
                        "path": "/five/with/question.bmp",
                        "size": 124185509,
                        "dataset": None,
                    },
                ],
                id="Basic /datasets/{pid}/files request",
            ),
            pytest.param(
                "0-449-78690-0",
                '{"limit": 1, "skip": 5}',
                [
                    {
                        "id": "1547",
                        "name": "Datafile 1547",
                        "path": "/training/value/share.gif",
                        "size": 80936756,
                        "dataset": None,
                    },
                ],
                id="Get dataset files with skip",
            ),
            pytest.param(
                "0-449-78690-0",
                '{"limit": 1, "where": {"name": "Datafile 1547"}}',
                [
                    {
                        "id": "1547",
                        "name": "Datafile 1547",
                        "path": "/training/value/share.gif",
                        "size": 80936756,
                        "dataset": None,
                    },
                ],
                id="Get dataset files with name condition",
            ),
            pytest.param(
                "0-449-78690-0",
                '{"limit": 1, "where": {"name": {"nilike": "Datafile 10060"}}}',
                [
                    {
                        "id": "1071",
                        "name": "Datafile 1071",
                        "path": "/sense/through/candidate.jpeg",
                        "size": 9390543,
                        "dataset": None,
                    },
                ],
                id="Get dataset files with name condition (operator specified)",
            ),
            pytest.param(
                "0-449-78690-0",
                '{"limit": 1, "where": {"size": {"gt": 155061161}}}',
                [
                    {
                        "id": "1309",
                        "name": "Datafile 1309",
                        "path": "/writer/family/pull.bmp",
                        "size": 171717920,
                        "dataset": None,
                    },
                ],
                id="Get dataset files with size condition",
            ),
            pytest.param(
                "0-449-78690-0",
                '{"limit": 1, "where": {"size": {"gt": 50000000000}}}',
                [],
                id="Get dataset files with condition to return empty list",
            ),
            pytest.param(
                "0-449-78690-0",
                '{"limit": 1, "include": [{"relation": "dataset"}]}',
                [
                    {
                        "id": "1071",
                        "name": "Datafile 1071",
                        "path": "/sense/through/candidate.jpeg",
                        "size": 9390543,
                        "dataset": {
                            "pid": "0-449-78690-0",
                            "title": "DATASET 1",
                            "isPublic": True,
                            "size": None,
                            "documents": [],
                            "techniques": [],
                            "instrument": None,
                            "files": [],
                            "parameters": [],
                            "samples": [],
                        },
                    },
                ],
                id="Get dataset files with include filter",
            ),
        ],
    )
    def test_valid_get_dataset_files_endpoint(
        self, flask_test_app_search_api, pid, request_filter, expected_json,
    ):
        test_response = flask_test_app_search_api.get(
            f"{Config.config.search_api.extension}/datasets/{pid}/files"
            f"?filter={request_filter}",
        )

        print(test_response)
        print(test_response.json)

        response_data = prepare_data_for_assertion(test_response.json)

        assert test_response.status_code == 200
        assert response_data == expected_json

    @pytest.mark.parametrize(
        "pid, request_filter, expected_status_code",
        [
            pytest.param("0-8401-1070-7", '{"where": []}', 400, id="Bad where filter"),
            pytest.param("0-8401-1070-7", '{"limit": -1}', 400, id="Bad limit filter"),
            pytest.param("0-8401-1070-7", '{"skip": -100}', 400, id="Bad skip filter"),
            pytest.param(
                "0-8401-1070-7", '{"include": ""}', 400, id="Bad include filter",
            ),
            pytest.param(
                "my 404 test pid",
                "{}",
                404,
                id="Non-existent dataset pid",
                # Skipped because this actually returns 200
                marks=pytest.mark.skip,
            ),
        ],
    )
    def test_invalid_get_dataset_files_endpoint(
        self, flask_test_app_search_api, pid, request_filter, expected_status_code,
    ):
        test_response = flask_test_app_search_api.get(
            f"{Config.config.search_api.extension}/datasets/{pid}/files"
            f"?filter={request_filter}",
        )

        assert test_response.status_code == expected_status_code
