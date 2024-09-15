#
#  Copyright MindBridge Analytics Inc. all rights reserved.
#
#  This material is confidential and may not be copied, distributed,
#  reversed engineered, decompiled or otherwise disseminated without
#  the prior written consent of MindBridge Analytics Inc.
#

from typing import Any, Dict
from pydantic import ConfigDict, field_validator, model_validator
from mindbridgeapi.common_validators import (
    _convert_userinfo_to_useritem,
    _warning_if_extra_fields,
)
from mindbridgeapi.generated_pydantic_model.model import (
    ApiAccountGroupingRead,
    ApiAccountGroupingUpdate,
)


class AccountGroupingItem(ApiAccountGroupingRead):
    model_config = ConfigDict(
        extra="allow",
        validate_assignment=True,
        validate_default=True,
        validate_return=True,
    )
    _a = model_validator(mode="after")(_warning_if_extra_fields)
    _b = field_validator("*")(_convert_userinfo_to_useritem)

    @property
    def update_json(self) -> Dict[str, Any]:
        in_class_dict = self.model_dump()
        ag_update = ApiAccountGroupingUpdate.model_validate(in_class_dict)
        return ag_update.model_dump(mode="json", by_alias=True, exclude_none=True)
