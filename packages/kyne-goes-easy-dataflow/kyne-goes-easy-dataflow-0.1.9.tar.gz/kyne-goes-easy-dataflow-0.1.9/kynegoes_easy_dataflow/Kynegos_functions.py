import os
import pandas as pd
import pickle
import time

def setup_credentials():
    """
    Configura las credenciales para usar Google Cloud API.
    Utiliza la variable de entorno GOOGLE_APPLICATION_CREDENTIALS si está definida,
    de lo contrario, usa la autenticación predeterminada.
    """
    from google.auth import default, load_credentials_from_file
    if 'GOOGLE_APPLICATION_CREDENTIALS' in os.environ:
        # Usa las credenciales del archivo JSON especificado en la variable de entorno
        credentials, project = load_credentials_from_file(os.environ['GOOGLE_APPLICATION_CREDENTIALS'])
    else:
        # Usa la autenticación predeterminada (por ejemplo, en Colab Enterprise)
        credentials, project = default()
    
    return credentials, project

def get_bigquery_client():
    from google.cloud import bigquery
    credentials, project = setup_credentials()
    return bigquery.Client(credentials=credentials, project=project)

def get_storage_client():
    from google.cloud import storage
    credentials, project = setup_credentials()
    return storage.Client(credentials=credentials, project=project)

def get_aiplatform_client():
    from google.cloud import aiplatform
    credentials, project = setup_credentials()
    aiplatform.init(credentials=credentials, project=project)
    return aiplatform

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
    from google.cloud import bigquery
    client_bq = get_bigquery_client()
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
    client_bq = get_bigquery_client()
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
    client = get_storage_client()
    try:
        bucket = client.bucket(target_bucket_name)
        if not bucket.exists():
            bucket.location = target_location
            client.create_bucket(bucket)
            print(f"Bucket '{target_bucket_name}' creado exitosamente en la ubicación '{target_location}'.")
        else:
            print(f"El bucket '{target_bucket_name}' ya existe.")
    except Exception as e:
        print(f"Error al crear el bucket '{target_bucket_name}': {e}")

def read_dataframe_from_pickle_gcs(bucket_name, file_name):
    """
    Lee un DataFrame de Pandas desde un bucket de Google Cloud Storage en formato binario (pickle).

    Args:
        bucket_name (str): El nombre del bucket de Google Cloud Storage.
        file_name (str): El nombre del archivo desde el cual se leerá el DataFrame.

    Returns:
        pd.DataFrame: El DataFrame leído desde el archivo en GCS.
    """
    client = get_storage_client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    print(f"Leyendo DataFrame desde gs://{bucket_name}/{file_name}.")
    df_pickle = blob.download_as_string()
    df = pickle.loads(df_pickle)
    print("DataFrame leído correctamente desde GCS.")
    return df

def save_dataframe_to_gcs_pickle(df, bucket_name, file_name):
    """
    Guarda un DataFrame de Pandas en un bucket de Google Cloud Storage en formato binario (pickle).

    Args:
        df (pd.DataFrame): El DataFrame que se desea guardar.
        bucket_name (str): El nombre del bucket de Google Cloud Storage.
        file_name (str): El nombre del archivo con el que se guardará el DataFrame.

    Raises:
        DataFrameAlreadyExistsError: Si el archivo con el nombre dado ya existe en el bucket.
    """
    client = get_storage_client()
    bucket = client.bucket(bucket_name)
    blobs = list(bucket.list_blobs(prefix=file_name))

    if any(file_name in blob.name for blob in blobs):
        raise DataFrameAlreadyExistsError(f"El DataFrame con el nombre '{file_name}' ya existe en el bucket '{bucket_name}'.")
    else:
        df_pickle = pickle.dumps(df)
        blob = bucket.blob(file_name)
        blob.upload_from_string(df_pickle, content_type='application/octet-stream')
        print(f"DataFrame guardado en gs://{bucket_name}/{file_name}.")

def read_dataframe_from_gcs_csv(bucket_name, file_name):
    """
    Lee un DataFrame de Pandas desde un archivo CSV almacenado en un bucket de Google Cloud Storage.

    Args:
        bucket_name (str): El nombre del bucket de Google Cloud Storage.
        file_name (str): El nombre del archivo CSV en el bucket.

    Returns:
        pd.DataFrame: El DataFrame leído desde el archivo CSV en GCS.
    """
    from io import StringIO

    client = get_storage_client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    
    print(f"Leyendo DataFrame desde gs://{bucket_name}/{file_name}.")
    csv_data = blob.download_as_text()  # Descarga el contenido del archivo como texto
    df = pd.read_csv(StringIO(csv_data))  # Convierte el texto en un DataFrame de Pandas
    print("DataFrame leído correctamente desde GCS en formato CSV.")
    
    return df

def save_dataframe_to_gcs_csv(df, bucket_name, file_name):
    """
    Guarda un DataFrame de Pandas en un bucket de Google Cloud Storage en formato CSV.

    Args:
        df (pd.DataFrame): El DataFrame que se desea guardar.
        bucket_name (str): El nombre del bucket de Google Cloud Storage.
        file_name (str): El nombre del archivo con el que se guardará el DataFrame.

    Raises:
        DataFrameAlreadyExistsError: Si el archivo con el nombre dado ya existe en el bucket.
    """
    client = get_storage_client()
    bucket = client.bucket(bucket_name)
    blobs = list(bucket.list_blobs(prefix=file_name))

    if any(file_name in blob.name for blob in blobs):
        raise DataFrameAlreadyExistsError(f"El DataFrame con el nombre '{file_name}' ya existe en el bucket '{bucket_name}'.")
    else:
        # Convierte el DataFrame a CSV en memoria y sube a GCS
        csv_data = df.to_csv(index=False)
        blob = bucket.blob(file_name)
        blob.upload_from_string(csv_data, content_type='text/csv')
        print(f"DataFrame guardado en formato CSV en gs://{bucket_name}/{file_name}.")

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
    client = get_storage_client()
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
    client_ai = get_aiplatform_client()
    client_ai.init(project=target_project, location=target_location)
    print(f"Subiendo modelo desde gs://{bucket_name}/{model_name} a Vertex AI con el nombre '{display_name}'.")
    model = client_ai.Model.upload(
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
    client_ai = get_aiplatform_client()
    client_ai.init(project=project_id, location=location)
    model_name = f"projects/{project_id}/locations/{location}/models/{model_id}"
    print(f"Cargando modelo desde Vertex AI con ID '{model_name}'.")
    model = client_ai.Model(model_name=model_name)
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
    client = get_storage_client()
    source_client = client.bucket(source_bucket_name)
    target_client = client.bucket(target_bucket_name)

    blobs = list(source_client.list_blobs(prefix=source_model_name + "/"))

    print(f"Iniciando copia de modelo '{source_model_name}' de '{source_bucket_name}' a '{target_bucket_name}'.")

    for blob in blobs:
        if blob.name.startswith(source_model_name + "/"):
            target_blob_name = target_model_name + blob.name[len(source_model_name):]
            source_client.copy_blob(blob, target_client, target_blob_name)
            print(f"Copiado '{blob.name}' a '{target_blob_name}'.")

    print(f"Modelo '{source_model_name}' copiado correctamente a '{target_bucket_name}'.")

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
    client_ai = get_aiplatform_client()
    client_ai.init(project=project_id, location=location)

    print(f"Creando un nuevo endpoint con el nombre '{endpoint_display_name}'...")
    endpoint = client_ai.Endpoint.create(display_name=endpoint_display_name)
    print(f"Nuevo endpoint creado: {endpoint.resource_name}")

    time.sleep(30)

    deployed_model_display_name = f"{display_name_pro}_{model.name.split('/')[-1]}"

    print("Iniciando despliegue del modelo...")
    try:
        endpoint.deploy(
            model=model,
            deployed_model_display_name=deployed_model_display_name,
            traffic_split={"0": 100},
            machine_type="n2-standard-4"
        )

        print(f"Modelo desplegado exitosamente: {deployed_model_display_name} en el endpoint {endpoint.display_name}")

    except Exception as e:
        print(f"Error durante el despliegue: {e}")
        raise

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
    client_ai = get_aiplatform_client()
    client_ai.init(project=project_id, location=location)
    print(f"Inicializado Vertex AI para el proyecto '{project_id}' en la ubicación '{location}'.")

    endpoint_name = f"projects/{project_id}/locations/{location}/endpoints/{endpoint_id}"
    endpoint = client_ai.Endpoint(endpoint_name=endpoint_name)
    print(f"Endpoint '{endpoint_name}' cargado desde Vertex AI.")

    return endpoint
