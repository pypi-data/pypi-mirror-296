"""
Generated by qenerate plugin=pydantic_v1. DO NOT MODIFY MANUALLY!
"""
from collections.abc import Callable  # noqa: F401 # pylint: disable=W0611
from datetime import datetime  # noqa: F401 # pylint: disable=W0611
from enum import Enum  # noqa: F401 # pylint: disable=W0611
from typing import (  # noqa: F401 # pylint: disable=W0611
    Any,
    Optional,
    Union,
)

from pydantic import (  # noqa: F401 # pylint: disable=W0611
    BaseModel,
    Extra,
    Field,
    Json,
)

from reconcile.gql_definitions.fragments.vault_secret import VaultSecret


DEFINITION = """
fragment VaultSecret on VaultSecret_v1 {
    path
    field
    version
    format
}

query GlitchtipInstance {
  instances: glitchtip_instances_v1 {
    name
    description
    consoleUrl
    automationUserEmail {
      ...VaultSecret
    }
    automationToken {
      ...VaultSecret
    }
    readTimeout
    maxRetries
    mailDomain
    glitchtipJiraBridgeAlertUrl
    glitchtipJiraBridgeToken {
      ...VaultSecret
    }
  }
}
"""


class ConfiguredBaseModel(BaseModel):
    class Config:
        smart_union=True
        extra=Extra.forbid


class GlitchtipInstanceV1(ConfiguredBaseModel):
    name: str = Field(..., alias="name")
    description: str = Field(..., alias="description")
    console_url: str = Field(..., alias="consoleUrl")
    automation_user_email: VaultSecret = Field(..., alias="automationUserEmail")
    automation_token: VaultSecret = Field(..., alias="automationToken")
    read_timeout: Optional[int] = Field(..., alias="readTimeout")
    max_retries: Optional[int] = Field(..., alias="maxRetries")
    mail_domain: Optional[str] = Field(..., alias="mailDomain")
    glitchtip_jira_bridge_alert_url: Optional[str] = Field(..., alias="glitchtipJiraBridgeAlertUrl")
    glitchtip_jira_bridge_token: Optional[VaultSecret] = Field(..., alias="glitchtipJiraBridgeToken")


class GlitchtipInstanceQueryData(ConfiguredBaseModel):
    instances: list[GlitchtipInstanceV1] = Field(..., alias="instances")


def query(query_func: Callable, **kwargs: Any) -> GlitchtipInstanceQueryData:
    """
    This is a convenience function which queries and parses the data into
    concrete types. It should be compatible with most GQL clients.
    You do not have to use it to consume the generated data classes.
    Alternatively, you can also mime and alternate the behavior
    of this function in the caller.

    Parameters:
        query_func (Callable): Function which queries your GQL Server
        kwargs: optional arguments that will be passed to the query function

    Returns:
        GlitchtipInstanceQueryData: queried data parsed into generated classes
    """
    raw_data: dict[Any, Any] = query_func(DEFINITION, **kwargs)
    return GlitchtipInstanceQueryData(**raw_data)
