import logging
from blikon_sdk.v1.core.config import set_client_application_settings
from blikon_sdk.v1.models.sdk_setup_model import SDKSetupSettings
from blikon_sdk.v1.models.sdk_configuration_model import SDKConfiguration
from opencensus.ext.azure.log_exporter import AzureLogHandler


blikon_sdk_setup_initiated = False


def setup_blikon_sdk(app, sdk_setup_settings: SDKSetupSettings):
    # Guardar nombre y modo de la aplicación cliente
    sdk_configuration = set_client_application_settings(sdk_setup_settings)

    # Inicializar la configuración del logging
    _setup_logging(sdk_configuration)

    # Indicar que el SDK ya se ha inicializado
    global blikon_sdk_setup_initiated
    if not blikon_sdk_setup_initiated:
        blikon_sdk_setup_initiated = True


def verify_blikon_sdk_initialized():
    if not blikon_sdk_setup_initiated:
        raise RuntimeError("Blikon SDK no inicializado")


def _setup_logging(sdk_configuration: SDKConfiguration):
    # Desactivar logs del servidor
    # logging.getLogger("uvicorn.error").disabled = True
    # logging.getLogger("uvicorn.access").disabled = True
    # logging.getLogger("fastapi").disabled = True
    # logging.getLogger("starlette").disabled = True

    # Obtener el logger
    logger = logging.getLogger(sdk_configuration.logger_name)
    # Deshabilitar la propagación hacia el logger raíz
    logger.propagate = False
    # Configurar el nivel del logger globalmente
    logger.setLevel(sdk_configuration.logging_level_console)
    # Crear el formato del logger
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S.%f"
    )

    # Configuración del logger para terminal
    if sdk_configuration.log_to_console:
        try:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(sdk_configuration.logging_level_console)
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)
        except Exception as e:
            logger.error(f"Error al inicializar el 'console_handler' del 'logger': {e}")

    # Configuración del logger para archivo
    if sdk_configuration.log_to_file:
        try:
            file_handler = logging.FileHandler("app.log")
            file_handler.setLevel(sdk_configuration.logging_level_file)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except Exception as e:
            logger.error(f"Error al inicializar el 'file_handler' del 'logger': {e}")

    # Configura el logging para Azure Application Insights
    if sdk_configuration.log_to_azure:
        try:
            azure_log_handler = AzureLogHandler(connection_string=sdk_configuration.azure_insights_instrumentation_key)
            azure_log_handler.setLevel(sdk_configuration.logging_level_azure_insights)
            azure_log_handler.setFormatter(formatter)
            logger.addHandler(azure_log_handler)
        except Exception as e:
            logger.error(f"Error al inicializar el 'azure_log_handler' del 'logger': {e}")

