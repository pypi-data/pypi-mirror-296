"""
Corva StreamX Semantic Attributes

Common names for different kinds of operations and data.
OpenTelemetry defines Semantic Conventions (sometimes called Semantic Attributes) that specify common names for different kinds of operations and data. The benefit of using Semantic Conventions is in following a common naming scheme that can be standardized across a codebase, libraries, and platforms.

@see https://opentelemetry.io/docs/concepts/semantic-conventions/
@see https://github.com/open-telemetry/opentelemetry-specification/blob/v1.26.0/specification/semantic-conventions.md
"""

CORVA_STREAMX_BOX_WRITER = "corva.streamx.box.writer"

CORVA_STREAMX_BOX_FETCHER = "corva.streamx.box.fetcher"

CORVA_STREAMX_BOX_FETCHER_CMD_START = "corva.streamx.box.fetcher.cmd.start"

CORVA_STREAMX_BOX_FETCHER_CMD_END = "corva.streamx.box.fetcher.cmd.end"

CORVA_STREAMX_BOX_FETCHER_DATA_START = "corva.streamx.box.fetcher.data.start"

CORVA_STREAMX_BOX_FETCHER_DATA_END = "corva.streamx.box.fetcher.data.end"

CORVA_STREAMX_BOX_SOURCES_ARIS_ODBC = "corva.streamx.box.sources.aris_odbc"

CORVA_STREAMX_BOX_SOURCES_COLDBORE = "corva.streamx.box.sources.coldbore"

CORVA_STREAMX_BOX_SOURCES_COLDBORE_V2 = "corva.streamx.box.sources.coldbore.v2"

CORVA_STREAMX_BOX_SOURCES_COLDBORE_VALVE = (
    "corva.streamx.box.sources.coldbore_valve"
)

CORVA_STREAMX_BOX_SOURCES_WITSML13 = "corva.streamx.box.sources.witsml13"

CORVA_STREAMX_BOX_SOURCES_WITSML14 = "corva.streamx.box.sources.witsml14"

CORVA_STREAMX_BOX_SOURCES_WITSML14_V2 = "corva.streamx.box.sources.witsml14.v2"

CORVA_STREAMX_CONSUMERS_ARIS_ODBC = "corva.streamx.consumers.aris_odbc"

CORVA_STREAMX_CONSUMERS_COLDBORE = "corva.streamx.consumers.coldbore"

CORVA_STREAMX_CONSUMERS_COLDBORE_V2 = "corva.streamx.consumers.coldbore.v2"

CORVA_STREAMX_CONSUMERS_COLDBORE_VALVE = (
    "corva.streamx.consumers.coldbore_valve"
)

CORVA_STREAMX_CONSUMERS_WITSML13 = "corva.streamx.consumers.witsml13"

CORVA_STREAMX_CONSUMERS_WITSML1311 = "corva.streamx.consumers.witsml1311"

CORVA_STREAMX_CONSUMERS_WITSML14 = "corva.streamx.consumers.witsml14"

CORVA_STREAMX_CONSUMERS_WITSML14_V2 = "corva.streamx.consumers.witsml14.v2"

CORVA_STREAMX_CONSUMERS_WITSML1411 = "corva.streamx.consumers.witsml1411"

CORVA_STREAMX_CONSUMERS_HANDLE_APP_STREAM_EVENTS = (
    "corva.streamx.consumers.handle_app_stream_events"
)

CORVA_STREAMX_CONSUMERS_RESEND_DATA_TO_PLATFORM = (
    "corva.streamx.consumers.resend_data_to_platform"
)

CORVA_STREAMX_CONSUMERS_RESEND_DATA_TO_PLATFORM_V2 = (
    "corva.streamx.consumers.resend_data_to_platform.v2"
)


"""
Corva StreamX Semantic Resource Attributes

A Resource is an immutable representation of the entity producing telemetry as Attributes. For example, a process producing telemetry that is running in a container on Kubernetes has a Pod name, it is in a namespace and possibly is part of a Deployment which also has a name. All three of these attributes can be included in the Resource. Note that there are certain "standard attributes" that have prescribed meanings.
The primary purpose of resources as a first-class concept in the SDK is decoupling of discovery of resource information from exporters. This allows for independent development and easy customization for users that need to integrate with closed source environments. The SDK MUST allow for creation of Resources and for associating them with telemetry.

@see https://opentelemetry.io/docs/concepts/resources/
@see https://github.com/open-telemetry/opentelemetry-specification/blob/v1.26.0/specification/resource/sdk.md
"""

CORVA_STREAMX_PROVIDER = "corva.streamx.provider"
"""
StreamX Provider Code - computer friendly company providing the relevant data
"""
CORVA_STREAMX_DATA_SOURCE_ID = "corva.streamx.data.source.id"
"""
StreamX DataSource ID
"""

CORVA_STREAMX_DATA_SOURCE_TYPE = "corva.streamx.data.source.type"
"""
StreamX DataSource Type

one of `data_source.Type`
(`resend`?!?, `witsml13`, `witsml14`, `witsml14-v2`, `coldbore`, `coldbore-valve`, `aris-odbc`, etc.)
"""

CORVA_STREAMX_DATA_SOURCE_WITSML_WELL_UID = (
    "corva.streamx.data.source.witsml.well.uid"
)
"""
StreamX DataSource WITSML Well UID
"""

CORVA_STREAMX_DATA_SOURCE_WITSML_WELLBORE_UID = (
    "corva.streamx.data.source.witsml.wellbore.uid"
)
"""
StreamX DataSource WITSML Wellbore UID
"""

CORVA_STREAMX_DATA_SOURCE_WITSML_LOG_UID = (
    "corva.streamx.data.source.witsml.log.uid"
)
"""
StreamX DataSource WITSML Log UID
"""

CORVA_STREAMX_DATA_SOURCE_WITSML_LOG_UIDS = (
    "corva.streamx.data.source.witsml.log.uids"
)
"""
StreamX DataSource WITSML Log UIDs Array / List
"""

CORVA_STREAMX_DATA_SOURCE_COLDBORE_JOB_ID = (
    "corva.streamx.data.source.coldbore.job.id"
)
"""
StreamX DataSource Coldbore Job ID
"""

CORVA_STREAMX_DATA_SOURCE_COLDBORE_VALVE_DATASET = (
    "corva.streamx.data.source.coldbore.valve.dataset"
)
"""
StreamX DataSource Coldbore Valve Dataset
"""

# TODO: Aris?
# CORVA_STREAMX_DATA_SOURCE_ARIS_?!? = "corva.streamx.data.source.aris.?!?"
# """
# StreamX DataSource Aris ?!?
# """

# TODO: Other Datasources?
# CORVA_STREAMX_DATA_SOURCE_?!?_?!? = "corva.streamx.data.source.?!?_?!?"
# """
# StreamX DataSource ?!? ?!?
# """

CORVA_STREAMX_DEPLOYMENT_ID = "corva.streamx.deployment.id"
"""
StreamX Deployment ID
"""

CORVA_STREAMX_DEPLOYMENT_TYPE = "corva.streamx.deployment.type"
"""
StreamX Deployment Type

one of `DeploymentType` (`consumer`, `data_source_reader`, `data_source_writer`, `handle_app_streams_consumer`)
"""

CORVA_STREAMX_DEPLOYMENT_GROUP = "corva.streamx.deployment.group"
"""
StreamX Deployment Group

one of (`consumers`, `box-software`)
"""
