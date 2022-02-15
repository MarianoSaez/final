# Guia de instalacion de Simple Web Scrapper Server

A continuacion se detalla el proceso de instalacion de la infraestructura de servidor de la aplicacion Web Scrapper Server.

## Requerimientos
- docker version 20.10.12 (https://docs.docker.com/engine/install/)
- docker-compose version 1.29.2 (https://docs.docker.com/compose/install/)

## Descarga del paquete de software
Para obtener el repositorio desde esta pagina ejecutar:
```
git clone https://github.com/MarianoSaez/final.git
```

## Despliegue de la infraestructura de servidor
Ahora es necesario realizar el despligue de los containers de docker con:
```
docker-compose up --build
```

# Guia de instalacion del cliente
## Requerimientos
- Python version 3.10 (https://www.python.org/downloads/release/python-3100/)

## Descarga del cliente
Para obtener el repositorio desde esta pagina ejecutar:
```
git clone https://github.com/MarianoSaez/final.git
```
Luego realizar un cambio de directorio a:
```
cd client/
```

## Ejecucion del cliente
Segun como se detalla en el [uso basico de la aplicacion](https://github.com/MarianoSaez/final#readme).
```
 scrap [URL] [-t|--tags] [-c|--htmlclass] [-s|--style]
```




