# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2021 CERN.
# Copyright (C) 2020-2021 Northwestern University.
#
# Invenio-RDM-Records is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Resources configuration."""

import marshmallow as ma
from flask_resources import HTTPJSONException, JSONSerializer, \
    ResponseHandler, create_error_handler
from invenio_drafts_resources.resources import RecordResourceConfig
from invenio_records_resources.resources.files import FileResourceConfig

from .serializers import UIJSONSerializer

#
# Response handlers
#
record_serializers = {
    "application/json": ResponseHandler(JSONSerializer()),
    "application/vnd.inveniordm.v1+json": ResponseHandler(UIJSONSerializer())
}


#
# Records and record versions
#
class RDMRecordResourceConfig(RecordResourceConfig):
    """Record resource configuration."""

    blueprint_name = "records"
    url_prefix = "/records"

    response_handlers = record_serializers


#
# Record files
#
class RDMRecordFilesResourceConfig(FileResourceConfig):
    """Bibliographic record files resource config."""

    allow_upload = False
    blueprint_name = "record_files"
    url_prefix = "/records/<pid_value>"


#
# Draft files
#
class RDMDraftFilesResourceConfig(FileResourceConfig):
    """Bibliographic record files resource config."""

    blueprint_name = "draft_files"
    url_prefix = "/records/<pid_value>/draft"


#
# Parent Record Links
#
record_links_error_handlers = RecordResourceConfig.error_handlers.copy()


record_links_error_handlers.update({
    LookupError: create_error_handler(
        HTTPJSONException(
            code=404,
            description="No secret link found with the given ID.",
        )
    ),
})


class RDMParentRecordLinksResourceConfig(RecordResourceConfig):
    """User records resource configuration."""

    blueprint_name = "record_access"

    url_prefix = "/records/<pid_value>/access"

    routes = {
        "list": "/links",
        "item": "/links/<link_id>",
    }

    links_config = {}

    request_view_args = {
        "pid_value": ma.fields.Str(),
        "link_id": ma.fields.Str()
    }

    response_handlers = {
        "application/json": ResponseHandler(JSONSerializer())
    }

    error_handlers = record_links_error_handlers


class RDMManagedPIDProviderResourceConfig(RecordResourceConfig):
    """PID provider resource configuration."""

    blueprint_name = "record_pid_provider"

    url_prefix = "/records/<pid_value>/draft/pids"

    routes = {
        "item": "/<pid_type>"
    }

    request_view_args = {
        "pid_type": ma.fields.Str(),
        "pid_value": ma.fields.Str(),
    }

    response_handlers = {
        "application/json": ResponseHandler(JSONSerializer())
    }


class PIDResolverResourceConfig(RecordResourceConfig):
    """PID provider resource configuration."""

    blueprint_name = "record_pids_resolver"

    url_prefix = "/pids/<pid_type>"

    routes = {
        "item-doi": "/<pid_prefix>/<pid_value>",
        "item": "/<pid_value>"
    }

    request_view_args = {
        "pid_prefix": ma.fields.Str(),
        "pid_type": ma.fields.Str(),
        "pid_value": ma.fields.Str(),
    }

    response_handlers = {
        "application/json": ResponseHandler(JSONSerializer())
    }
