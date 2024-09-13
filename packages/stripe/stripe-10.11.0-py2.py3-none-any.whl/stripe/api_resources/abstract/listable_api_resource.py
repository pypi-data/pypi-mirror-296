# -*- coding: utf-8 -*-
# File generated from our OpenAPI spec
from typing_extensions import TYPE_CHECKING
from warnings import warn

warn(
    """
    The stripe.api_resources.listable_api_resource package is deprecated, please change your
    imports to import from stripe directly.
    From:
      from stripe.api_resources.listable_api_resource import ListableAPIResource
    To:
      from stripe import ListableAPIResource
    """,
    DeprecationWarning,
    stacklevel=2,
)
if not TYPE_CHECKING:
    from stripe._listable_api_resource import (  # noqa
        ListableAPIResource,
    )
