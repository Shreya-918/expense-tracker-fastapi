from fastapi import FastAPI

from .schemas.api import ApiResponse


from .routers.auth_api import auth_router
from .routers.users_api import user_router
from .routers.expense_api import expense_router

from .core.db import Base, engine

from .models import expense_model
from .models import user_model


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="expense tracker fast api"
)

print("everything works good")

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(expense_router)
