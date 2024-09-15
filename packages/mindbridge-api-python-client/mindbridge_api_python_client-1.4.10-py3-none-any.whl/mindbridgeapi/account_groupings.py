#
#  Copyright MindBridge Analytics Inc. all rights reserved.
#
#  This material is confidential and may not be copied, distributed,
#  reversed engineered, decompiled or otherwise disseminated without
#  the prior written consent of MindBridge Analytics Inc.
#

from dataclasses import dataclass
from functools import cached_property
import logging
from typing import TYPE_CHECKING, Any, Dict, Generator, Optional, Union
from mindbridgeapi.account_grouping_item import AccountGroupingItem
from mindbridgeapi.async_results import AsyncResults
from mindbridgeapi.base_set import BaseSet
from mindbridgeapi.exceptions import ItemError, ItemNotFoundError
from mindbridgeapi.generated_pydantic_model.model import (
    ApiAsyncResult,
    ApiImportAccountGroupingParamsCreateOnly,
    ApiImportAccountGroupingParamsUpdate,
)
from mindbridgeapi.generated_pydantic_model.model import (
    Type7 as AccountGroupingFileType,
)
from mindbridgeapi.generated_pydantic_model.model import Status2 as AsyncResultStatus
from mindbridgeapi.generated_pydantic_model.model import Type1 as AsyncResultType

if TYPE_CHECKING:
    from os import PathLike
    from pathlib import Path


logger = logging.getLogger(__name__)


@dataclass
class AccountGroupings(BaseSet):
    def __post_init__(self) -> None:
        self.async_result_set = AsyncResults(server=self.server)

    @cached_property
    def base_url(self) -> str:
        return f"{self.server.base_url}/account-groupings"

    def get_by_id(self, id: str) -> AccountGroupingItem:
        url = f"{self.base_url}/{id}"
        resp_dict = super()._get_by_id(url=url)

        return AccountGroupingItem.model_validate(resp_dict)

    def get(
        self, json: Optional[Dict[str, Any]] = None
    ) -> Generator[AccountGroupingItem, None, None]:
        if json is None:
            json = {}

        url = f"{self.base_url}/query"
        for resp_dict in super()._get(url=url, json=json):
            yield AccountGroupingItem.model_validate(resp_dict)

    def export(self, input_item: AccountGroupingItem) -> ApiAsyncResult:
        if getattr(input_item, "id", None) is None:
            raise ItemNotFoundError

        url = f"{self.base_url}/{input_item.id}/export"
        resp_dict = super()._create(url=url)

        return ApiAsyncResult.model_validate(resp_dict)

    def wait_for_export(
        self, async_result: ApiAsyncResult, max_wait_minutes: int = 5
    ) -> None:
        """Wait for the async result for the data table export to complete

        Waits, at most the minutes specified, for the async result to be COMPLETE and
        raises and error if any error

        Args:
            async_result (AsyncResultItem): Async result to check
            max_wait_minutes (int): Maximum minutes to wait (default: `5`)

        Raises:
            ValueError: If not a ACCOUNT_GROUPING_EXPORT
        """
        if async_result.type != AsyncResultType.ACCOUNT_GROUPING_EXPORT:
            raise ItemError(f"{async_result.type=}")

        self.async_result_set._wait_for_async_result(
            async_result=async_result,
            max_wait_minutes=max_wait_minutes,
            init_interval_sec=5,
        )

    def download(
        self, async_result: ApiAsyncResult, output_file_path: "Path"
    ) -> "Path":
        # Get the current status
        resp_dict = super()._get_by_id(
            url=f"{self.server.base_url}/async-results/{async_result.id}"
        )
        async_result = ApiAsyncResult.model_validate(resp_dict)

        url = f"{self.server.base_url}/file-results/{async_result.entity_id}/export"

        if async_result.type != AsyncResultType.ACCOUNT_GROUPING_EXPORT:
            raise ItemError(f"{async_result.type=}")

        if async_result.status != AsyncResultStatus.COMPLETE:
            raise ItemError(f"{async_result.status=}")

        return super()._download(url=url, output_path=output_file_path)

    def upload(
        self,
        name: str,
        input_file: Union[str, "PathLike[Any]"],
        type: AccountGroupingFileType = AccountGroupingFileType.MINDBRIDGE_TEMPLATE,
    ) -> AccountGroupingItem:
        chunked_file = self.server.chunked_files.upload(input_file)

        url = f"{self.base_url}/import-from-chunked-file"
        ag_params = ApiImportAccountGroupingParamsCreateOnly(
            name=name, type=type, chunked_file_id=chunked_file.id
        )
        json = ag_params.model_dump(mode="json", by_alias=True, exclude_none=True)
        resp_dict = super()._create(url=url, json=json)

        return AccountGroupingItem.model_validate(resp_dict)

    def update(self, account_grouping: AccountGroupingItem) -> AccountGroupingItem:
        if getattr(account_grouping, "id", None) is None:
            raise ItemNotFoundError

        url = f"{self.base_url}/{account_grouping.id}"
        resp_dict = super()._update(url=url, json=account_grouping.update_json)

        return AccountGroupingItem.model_validate(resp_dict)

    def delete(self, account_grouping: AccountGroupingItem) -> None:
        if getattr(account_grouping, "id", None) is None:
            raise ItemNotFoundError

        url = f"{self.base_url}/{account_grouping.id}"
        super()._delete(url=url)

    def append(
        self,
        account_grouping: AccountGroupingItem,
        input_file: Union[str, "PathLike[Any]"],
    ) -> AccountGroupingItem:
        chunked_file = self.server.chunked_files.upload(input_file)

        url = f"{self.base_url}/{account_grouping.id}/append-from-chunked-file"
        ag_params = ApiImportAccountGroupingParamsUpdate(
            chunked_file_id=chunked_file.id
        )
        json = ag_params.model_dump(mode="json", by_alias=True, exclude_none=True)
        resp_dict = super()._create(url=url, json=json)

        return AccountGroupingItem.model_validate(resp_dict)
