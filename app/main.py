from fastapi import FastAPI

from .api.routes import base_router as Router
from .config import Base, engine
from .config import API_PREFIX, DEBUG, PROJECT_NAME, VERSION

Base.metadata.create_all(bind=engine)

app = FastAPI()

app = FastAPI(title=PROJECT_NAME, debug=DEBUG, version=VERSION)
app.include_router(Router, prefix=API_PREFIX)
