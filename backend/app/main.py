from fastapi import FastAPI


app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/item/{itemid}/{q}")
def read_item(itemid: int, q: str | None = None):
    return {"itemid": itemid, "q": q}
