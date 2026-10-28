from fastapi import FastAPI
import uvicorn
from warehause_manager.database import engine, Base
from warehause_manager.models import Product
from warehause_manager.routers.products import router


app = FastAPI(
    title="Warehouse Api",
    description="Manager",
    version="0.1.0"
)

Base.metadata.create_all(engine)

app.include_router(router)


@app.get("/")
def root():
    return {"message": "OK"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
