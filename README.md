# Evaluacion de curso Cosmos DB

## Pasos para evaluar la aplicacion en el repositorio
1. Abrir el codespace asociado al repositorio
2. Una vez dentro del codespace lanzar el comando siguiente en la seccion de TERMINAL
```
uvicorn app:app --reload
```
3. Al terminar de levantar la aplicacion en la seccion PUERTOS permitira ingresar a una URL ubicada en la columna Direccion reenviada haciendo Ctrl + Click en la direccion
4. Una vez abierta la direccion agregarle al final de la URL lo siguiente : /docs
5. Al abrirse la pagina con todas los endpoints expuestos en el API se podran probar uno a uno con la opcion de Try Out y Execute