import logging

from flask_restful import Resource

from datagateway_api.src.common.helpers import get_filters_from_query_string
from datagateway_api.src.search_api.helpers import (
    get_count,
    get_files,
    get_files_count,
    get_search,
    get_with_pid,
    search_api_error_handling,
)

log = logging.getLogger()


def get_search_endpoint(entity_name):
    """
    Given an entity name, generate a flask_restful `Resource` class. In
    `create_api_endpoints()`, these generated classes are registered with the API e.g.
    `api.add_resource(get_search_endpoint("Dataset"), "/datasets")`

    :param entity_name: Name of the entity
    :type entity_name: :class:`str`
    :return: Generated endpoint class
    """

    class Endpoint(Resource):
        @search_api_error_handling
        def get(self):
            filters = get_filters_from_query_string("search_api", entity_name)
            log.debug("Filters: %s", filters)
            return get_search(entity_name, filters), 200

        # TODO - Add `get.__doc__`

    Endpoint.__name__ = entity_name
    return Endpoint


def get_single_endpoint(entity_name):
    """
    Given an entity name, generate a flask_restful `Resource` class. In
    `create_api_endpoints()`, these generated classes are registered with the API e.g.
    `api.add_resource(get_single_endpoint("Dataset"), "/datasets/<string:pid>")`

    :param entity_name: Name of the entity
    :type entity_name: :class:`str`
    :return: Generated endpoint class
    """

    class EndpointWithID(Resource):
        @search_api_error_handling
        def get(self, pid):
            filters = get_filters_from_query_string("search_api", entity_name)
            log.debug("Filters: %s", filters)
            return get_with_pid(entity_name, pid, filters), 200

        # TODO - Add `get.__doc__`

    EndpointWithID.__name__ = entity_name
    return EndpointWithID


def get_number_count_endpoint(entity_name):
    """
    Given an entity name, generate a flask_restful `Resource` class. In
    `create_api_endpoints()`, these generated classes are registered with the API e.g.
    `api.add_resource(get_number_count_endpoint("Dataset"), "/datasets/count")`

    :param entity_name: Name of the entity
    :type entity_name: :class:`str`
    :return: Generated endpoint class
    """

    class CountEndpoint(Resource):
        @search_api_error_handling
        def get(self):
            # Only WHERE included on count endpoints
            filters = get_filters_from_query_string("search_api", entity_name)
            log.debug("Filters: %s", filters)
            return get_count(entity_name, filters), 200

        # TODO - Add `get.__doc__`

    CountEndpoint.__name__ = entity_name
    return CountEndpoint


def get_files_endpoint(entity_name):
    """
    Given an entity name, generate a flask_restful `Resource` class. In
    `create_api_endpoints()`, these generated classes are registered with the API e.g.
    `api.add_resource(get_files_endpoint("Dataset"), "/datasets/<string:pid>/files")`

    :param entity_name: Name of the entity
    :type entity_name: :class:`str`
    :return: Generated endpoint class
    """

    class FilesEndpoint(Resource):
        @search_api_error_handling
        def get(self, pid):
            filters = get_filters_from_query_string("search_api", entity_name)
            log.debug("Filters: %s", filters)
            return get_files(entity_name, pid, filters), 200

        # TODO - Add `get.__doc__`

    FilesEndpoint.__name__ = entity_name
    return FilesEndpoint


def get_number_count_files_endpoint(entity_name):
    """
    Given an entity name, generate a flask_restful `Resource` class. In
    `create_api_endpoints()`, these generated classes are registered with the API e.g.
    `api.add_resource(get_number_count_files_endpoint("Dataset"),
    "/datasets<string:pid>/files/count")`

    :param entity_name: Name of the entity
    :type entity_name: :class:`str`
    :return: Generated endpoint class
    """

    class CountFilesEndpoint(Resource):
        @search_api_error_handling
        def get(self, pid):
            # Only WHERE included on count endpoints
            filters = get_filters_from_query_string("search_api", entity_name)
            log.debug("Filters: %s", filters)
            return get_files_count(entity_name, filters, pid)

        # TODO - Add `get.__doc__`

    CountFilesEndpoint.__name__ = entity_name
    return CountFilesEndpoint
