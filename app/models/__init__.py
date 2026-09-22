from app.models.user import User  # noqa: F401 - registra el modelo en Base.metadata
from app.models.product import Product

__all__ = ["User","Product"]
