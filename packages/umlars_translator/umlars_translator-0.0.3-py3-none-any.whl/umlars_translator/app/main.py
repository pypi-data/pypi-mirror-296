from typing import Optional
import os
import logging
from contextlib import asynccontextmanager

from kink import di, inject
import uvicorn
from fastapi import FastAPI, Depends
from fastapi.exceptions import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import ValidationError

from umlars_translator.app.adapters.repositories.uml_model_repository import UmlModelRepository
from umlars_translator.app.adapters.repositories.mongo_uml_model_repository import MongoDBUmlModelRepository
from umlars_translator.app.dtos.uml_model import UmlModel
from umlars_translator.app.dtos import input as source_models
from umlars_translator.app.adapters.message_brokers.rabbitmq_message_consumer import RabbitMQConsumer
from umlars_translator.app import config
from umlars_translator.app.exceptions import ServiceConnectionError, QueueUnavailableError
from umlars_translator.logger import add_file_handler
from umlars_translator.app.services.models_translator import translate_service


def create_app_logger():
    """
    This function provides consistent logger creation for the application.
    New logger for the application is created as a child of the main logger, 
    used in the core module.
    """
    logs_file = config.LOG_FILE
    app_logger = di[logging.Logger].getChild(config.APP_LOGGER_NAME)
    app_logger.setLevel(config.LOG_LEVEL)
    add_file_handler(app_logger, logs_file, config.LOG_LEVEL)
    return app_logger


di["app_logger"] = lambda _: create_app_logger()
di["translate_service"] = translate_service

@inject
def get_db_client(app_logger: logging.Logger) -> AsyncIOMotorClient:
    try:
        connection_str = config.DB_CONN_STR
        return AsyncIOMotorClient(connection_str)
    except Exception as e:
        app_logger.error(f"Failed to connect to the database: {e}")
        raise HTTPException(status_code=500, detail="Failed to connect to the database")        


di[AsyncIOMotorClient] = lambda _: get_db_client()


@inject
def get_uml_model_repository(db_client: AsyncIOMotorClient) -> UmlModelRepository:
    return MongoDBUmlModelRepository(db_client, config.DB_NAME, config.DB_COLLECTION_NAME)


di[UmlModelRepository] = lambda _: get_uml_model_repository()


async def start_consuming_messages() -> None:
    try:
        consumer = RabbitMQConsumer(config.MESSAGE_BROKER_QUEUE_UPLOADED_FILES_NAME, config.MESSAGE_BROKER_HOST)
        di[RabbitMQConsumer] = consumer
    except QueueUnavailableError as e:
        raise ServiceConnectionError("Failed to create a consumer for the message queue") from e
    return await consumer.start_consuming()


async def connect_services():
    try:
        repository_service_connector = di["repository_api_connector"]
        await repository_service_connector.authenticate(create_token_endpoint = config.REPOSITORY_SERVICE_CREATE_JWT_ENDPOINT, user={"username": config.REPOSITORY_SERVICE_USER, "password": config.REPOSITORY_SERVICE_PASSWORD})
    except Exception as e:
        raise ServiceConnectionError(f"Failed to connect to the service: {e}") from e


@inject
@asynccontextmanager
async def lifespan_event_handler(app: FastAPI, logger: logging.Logger):
    logger.info("Starting the application")
    if config.RUN_STANDALONE:
        logger.info("Running the application in standalone mode")
        yield
        return

    logger.info("Running the application in connected mode")
    try:
        try:
            await connect_services()
            await start_consuming_messages()
        except Exception as ex:
            error_message = f"Error occured during the application startup: {type(ex)} - {ex}"
            logger.error(error_message)
            raise ServiceConnectionError(error_message) from ex
        yield
    except ServiceConnectionError as ex:
        raise ServiceConnectionError("Error occured before the application startup") from ex


app = FastAPI(lifespan=lifespan_event_handler)


@app.get("/uml-models/{model_id}")
async def get_uml_model(model_id: str, model_repo: UmlModelRepository = Depends(lambda: di[UmlModelRepository]), app_logger: logging.Logger = Depends(lambda: di[logging.Logger])) -> UmlModel:
    try:
        model = await model_repo.get(model_id)
    except ValidationError as e:
        app_logger.error(f"Failed to validate the model from database: {e}")
        raise HTTPException(status_code=422, detail=f"Invalid model data. Error: {e}")
    if model is None:
        app_logger.error(f"Model with ID: {model_id} not found in the database")
        raise HTTPException(status_code=404, detail=f"Model with ID: {model_id} not found")
    return model


@app.post("/uml-models")
async def save_uml_model(uml_model: UmlModel, model_repo: UmlModelRepository = Depends(lambda: di[UmlModelRepository]), app_logger: logging.Logger = Depends(lambda: di[logging.Logger])):
    app_logger.info(f"Saving the model with ID: {uml_model.id}")
    await model_repo.save(uml_model)
    app_logger.info(f"Model with ID: {uml_model.id} saved to the database")
    return {"status": "success"}


@app.post("/translate")
async def translate_uml_model(uml_model: source_models.UmlModelDTO, model_repo: UmlModelRepository = Depends(lambda: di[UmlModelRepository]), translate_service=Depends(lambda: di["translate_service"]), app_logger: logging.Logger = Depends(lambda: di[logging.Logger])):
    translated_model = await translate_service(uml_model, app_logger)
    await model_repo.save(translated_model)
    return {"status": "success"}


@inject
def run_app(port: int = config.RUN_ON_PORT, host: str = config.TRANSLATION_HOST, context: str = config.CONTEXT, app_logger: Optional[logging.Logger] = None):
    app_logger.info(f"\nStarting the application on {host}:{port}")

    if context == 'DEV':
        return uvicorn.run("umlars_translator.app.main:app", host=host, port=port, reload=True)
    else:
        return uvicorn.run("umlars_translator.app.main:app", host=host, port=port)


if __name__ == "__main__":
    run_app()
