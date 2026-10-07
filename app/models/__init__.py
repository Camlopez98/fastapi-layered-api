from app.models.user import User  # noqa: F401 - registra el modelo en Base.metadata
from app.models.product import Product  # noqa: F401 - registra el modelo en Base.metadata
from app.models.category import Category  # noqa: F401 - registra el modelo en Base.metadata

__all__ = ["User", "Product", "Category"]
