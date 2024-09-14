import json
from dataclasses import dataclass
from typing import Dict, List, Optional, Union
from urllib.parse import urlencode

import click
import requests

from cobo_cli.data.constants import constants
from cobo_cli.data.enums import EnvironmentType
from cobo_cli.data.objects import UserTokenSigner


@dataclass(frozen=True)
class ApiError:
    errorCode: int
    errorMessage: str
    errorId: str


@dataclass
class ApiResponse:
    success: bool
    result: Optional[dict]
    exception: Optional[ApiError]


class PortalClient(object):
    def __init__(self, ctx: click.Context):
        # 所有接口默认为user token鉴权，如果需要其他方式，继承此类
        self.env = ctx.obj.env.value.upper()
        self.api_signer = UserTokenSigner(
            ctx.obj.env_manager.get_config("USER_ACCESS_TOKEN")
        )
        self.host = constants.get(f"API_HOST_{self.env}")

    def _request(self, method: str, path: str, params: dict):
        method = method.upper()

        headers = self.api_signer.get_headers()
        url = f"{self.host}{path}"

        if method == "GET":
            resp = requests.get(url, params=urlencode(params), headers=headers)
        elif method == "POST":
            resp = requests.post(url, json=params, headers=headers)
        elif method == "PUT":
            resp = requests.put(url, json=params, headers=headers)
        else:
            raise Exception("Not support http method")
        content = resp.content.decode()
        result = json.loads(content)
        success = result["success"]
        if success:
            return ApiResponse(True, result["result"], None)
        else:
            exception = ApiError(
                result["error_code"], result["error_message"], result["error_id"]
            )
            return ApiResponse(False, None, exception)

    def publish_app(self, manifest: Dict[str, Union[str, List[str]]]):
        manifest.pop("app_id", None)
        if self.env == EnvironmentType.PRODUCTION.value.upper():
            manifest.update({"app_id": manifest["dev_app_id"]})
        manifest = self._filter_empty_params(manifest)
        return self._request(
            method="POST", path="/web/v2/appstore/apps", params=manifest
        )

    def update_app(self, app_uuid: str, manifest: Dict[str, Union[str, List[str]]]):
        manifest.pop("app_id", None)
        manifest = self._filter_empty_params(manifest)
        return self._request(
            method="PUT", path=f"/web/v2/appstore/apps/{app_uuid}", params=manifest
        )

    def get_status(self, app_uuid: str):
        return self._request(
            method="GET", path=f"/web/v2/appstore/apps/{app_uuid}/status", params={}
        )

    def get_app(self, app_uuid: str):
        return self._request(
            method="GET", path=f"/web/v2/appstore/apps/{app_uuid}", params={"status_list": "INIT,ACTIVE,FROZEN"}
        )

    def _filter_empty_params(self, manifest):
        return {k: v for k, v in manifest.items() if v is not None}