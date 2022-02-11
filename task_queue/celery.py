"""
Instancia de Celery a ser importada por modulos que contengan
funciones llamadas de forma remota.
"""
import os
from celery import Celery


app = Celery(
    "task_queue",
    broker=os.environ.get("CELERY_BROKER_URL"),
    backend=os.environ.get("CELERY_BACKEND_URL"),
    include=[
        "task_queue.scrap_tasks",
    ]
)

if __name__ == "__main__":
    app.start()
