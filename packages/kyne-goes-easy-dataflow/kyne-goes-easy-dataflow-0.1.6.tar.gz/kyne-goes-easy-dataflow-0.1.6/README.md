
# Kyne Goes Easy Dataflow

`kyne-goes-easy-dataflow` es una colección de funciones genéricas diseñadas para simplificar las operaciones con Google Cloud Platform (GCP). Este paquete facilita la interacción con servicios como Google Cloud Storage, BigQuery, y otros componentes clave de GCP, permitiendo a los desarrolladores integrar estas herramientas de manera más eficiente en sus proyectos.

## Instalación

Para instalar el paquete, utiliza pip:

```bash
pip install kyne-goes-easy-dataflow
```

## Actualización

Para instalar el paquete, utiliza pip:

```bash
pip install --upgrade kyne-goes-easy-dataflow
```


## Uso

### Importar el Paquete

Para comenzar a utilizar las funciones disponibles, simplemente importa el paquete en tu script de Python:

```python

import kynegoes_easy_dataflow.Kynegos_functions as KYNEGOS_FUNCTIONS

```

### Exploración de Funciones

Para ver qué funciones están disponibles en el paquete, puedes utilizar la función `dir()` de Python:

```python
print(dir(KYNEGOS_FUNCTIONS))
```

Esto te mostrará una lista de todas las funciones disponibles en `kyne-goes-easy-dataflow`.

### Ejemplo de Uso

Cada función en el paquete está diseñada para realizar una tarea específica en GCP. Aquí te mostramos un ejemplo básico de cómo utilizar una de las funciones para cargar un archivo a Google Cloud Storage:

```python
# Ejemplo de cómo subir un archivo a Google Cloud Storage
KYNEGOS_FUNCTIONS.upload_to_gcs(bucket_name='nombre_del_bucket', source_file='ruta/del/archivo.txt', destination_blob='carpeta/archivo.txt')
```

### Documentación de Funciones

Para obtener detalles sobre cómo usar cada función, puedes consultar la documentación inline mediante `help()`:

```python
help(KYNEGOS_FUNCTIONS.upload_to_gcs)
```

Esto te proporcionará una descripción detallada de los parámetros y el propósito de la función.

## Contribuciones

Si deseas contribuir a este proyecto, por favor, envíe un correo mediante la plataforma Pypy.org