# Simple Web Scrapper Server
Simple Web Scrapper Server es una herramienta que facilita la tarea de buscar, procesar y reunir datos que se encuentran en sitios web.
 
 ![arquitectura](https://github.com/MarianoSaez/final/blob/main/img/Esquema%20gral..png)

 ## Uso basico de la aplicacion
 ```
 scrap [URL] [-t|--tags] [-c|--htmlclass] [-s|--style]
 ```
 URL \<list\> : Lista de url's a visitar por la herramienta

 -t | --tags \<list\> : Lista de HTML tags a buscar dentro de la respectiva pagina vistada

 -c | --htmlclass \<list\> : Lista de listas de clases HTML con la que se buscara dentro de la respectiva pagina visitada

 -s | --style \<list\> : Lista de listas de estilos con la que se buscara dentro de la respectiva pagina visitada

 ### Ejemplo de uso
 ```
 scrap https://somewebsite.com/path/to/data -t div -c div_table_cell -s font-weigth: bold
 ```