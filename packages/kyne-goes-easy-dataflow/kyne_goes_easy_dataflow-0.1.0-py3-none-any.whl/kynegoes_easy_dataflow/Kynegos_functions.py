from google.cloud import bigquery
from google.cloud import storage
from google.cloud import aiplatform
import tensorflow as tf
import pandas as pd
import pickle

client_bq = bigquery.Client()

def upload_to_bigquery(df, dataset_id, table_name):
    """
    Sube un DataFrame a una tabla de BigQuery, reemplazando los datos existentes.

    Args:
        df (pd.DataFrame): El DataFrame que se desea subir.
        dataset_id (str): El ID del dataset de BigQuery.
        table_name (str): El nombre de la tabla en BigQuery.

    Returns:
        None
    """
    table_id = f"{dataset_id}.{table_name}"
    job = client_bq.load_table_from_dataframe(df, table_id, job_config=bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE"))
    job.result()
    print(f"DataFrame subido a BigQuery en la tabla '{table_id}'.")

def query_bigquery(query):
    """
    Ejecuta una consulta en BigQuery y devuelve los resultados como un DataFrame.

    Args:
        query (str): La consulta SQL a ejecutar.

    Returns:
        pd.DataFrame: Los resultados de la consulta.
    """
    query_job = client_bq.query(query)
    print(f"Ejecutando consulta en BigQuery: {query}")
    result_df = query_job.to_dataframe()
    print("Consulta completada y resultados devueltos como DataFrame.")
    return result_df

def crear_bucket(target_project, target_location, target_bucket_name):
    """
    Crea un bucket en Google Cloud Storage si no existe.

    Args:
        target_project (str): El ID del proyecto de Google Cloud.
        target_location (str): La ubicación donde se creará el bucket.
        target_bucket_name (str): El nombre del bucket.

    Returns:
        None
    """
    try:
        client = storage.Client(project=target_project)
        bucket = client.bucket(target_bucket_name)
        if not bucket.exists():
            bucket.location = target_location
            client.create_bucket(bucket)
            print(f"Bucket '{target_bucket_name}' creado exitosamente en la ubicación '{target_location}'.")
        else:
            print(f"El bucket '{target_bucket_name}' ya existe.")
    except Exception as e:
        print(f"Error al crear el bucket '{target_bucket_name}': {e}")

def read_dataframe_from_gcs(bucket_name, file_name):
    """
    Lee un DataFrame de Pandas desde un bucket de Google Cloud Storage en formato binario (pickle).

    Args:
        bucket_name (str): El nombre del bucket de Google Cloud Storage.
        file_name (str): El nombre del archivo desde el cual se leerá el DataFrame.

    Returns:
        pd.DataFrame: El DataFrame leído desde el archivo en GCS.
    """
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    print(f"Leyendo DataFrame desde gs://{bucket_name}/{file_name}.")
    df_pickle = blob.download_as_string()
    df = pickle.loads(df_pickle)
    print("DataFrame leído correctamente desde GCS.")
    return df

def save_dataframe_to_gcs(df, bucket_name, file_name):
    """
    Guarda un DataFrame de Pandas en un bucket de Google Cloud Storage en formato binario (pickle).

    Args:
        df (pd.DataFrame): El DataFrame que se desea guardar.
        bucket_name (str): El nombre del bucket de Google Cloud Storage.
        file_name (str): El nombre del archivo con el que se guardará el DataFrame.

    Raises:
        DataFrameAlreadyExistsError: Si el archivo con el nombre dado ya existe en el bucket.
    """
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blobs = list(bucket.list_blobs(prefix=file_name))

    if any(file_name in blob.name for blob in blobs):
        raise DataFrameAlreadyExistsError(f"El DataFrame con el nombre '{file_name}' ya existe en el bucket '{bucket_name}'.")
    else:
        df_pickle = pickle.dumps(df)
        blob = bucket.blob(file_name)
        blob.upload_from_string(df_pickle, content_type='application/octet-stream')
        print(f"DataFrame guardado en gs://{bucket_name}/{file_name}.")

def save_model_to_gcs(model, bucket_name, model_name):
    """
    Guarda un modelo de TensorFlow en un bucket de Google Cloud Storage.

    Args:
        model (tf.keras.Model): El modelo de TensorFlow que se desea guardar.
        bucket_name (str): El nombre del bucket de Google Cloud Storage.
        model_name (str): El nombre del archivo con el que se guardará el modelo.

    Raises:
        ModelAlreadyExistsError: Si el modelo con el nombre dado ya existe en el bucket.
    """
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blobs = list(bucket.list_blobs(prefix=model_name))

    if any(model_name in blob.name for blob in blobs):
        raise ModelAlreadyExistsError(f"El modelo con el nombre '{model_name}' ya existe en el bucket '{bucket_name}'.")
    else:
        model_dir = f'gs://{bucket_name}/{model_name}'
        model.save(model_dir)
        print(f"Modelo guardado en {model_dir}.")

def upload_model_to_vertex_ai(target_project, target_location, bucket_name, model_name, display_name):
    """
    Sube un modelo de TensorFlow a Vertex AI.

    Args:
        target_project (str): El ID del proyecto de Google Cloud.
        target_location (str): La ubicación del modelo en Vertex AI.
        bucket_name (str): El nombre del bucket de Google Cloud Storage.
        model_name (str): El nombre del archivo con el que se guardó el modelo en GCS.
        display_name (str): El nombre que se mostrará en Vertex AI.

    Returns:
        google.cloud.aiplatform.Model: El modelo subido a Vertex AI.
    """
    aiplatform.init(project=target_project, location=target_location)
    print(f"Subiendo modelo desde gs://{bucket_name}/{model_name} a Vertex AI con el nombre '{display_name}'.")
    model = aiplatform.Model.upload(
        display_name=display_name,
        artifact_uri=f'gs://{bucket_name}/{model_name}',
        serving_container_image_uri="us-docker.pkg.dev/vertex-ai/prediction/tf2-cpu.2-8:latest"
    )
    print(f"Modelo subido a Vertex AI con el nombre '{display_name}'.")
    return model

def load_model_from_vertex_ai(model_id, project_id, location):
    """
    Carga un modelo desde Vertex AI en una variable.

    Args:
        model_id (str): El ID del modelo en Vertex AI.
        project_id (str): El ID del proyecto de GCP.
        location (str): La ubicación del modelo en Vertex AI.

    Returns:
        aiplatform.Model: El modelo cargado desde Vertex AI.
    """
    aiplatform.init(project=project_id, location=location)
    model_name = f"projects/{project_id}/locations/{location}/models/{model_id}"
    print(f"Cargando modelo desde Vertex AI con ID '{model_name}'.")
    model = aiplatform.Model(model_name=model_name)
    print(f"Modelo '{model_name}' cargado correctamente desde Vertex AI.")
    return model

def copy_model_between_buckets(source_project, source_location, source_bucket_name, source_model_name,
                               target_project, target_location, target_bucket_name, target_model_name):
    """
    Copia un modelo (carpeta) de un bucket en un proyecto y ubicación a otro bucket en otro proyecto y ubicación.

    Args:
        source_project (str): El ID del proyecto de origen.
        source_location (str): La ubicación del bucket de origen.
        source_bucket_name (str): El nombre del bucket de origen.
        source_model_name (str): El nombre de la carpeta del modelo en el bucket de origen.
        target_project (str): El ID del proyecto de destino.
        target_location (str): La ubicación del bucket de destino.
        target_bucket_name (str): El nombre del bucket de destino.
        target_model_name (str): El nombre de la carpeta del modelo en el bucket de destino.

    Returns:
        None
    """
    source_client = storage.Client(project=source_project)
    target_client = storage.Client(project=target_project)

    source_bucket = source_client.bucket(source_bucket_name)
    target_bucket = target_client.bucket(target_bucket_name)

    blobs = list(source_bucket.list_blobs(prefix=source_model_name + "/"))

    print(f"Iniciando copia de modelo '{source_model_name}' de '{source_bucket_name}' a '{target_bucket_name}'.")

    for blob in blobs:
        if blob.name.startswith(source_model_name + "/"):
            target_blob_name = target_model_name + blob.name[len(source_model_name):]
            source_bucket.copy_blob(blob, target_bucket, target_blob_name)
            print(f"Copiado '{blob.name}' a '{target_blob_name}'.")

    print(f"Modelo '{source_model_name}' copiado correctamente a '{target_bucket_name}'.")


def deploy_model_with_custom_name(model_id, project_id, location, endpoint_display_name, display_name_pro):
    """
    Despliega un modelo en Vertex AI en un endpoint específico con un nombre personalizado.

    Args:
        model_id (str): El ID del modelo en Vertex AI.
        project_id (str): El ID del proyecto de Google Cloud.
        location (str): La ubicación del modelo y el endpoint en Vertex AI.
        endpoint_display_name (str): El nombre de visualización del endpoint.
        display_name_pro (str): Prefijo para el nombre de visualización del modelo desplegado.

    Returns:
        None
    """
    # Inicializa la configuración de Vertex AI
    aiplatform.init(project=project_id, location=location)
    print(f"Inicializado Vertex AI para el proyecto '{project_id}' en la ubicación '{location}'.")

    # Construir el nombre del modelo completo
    model_name = f"projects/{project_id}/locations/{location}/models/{model_id}"
    model = aiplatform.Model(model_name=model_name)
    print(f"Modelo '{model_name}' cargado desde Vertex AI.")

    # Buscar el endpoint existente con el nombre dado
    endpoints = aiplatform.Endpoint.list(filter=f'display_name="{endpoint_display_name}"')
    
    # Verificar si el endpoint ya existe o necesita ser creado
    if endpoints:
        endpoint = endpoints[0]
        print(f"Endpoint existente encontrado: {endpoint.resource_name}")
    else:
        endpoint = aiplatform.Endpoint.create(display_name=endpoint_display_name)
        print(f"Endpoint creado: {endpoint.resource_name}")

    # Desplegar el modelo en el endpoint con un nombre de visualización personalizado
    deployed_model_display_name = f"{display_name_pro}_{model_id}"
    deployed_model = endpoint.deploy(
        model=model,
        deployed_model_display_name=deployed_model_display_name,
        traffic_split={"0": 100},
        machine_type="n1-standard-2"
    )
    print(f"Modelo '{deployed_model.display_name}' desplegado exitosamente en el endpoint '{endpoint.display_name}'.")


def deploy_model_within_endpoint(model, project_id, location, endpoint_display_name, display_name_pro):
    """
    Despliega un modelo en Vertex AI en un endpoint existente o crea uno nuevo si no existe.

    Args:
        model (aiplatform.Model): El objeto de modelo en Vertex AI ya cargado.
        project_id (str): El ID del proyecto de Google Cloud.
        location (str): La ubicación del modelo y el endpoint en Vertex AI.
        endpoint_display_name (str): El nombre de visualización del endpoint.
        display_name_pro (str): Prefijo para el nombre de visualización del modelo desplegado.

    Returns:
        None
    """
    # Inicializa la configuración de Vertex AI
    aiplatform.init(project=project_id, location=location)


El mensaje de error "La operación de despliegue no se inició correctamente. El objeto operation es None." indica que la llamada a deploy() del endpoint no está retornando un objeto de operación válido, lo cual es inusual si todo parece haber salido bien según los logs.

Posibles Causas y Soluciones
Revisar la Versión del SDK:

Asegúrate de que tienes la versión más reciente del SDK de Google Cloud AI Platform (google-cloud-aiplatform). Puedes actualizarla usando:
bash
Copiar código
pip install --upgrade google-cloud-aiplatform
Verificar los Permisos y la Configuración del Entorno:

Asegúrate de que tu entorno tiene los permisos correctos para desplegar modelos y crear endpoints en Vertex AI.
Verifica también que las credenciales de Google Cloud estén configuradas correctamente.
Probar Sin el Método result():

Si el despliegue está completándose según los logs, pero operation es None, podría ser un comportamiento inesperado del SDK. Intenta simplemente omitir el uso de operation.result() y verifica si el modelo está realmente desplegado y funcionando en el endpoint.
Código Ajustado
Aquí te dejo una versión ajustada para manejar la situación, sin esperar explícitamente por operation.result():

python
Copiar código
from google.cloud import aiplatform

def deploy_model_with_new_endpoint(model, project_id, location, endpoint_display_name, display_name_pro):
    """
    Despliega un modelo en Vertex AI en un nuevo endpoint con un nombre personalizado.

    Args:
        model (aiplatform.Model): El objeto de modelo en Vertex AI ya cargado.
        project_id (str): El ID del proyecto de Google Cloud.
        location (str): La ubicación del modelo y el endpoint en Vertex AI.
        endpoint_display_name (str): El nombre de visualización del nuevo endpoint.
        display_name_pro (str): Prefijo para el nombre de visualización del modelo desplegado.

    Returns:
        None
    """
    # Inicializa la configuración de Vertex AI
    aiplatform.init(project=project_id, location=location)

    # Crear un nuevo endpoint
    print(f"Creando un nuevo endpoint con el nombre '{endpoint_display_name}'...")
    endpoint = aiplatform.Endpoint.create(display_name=endpoint_display_name)
    print(f"Nuevo endpoint creado: {endpoint.resource_name}")


    # Definir el nombre de visualización del modelo desplegado
    deployed_model_display_name = f"{display_name_pro}_{model.name.split('/')[-1]}"

    print("Iniciando despliegue del modelo...")
    try:
        # Desplegar el modelo en el endpoint existente o nuevo
        endpoint.deploy(
            model=model,
            deployed_model_display_name=deployed_model_display_name,
            traffic_split={"0": 100},
            machine_type="n2-standard-4"
        )

        print(f"Modelo desplegado exitosamente: {deployed_model_display_name} en el endpoint {endpoint.display_name}")

    except Exception as e:
        print(f"Error durante el despliegue: {e}")
        raise  # Lanza la excepción para detener la ejecución si hay un error

def load_endpoint(project_id, location, endpoint_id):
    """
    Carga un endpoint en Vertex AI para poder realizar predicciones.

    Args:
        project_id (str): El ID del proyecto de Google Cloud.
        location (str): La ubicación del endpoint en Vertex AI.
        endpoint_id (str): El ID del endpoint en Vertex AI.

    Returns:
        aiplatform.Endpoint: El endpoint cargado desde Vertex AI.
    """
    # Inicializa la configuración de Vertex AI
    aiplatform.init(project=project_id, location=location)
    print(f"Inicializado Vertex AI para el proyecto '{project_id}' en la ubicación '{location}'.")

    # Referenciar al endpoint creado previamente
    endpoint_name = f"projects/{project_id}/locations/{location}/endpoints/{endpoint_id}"
    endpoint = aiplatform.Endpoint(endpoint_name=endpoint_name)
    print(f"Endpoint '{endpoint_name}' cargado desde Vertex AI.")

    return endpoint

