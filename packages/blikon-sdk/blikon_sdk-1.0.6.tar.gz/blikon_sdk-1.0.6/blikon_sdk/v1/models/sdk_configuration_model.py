from pydantic import BaseModel

# Constantes de configuración del SDK
SDK_NAME: str = "Blikon Python API SDK"
SDK_VERSION: str = "1.0.0"
JWT_ALGORITHM: str = "HS256"
HTTP_TIMEOUT_SEC: int = 10
HTTP_CONNECT_SEC: int = 5
LOGGER_NAME: str = "SDK_logger"


class BaseSDKConfiguration(BaseModel):
    # Propios del SDK
    sdk_name: str = SDK_NAME
    sdk_version: str = SDK_VERSION
    jwt_algorithm: str = JWT_ALGORITHM
    http_timeout_sec: int = HTTP_TIMEOUT_SEC
    http_connect_sec: int = HTTP_CONNECT_SEC
    logger_name: str = LOGGER_NAME


class SDKConfiguration(BaseSDKConfiguration):
    # Desde el client application
    client_application_name: str = ""
    client_application_description: str = ""
    client_application_version: str = ""
    client_application_mode: int = 0
    log_to_console: bool = False
    log_to_file: bool = False
    log_to_azure: bool = False
    logging_level_console: int = 20  # INFO, WARNING, ERROR, CRITICAL
    logging_level_file: int = 20  # INFO, WARNING, ERROR, CRITICAL
    logging_level_azure_insights: int = 20  # INFO, WARNING, ERROR, CRITICAL
    azure_insights_instrumentation_key: str = ""  # Para el logging de Azure Application Insights
