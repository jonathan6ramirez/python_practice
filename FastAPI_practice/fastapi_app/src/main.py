import uvicorn
from fastapi import FastAPI
from web import explorer, creature, user

# INFO: This is how you cutomize the auto generated FastAPI
# documentation
# app = FastAPI(
#     title="Related Blog Articles",
#     description="This API was built with FastAPI and exists to find related blog articles given the ID of blog article.",
#     version="1.0.0",
#     servers=[
#         {
#             "url": "http://localhost:8000",
#             "description": "Development Server"
#         },
#         {
#             "url": "https://mock.pstmn.io",
#             "description": "Mock Server",
#         }
#     ],
# )

app = FastAPI(
    title="Creatures and Explorers database.",
    description="This is a database for creatures and the explorers looking for them.",
    version="1.0.0",
)
app.include_router(explorer.router)
app.include_router(creature.router)
app.include_router(user.router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
