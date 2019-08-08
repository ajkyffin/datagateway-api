from flask import request
from flask_restful import Resource

from common.database_helpers import get_row_by_id, delete_row_by_id, update_row_from_id, get_rows_by_filter, \
    get_filtered_row_count, get_first_filtered_row, create_row_from_json, patch_entities
from common.helpers import requires_session_id, queries_records, get_filters_from_query_string
from common.models.db_models import INVESTIGATIONINSTRUMENT
from src.swagger.swagger_generator import swagger_gen


@swagger_gen.resource_wrapper()
class InvestigationInstruments(Resource):
    @requires_session_id
    @queries_records
    def get(self):
        return get_rows_by_filter(INVESTIGATIONINSTRUMENT, get_filters_from_query_string()), 200

    @requires_session_id
    @queries_records
    def post(self):
        create_row_from_json(INVESTIGATIONINSTRUMENT, request.json)
        return get_row_by_id(INVESTIGATIONINSTRUMENT, request.json["id"].to_dict()), 200

    @requires_session_id
    @queries_records
    def patch(self):
        return list(map(lambda x: x.to_dict(), patch_entities(INVESTIGATIONINSTRUMENT, request.json))), 200


class InvestigationInstrumentsWithID(Resource):
    @requires_session_id
    @queries_records
    def get(self, id):
        return get_row_by_id(INVESTIGATIONINSTRUMENT, id).to_dict(), 200

    @requires_session_id
    @queries_records
    def delete(self, id):
        delete_row_by_id(INVESTIGATIONINSTRUMENT, id)
        return "", 204

    @requires_session_id
    @queries_records
    def patch(self, id):
        update_row_from_id(INVESTIGATIONINSTRUMENT, id, str(request.json))
        return get_row_by_id(INVESTIGATIONINSTRUMENT, id).to_dict(), 200


class InvestigationInstrumentsCount(Resource):
    @requires_session_id
    @queries_records
    def get(self):
        filters = get_filters_from_query_string()
        return get_filtered_row_count(INVESTIGATIONINSTRUMENT, filters), 200


class InvestigationInstrumentsFindOne(Resource):
    @requires_session_id
    @queries_records
    def get(self):
        filters = get_filters_from_query_string()
        return get_first_filtered_row(INVESTIGATIONINSTRUMENT, filters), 200
