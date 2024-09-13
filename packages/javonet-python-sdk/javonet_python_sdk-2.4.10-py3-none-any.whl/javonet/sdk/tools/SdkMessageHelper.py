import socket
import datetime
import platform
import importlib.metadata
from aiohttp import ClientSession

from javonet.sdk.tools.ActivationHelper import ActivationHelper

def __get_host_name():
    try:
        return socket.gethostname()
    except socket.error:
        return "Unknown Host"

def __get_package_version():
    try:
        return importlib.metadata.version("javonet-python-sdk")
    except importlib.metadata.PackageNotFoundError:
        return None

address = "https://dc.services.visualstudio.com/v2/track"
instrumentation_key = "2c751560-90c8-40e9-b5dd-534566514723"
calling_runtime_name = "Python"
javonet_version = __get_package_version()
node_name = __get_host_name()
os_name = platform.system()

class SdkMessageHelper:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SdkMessageHelper, cls).__new__(cls)
        return cls._instance

    async def send_message_to_app_insights(self, operation_name, message):
        try:
            formatted_datetime = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
            license_key = ActivationHelper.get_license_key()
            json_payload = {
                "name": "AppEvents",
                "time": formatted_datetime,
                "iKey": instrumentation_key,
                "tags": {
                    "ai.application.ver": javonet_version,
                    "ai.cloud.roleInstance": node_name,
                    "ai.operation.id": "0",
                    "ai.operation.parentId": "0",
                    "ai.operation.name": operation_name,
                    "ai.internal.sdkVersion": "javonet:2",
                    "ai.internal.nodeName": node_name
                },
                "data": {
                    "baseType": "EventData",
                    "baseData": {
                        "ver": 2,
                        "name": message,
                        "properties": {
                            "OperatingSystem": os_name,
                            "LicenseKey": license_key,
                            "CallingTechnology": calling_runtime_name
                        }
                    }
                }
            }

            async with ClientSession().post(address, json=json_payload) as response:
                return response.status
        except Exception:
            return -1



