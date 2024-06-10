# Databricks notebook source
import requests 
import time

_DATABRICK_TOKEN = dbutils.notebook.entry_point.getDbutils().notebook().getContext().apiToken().get()

def run_databricks_job(query):
    job_id = "814696812463781"    
    databricks_token = f"Bearer {_DATABRICK_TOKEN}"
    databricks_env_url = "https://dbc-4baa1af4-a1f3.cloud.databricks.com/api/2.0/jobs/run-now"  

    # 'https://adb-7114432958180866.6.azuredatabricks.net/api/2.1/jobs/run-now'
    databricks_params = {
                "job_id": job_id,
                "notebook_params":{
                    "Query_String": query
                }
                }

    r = requests.post(
        url=databricks_env_url,
                headers={
            'Authorization': databricks_token, 
            'content-type': 'application/json'
            },
        json=databricks_params
    )
    return r


def check_databricks_job(run_id):
    job_id = "814696812463781"
    databricks_token = f"Bearer {_DATABRICK_TOKEN}"
    databricks_env_url = f"https://dbc-4baa1af4-a1f3.cloud.databricks.com/api/2.1/jobs/runs/get"  

    r = requests.get(
        url=databricks_env_url,
                headers={
            'Authorization': databricks_token, 
            'content-type': 'application/json'
            },
        params={
            "run_id":run_id
        }
    )
    response_json = r.json()
    tasks = response_json.get("tasks", [])
    task_outputs = []
    for task in tasks:
        task_run_id = task.get("run_id")
        task_output = requests.get(
            url=databricks_env_url + "-output",
            headers={
                'Authorization': databricks_token, 
                'content-type': 'application/json'
            },
            params={
                "run_id": task_run_id
            }
        )
        task_outputs.append(task_output.json())
    return task_outputs

def get_response(query):
    r = run_databricks_job(query=query)
    run_id= r.json()['run_id']
    state = 'RUNNING'
    while (state=='RUNNING' or state=='PENDING'):
        print(state)
        response = check_databricks_job(run_id=run_id)
        time.sleep(2)
        state=response[0]['metadata']['state']['life_cycle_state']

    response_text = response[0]['notebook_output']['result']
    return response_text



# COMMAND ----------

QUERY = "Get the Average Value of Crude each month over the last 6 months?"
response = get_response(query=QUERY)
print(response)


# COMMAND ----------


