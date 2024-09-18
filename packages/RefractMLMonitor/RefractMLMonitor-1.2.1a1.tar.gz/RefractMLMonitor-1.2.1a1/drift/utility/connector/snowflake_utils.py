from fdc_connector_python_sdk.factory.connectorFactory import ConnectionFactory
import requests

connection_manager = "http://fdc-project-manager:80/project-manager"


def get_conn_details_from_ds_name(ds_name, project_id):
    if not project_id:
        raise Exception("Project ID is not provided!")

    url = f"{connection_manager}/connections/api/External/v2/external/getConnConfig/" \
          f"{ds_name}/fdcuser/{project_id}"  # user id hard coded, as it's not being used in API code.
    return requests.get(url, verify=False).json()


def get_connection(connection_details):
    region = connection_details['region'] if connection_details["cloudPlatform"] is None \
        else connection_details['region'] + "." + connection_details["cloudPlatform"]
    url = "https://" + connection_details["params"]["READER"]["accountId"] + "." + region + ".snowflakecomputing.com"
    auth_type = connection_details["params"]["READER"]["authenticationType"]
    if auth_type == 'privateKey':
        auth_type = 'keyBased'
    connection_params = {
        'connectionURL': url,
        'username': connection_details["params"]["READER"]["user"],
        'password': connection_details["params"]["READER"]["password"],
        'role': connection_details["params"]["READER"]["role"],
        'warehouse': connection_details["params"]["READER"]["wareHouse"],
        'database': connection_details["params"]["READER"]["database"],
        'schema': connection_details["params"]["READER"]["schema"],
        'applicationName': "FOSFOR",
        'private_key': connection_details["params"]["READER"]["privateKey"],
        'passphrase': connection_details["params"]["READER"]["passPhrase"]
    }
    snowflake_connector = ConnectionFactory.get_connector("snowflake")
    snowflake_dto = ConnectionFactory.get_dto("SNOWFLAKE")
    param_dict = snowflake_dto.set_param(auth_type=auth_type, **connection_params)
    connection = snowflake_connector.get_connection(param_dict)
    return connection


def fetch_data_frame(ds_name, project_id, row_count, filter_condition):
    try:
        connection_details = get_conn_details_from_ds_name(ds_name=ds_name, project_id=project_id)
        connection = get_connection(connection_details=connection_details)
        table_name = connection_details["params"]["READER"]["tables"]
        query = get_dataframe_query(table_name, row_count, filter_condition, double_quotes=True)
        snowflake_connector = ConnectionFactory.get_connector("snowflake")
        data = snowflake_connector.execute_single_statement(query, "FOSFOR_INSIGHT_PLUGIN_RUN", connection)
        data_frames = data.fetch_pandas_all()
        snowflake_connector.close_connection(connection)
        return data_frames
    except Exception as ex:
        print(f"Exception occurred in reading data_frame from snowflake connection: {ex}")


def get_dataframe_query(table_name, row_count, filter_condition, top=None, double_quotes=None):
    """
    To get the query to fetch dataframe
    :param table_name:
    :param row_count:
    :param filter_condition:
    :param top:
    :param double_quotes:
    :return: query
    """
    if double_quotes:
        query = f'SELECT * FROM "{table_name}"'
    else:
        query = f"SELECT * FROM {table_name}"
    if top and int(row_count) > 0:
        print(f"fetching {row_count} records!")
        query = f"SELECT TOP {row_count} * FROM {table_name}"
    if filter_condition:
        query = query + " " + filter_condition
    if not top and int(row_count) > 0:
        print(f"fetching {row_count} records!")
        query = f"{query} LIMIT {row_count}"
    return query

