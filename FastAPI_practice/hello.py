from fastapi import FastAPI, Header, Response, Body


app = FastAPI()


@app.get("/agent")
def agent(user_agent: str = Header()):
    return user_agent


@app.post("/hi")
def greet(who: str = Body(embed=True)):
    return f"Hello? {who}?"


@app.get("/happy")
def happy(status_code=200):
    return ":)"


@app.get("/header/{name}/{value}")
def header(name: str, value: str, response: Response):
    response.headers[name] = value
    return "normal body"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("hello:app", reload=True)
