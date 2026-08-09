"""Worker configuration and module binding."""

from app.config.settings import settings
from app.workers import knowledge_ingestion_worker

functions = [knowledge_ingestion_worker.process_document]


class WorkerSettings:
    """ARQ worker settings."""

    redis_settings = settings.REDIS_DSN
    functions = functions
