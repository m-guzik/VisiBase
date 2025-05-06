from .forms import router as forms_router
from .websockets import router as websockets_router


routers = [
    forms_router,
    websockets_router,
]

