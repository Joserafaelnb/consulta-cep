from fastapi import FastAPI

app = FastAPI(title="Consulta de CEP")


@app.get("/health")
def health():
    return {"status": "ok"}