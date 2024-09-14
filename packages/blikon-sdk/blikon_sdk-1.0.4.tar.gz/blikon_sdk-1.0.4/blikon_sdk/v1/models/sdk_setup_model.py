from pydantic import BaseModel


class SDKSetupSettings(BaseModel):
    client_application_name: str = ""
    client_application_description: str = ""
    client_application_version: str = ""
    client_application_mode: int = 0
    log_to_console: bool = False
    log_to_file: bool = False
    log_to_azure: bool = False
    logging_level_console: int = 20 # INFO, WARNING, ERROR, CRITICAL
    logging_level_file: int = 20 # INFO, WARNING, ERROR, CRITICAL
    logging_level_azure_insights: int = 20  # INFO, WARNING, ERROR, CRITICAL
    azure_insights_instrumentation_key: str = ""  # Para el logging de Azure Application Insights
