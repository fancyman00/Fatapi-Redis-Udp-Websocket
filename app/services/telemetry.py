from app.model.telemetry import IrTelemetry
from app.services.redis import get_redis


async def create_telemetry_service_ir(*args, **kwargs) -> IrTelemetry:
    service = IrTelemetry(*args, **kwargs)
    service.init(await get_redis())
    return service
