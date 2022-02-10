"""
Instancia de Celery a ser importada por modulos que contengan
funciones llamadas de forma remota.
"""
from celery import Celery


app = Celery(
    "task_queue",
    broker="redis://localhost",
    backend="redis://localhost",
    include=[
        "task_queue.scrap_tasks",
    ]
)

if __name__ == "__main__":
    app.start()
