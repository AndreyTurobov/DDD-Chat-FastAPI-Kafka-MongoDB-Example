from fastapi import FastAPI


def create_app():
    return FastAPI(
        title="Simple FastAPI Kafka Chat",
        docs_url="/api/docs",
        description="A simple fastapi + kafka + DDD example",
        debug=True,
    )
