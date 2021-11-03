from typing import Optional
from fastapi_camelcase import CamelModel

class KubeappsResponse(CamelModel):
    status_code: int
    data: dict

# {
#   "appRepositoryResourceName": "string",
#   "appRepositoryResourceNamespace": "string",
#   "chartName": "string",
#   "releaseName": "string",
#   "version": "string",
#   "values": "string"
# }

class CreateRelease(CamelModel):
    appRepositoryResourceName: str = "robot-helm-charts"
    appRepositoryResourceNamespace: str = "default"
    chartName: str
    releaseName: str
    version: str
    values: str = "namespace: instances\ncmStartName: jackal-start-2\ncmSupervisordName: jackal-supervisord-2\ndeploymentName: jackal-2\ndeploymentReplicas: 1\nhttpPort: 31006\nwebrtcPort: 31007\ntheiaPort: 31008\nrosbridgePort: 31009\nwebvizPort: 31010"

class UpdateRelease(CamelModel):
    appRepositoryResourceName: str
    appRepositoryResourceNamespace: str
    chartName: str
    version: Optional[str]
    values: Optional[str]