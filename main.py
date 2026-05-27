from fastapi import FastAPI

from router import router

app = FastAPI(title="Job Application Tracker")

app.include_router(router)


@app.get("/")
def root():
    return {"message": "Job Application Tracker API"}
