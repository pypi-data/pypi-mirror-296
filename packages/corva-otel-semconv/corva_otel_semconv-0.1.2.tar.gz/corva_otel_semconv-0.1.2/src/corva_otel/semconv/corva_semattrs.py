"""
Corva Semantic Attributes

Common names for different kinds of operations and data.
OpenTelemetry defines Semantic Conventions (sometimes called Semantic Attributes) that specify common names for different kinds of operations and data. The benefit of using Semantic Conventions is in following a common naming scheme that can be standardized across a codebase, libraries, and platforms.

@see https://opentelemetry.io/docs/concepts/semantic-conventions/
@see https://github.com/open-telemetry/opentelemetry-specification/blob/v1.26.0/specification/semantic-conventions.md
"""

CORVA_ASSET_ID = "corva.asset.id"
"""
Corva Asset ID
"""

CORVA_ASSET_TYPE = "corva.asset.type"
"""
Corva Asset Type one of [`Rig`, `Well`, `Program`]
"""

CORVA_ASSET_NAME = "corva.asset.name"
"""
Corva Asset Name
@optional
"""

CORVA_COMPANY_ID = "corva.company.id"
"""
Corva Company ID in which context the application is invoked, or is owning the relevant resource
"""

CORVA_COMPANY_NAME = "corva.company.name"
"""
Corva Company Name in which context the application is invoked, or is owning the relevant resource
"""

CORVA_SOURCE_TYPE = "corva.source.type"
"""
Corva Source Type one of [`drilling`, `lithology`, `drillout`, `frac`, `pumpdown`, `wireline`]
@optional
"""

CORVA_LOG_TYPE = "corva.log.type"
"""
Corva Log Type one of [`time`, `depth`]
@optional
"""

CORVA_APP_STREAM_ID = "corva.app.stream.id"
"""
Corva Application Stream ID is a given graph of applications connections, handling given set of data as sa stream
"""

CORVA_APP_CONNECTION_ID = "corva.app.connection.id"
"""
Corva Application Connection ID is the ID of a given Application within a Stream
Not very useful, prefer providing `CORVA_APP_STREAM_ID`
@optional
"""

CORVA_APP_SCHEDULE_ID = "corva.app.schedule.id"
"""
Corva Application Schedule ID
@optional
"""

CORVA_APP_SCHEDULE_START = "corva.app.schedule.start"
"""
Corva Application Schedule Start
@optional
"""

CORVA_APP_SCHEDULE_END = "corva.app.schedule.end"
"""
Corva Application Schedule End
@optional
"""

CORVA_APP_SCHEDULER_TYPE = "corva.app.scheduler.type"
"""
Corva Application Scheduler Type
scheduler_type: 1  - this means that it is a time-based application that operates according to a schedule.
@optional
"""

CORVA_USER_ID = "corva.user.id"
"""
User ID
"""

CORVA_IMPERSONATOR_ID = "corva.impersonator.id"
"""
User Impersonator ID
@see CorvaSemanticAttributes.CORVA_USER_ID
"""

CORVA_SEGMENT = "corva.segment"
"""
Corva Segment
"""

"""
Corva Semantic Resource Attributes

A Resource is an immutable representation of the entity producing telemetry as Attributes. For example, a process producing telemetry that is running in a container on Kubernetes has a Pod name, it is in a namespace and possibly is part of a Deployment which also has a name. All three of these attributes can be included in the Resource. Note that there are certain "standard attributes" that have prescribed meanings.
The primary purpose of resources as a first-class concept in the SDK is decoupling of discovery of resource information from exporters. This allows for independent development and easy customization for users that need to integrate with closed source environments. The SDK MUST allow for creation of Resources and for associating them with telemetry.

@see https://opentelemetry.io/docs/concepts/resources/
@see https://github.com/open-telemetry/opentelemetry-specification/blob/v1.26.0/specification/resource/sdk.md
"""

CORVA_APP_ID = "corva.app.id"
"""
Corva Application ID
@deprecated The Application ID is not portable through environments, use the CorvaSemanticResourceAttributes.CORVA_APP_KEY instead
"""

CORVA_APP_KEY = "corva.app.key"
"""
Corva Application Key
"""

CORVA_APP_API_KEY = "corva.app.api_key"
"""
Corva Application API Key, please HASH key before sending
api_key = hashlib.sha256(str(copy_event.get('api_key')).encode('utf-8')).hexdigest()
@optional
"""

CORVA_APP_VERSION = "corva.app.version"
"""
Corva Application Version
"""

CORVA_APP_CATEGORY = "corva.app.category"
"""
Corva Application Category one of [`source_app`, `engineering_app`, `enrichment_app`, `stream_app`, `scheduling_app`]
@optional
"""

CORVA_APP_TYPE = "corva.app.type"
"""
Corva Application Type one of [`data_app`, `ui_app`]
@optional
"""

CORVA_APP_PROVIDER = "corva.app.provider"
"""
Corva Application Provider e.g. `corva`
@optional
"""

CORVA_INVOKE_APP_ID = "corva.invoke.app.id"
"""
Invoked Application ID
@optional
@see CorvaSemanticResourceAttributes.CORVA_APP_ID
"""

CORVA_INVOKE_APP_KEY = "corva.invoke.app.key"
"""
Invoked Application Key
@optional
@see CorvaSemanticResourceAttributes.CORVA_APP_KEY
"""

CORVA_INVOKE_APP_VERSION = "corva.invoke.app.version"
"""
Invoked Application Version
@optional
@see CorvaSemanticAttributes.CORVA_APP_VERSION
"""

CORVA_INVOKE_APP_TYPE = "corva.invoke.app.type"
"""
Invoked Application Type
@optional
@see CorvaSemanticAttributes.CORVA_APP_TYPE
"""

CORVA_APP_RUN_ID = "corva.app_run.id"
"""
AppRun ID
@optional
"""

# TODO: Supplement the list of attributes as we go
