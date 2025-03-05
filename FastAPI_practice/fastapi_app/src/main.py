import uvicorn
from fastapi import FastAPI
from web import explorer, creature

app = FastAPI()

app.include_router(explorer.router)
app.include_router(creature.router)

print("this it the main file echoing")

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
