# Diagrama de arquitectura
![arquitectura](https://github.com/MarianoSaez/final/blob/main/img/Diagrama%20de%20infraestructura.png)

La arquitectura de la aplicacion consiste de un modelo cliente-servidor donde el cliente solicita realizar un **_scrapping_** a una o varias paginas (similares). Como realizar esta solicitud se detalla en el [uso basico de la aplicacion](https://github.com/MarianoSaez/final#readme).

Una vez recibida la solicitud (Request), el servidor asigna un conjunto de URL y parametros de busqueda a una tarea o **_task_** que sera llevada a cabo por una cola de tareas montada en [**Celery**](https://docs.celeryproject.org/en/stable/index.html) con un **_Message Broker_** en [**Redis**](https://redis.io/).

Cada **_task_** de **Celery** realizara un Request HTTP a la URL que le fue asignada y una vez obtenido el Response HTTP, se analizara el HTML recibido en busqueda de **_tags HTML_** que cumplan con los parametros de busqueda recibidos y los agregara a una lista.

![diagrama_de_concurrencia](https://github.com/MarianoSaez/final/blob/main/img/Diagrama%20de%20concurrencia.png)

Cuando cada **_task_** retorno al servidor su resultado, este construye una respuesta con todos los conjuntos de resultados obtenidos y la envia al cliente. Como tarea adicional, el servidor se encarga de llevar un **_log_** de las tareas realizadas, el cual se almacena en una instancia de [**MongoDB**](https://www.mongodb.com/), que dada la similitud de formatos en los que trabajan el servidor y el DBMS, fue la opcion elegida.

Por ultimo, cuando el cliente recibe la respuesta del servidor, este genera 3 archivos.

- Resultados de **_scrapping_** en CSV
- Resultados de **_scrapping_** en JSON
- Informacion de control y resultados de **_scrapping_** en JSON