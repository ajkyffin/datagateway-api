import pytest

from datagateway_api.src.common.config import Config


class TestDBCreateData:
    investigation_name_prefix = "DB Test Data for API Testing, Data Creation"

    @pytest.mark.usefixtures("remove_test_created_investigation_data")
    def test_valid_create_data(self, flask_test_app_db, valid_db_credentials_header):
        create_investigations_json = [
            {
                "name": f"{self.investigation_name_prefix} {i}",
                "title": "Test data for the Python DB Backend on DataGateway API",
                "summary": "DB Test data for DataGateway API testing",
                "releaseDate": "2020-03-03 08:00:08",
                "startDate": "2020-02-02 09:00:09",
                "endDate": "2020-02-03 10:00:10",
                "visitId": "Data Creation Visit DB",
                "doi": "DataGateway API DB Test DOI",
                "facilityID": 1,
                "typeID": 1,
            }
            for i in range(2)
        ]

        test_response = flask_test_app_db.post(
            f"{Config.config.datagateway_api.extension}/investigations",
            headers=valid_db_credentials_header,
            json=create_investigations_json,
        )

        response_json = test_response.json

        for investigation_request in response_json:
            investigation_request.pop("createId")
            investigation_request.pop("createTime")
            investigation_request.pop("id")
            investigation_request.pop("modId")
            investigation_request.pop("modTime")
            investigation_request["endDate"] = investigation_request["endDate"][:-6]
            investigation_request["releaseDate"] = investigation_request["releaseDate"][
                :-6
            ]
            investigation_request["startDate"] = investigation_request["startDate"][:-6]

        assert create_investigations_json == response_json

    @pytest.mark.usefixtures("remove_test_created_investigation_data")
    def test_valid_boundary_create_data(
        self, flask_test_app_db, valid_db_credentials_header,
    ):
        """Create a single investigation, as opposed to multiple"""

        create_investigation_json = {
            "name": f"{self.investigation_name_prefix} 0",
            "title": "Test data for the Python ICAT Backend on the API",
            "summary": "Test data for DataGateway API testing",
            "releaseDate": "2020-03-03 08:00:08",
            "startDate": "2020-02-02 09:00:09",
            "endDate": "2020-02-03 10:00:10",
            "visitId": "Data Creation Visit",
            "doi": "DataGateway API Test DOI",
            "facilityID": 1,
            "typeID": 1,
        }

        test_response = flask_test_app_db.post(
            f"{Config.config.datagateway_api.extension}/investigations",
            headers=valid_db_credentials_header,
            json=create_investigation_json,
        )

        response_json = test_response.json

        response_json.pop("createId")
        response_json.pop("createTime")
        response_json.pop("id")
        response_json.pop("modId")
        response_json.pop("modTime")
        response_json["endDate"] = response_json["endDate"][:-6]
        response_json["releaseDate"] = response_json["releaseDate"][:-6]
        response_json["startDate"] = response_json["startDate"][:-6]

        assert create_investigation_json == response_json

    def test_invalid_create_data(
        self, flask_test_app_db, valid_db_credentials_header,
    ):
        """An investigation requires a minimum of: name, visitId, facility, type"""

        invalid_request_body = {
            "title": "Test Title for DataGateway API Backend testing",
        }

        test_response = flask_test_app_db.post(
            f"{Config.config.datagateway_api.extension}/investigations",
            headers=valid_db_credentials_header,
            json=invalid_request_body,
        )

        assert test_response.status_code == 400
