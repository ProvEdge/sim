from typing import Optional
from pydantic import BaseModel

class KubeappsResponse(BaseModel):
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

class CreateRelease(BaseModel):
    appRepositoryResourceName: str = "robot-helm-charts"
    appRepositoryResourceNamespace: str = "default"
    chartName: str
    releaseName: str
    version: str
    values: str = "namespace: instances\ncmStartName: jackal-start-2\ncmSupervisordName: jackal-supervisord-2\ndeploymentName: jackal-2\ndeploymentReplicas: 1\nhttpPort: 31006\nwebrtcPort: 31007\ntheiaPort: 31008\nrosbridgePort: 31009\nwebvizPort: 31010"

class UpdateRelease(BaseModel):
    appRepositoryResourceName: str
    appRepositoryResourceNamespace: str
    chartName: str
    version: Optional[str]
    values: Optional[str]