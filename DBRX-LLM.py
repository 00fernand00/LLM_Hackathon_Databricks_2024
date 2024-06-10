# Databricks notebook source
# MAGIC %pip install databricks_genai_inference

# COMMAND ----------

dbutils.library.restartPython()

# COMMAND ----------

df = spark.sql('select * from workspace.default.wti_prices_curated')

# COMMAND ----------

def get_metadata(catalog,table_name):
    table_meta = spark.sql(f"select * from {catalog}.information_schema.tables where table_name = '{table_name}'")
    table_meta.show()
    # table_meta_text = table_meta.select('comment').collect()[0]['comment']
    table_meta_text = {"table_name" : table_name}
    import json 
    column_meta = spark.sql(f"select * from {catalog}.information_schema.columns where table_name = '{table_name}'")
    column_meta_text_preprocess = column_meta.select('column_name', 'comment', 'data_type').collect()[:]

    # Initialize a list to store dictionaries for each row
    data_list = []

    # Iterate over the sample data and populate the list with dictionaries
    for row in column_meta_text_preprocess:
        data_list.append({
            'column_name': row.column_name,
            'comment': row.comment,
            'data_type': row.data_type
        })

    # Convert the list of dictionaries to JSON format
    column_meta_text = json.dumps(data_list, indent=4)
    return table_meta_text, column_meta_text

catalog = "workspace"

table_meta_text1, column_meta_text1 = get_metadata(catalog, 'wti_prices_curated')

print(f"table_meta_text1: {table_meta_text1}")
print(f"column_meta_text1: {column_meta_text1}")

# COMMAND ----------

table_meta_text = table_meta_text1
column_meta_text = column_meta_text1

# COMMAND ----------

print(table_meta_text)
print(column_meta_text)

# COMMAND ----------

SQL_TEMPLATE = f"""You are a Databricks SQL assistant. Your ONLY job is to write CORRECT SQL code that can be ran in Databricks notebooks. Do not provide any other charcters in your answer other than the SQL code. 

YOU DO NOT DO ANYTHING OTHER THAN WRITE SQL CODE.

CONTEXT TO USE TO CONSTRUCT SQL QUERY:
TABLE INFORMATION:
{table_meta_text}

COLUMN INFORMATION:
{column_meta_text}

YOU DO NOT DO ANYTHING OTHER THAN WRITE SQL CODE.

EXAMPLE:
USER: Give me the total count of all employees

CORRECT OUTPUT:
SELECT COUNT(*)
FROM my_table;

"""

# COMMAND ----------

def get_sql(query_text):
  from databricks_genai_inference import ChatCompletion

  # Only required when running this example outside of a Databricks Notebook
  #DATABRICKS_HOST="https://<workspace>.databricks.com"
  #DATABRICKS_TOKEN=""
  DATABRICKS_HOST = "https://dbc-4baa1af4-a1f3.cloud.databricks.com"
  #"https://dbc-4baa1af4-a1f3.cloud.databricks.com/serving-endpoints"
  # DATABRICKS_TOKEN format: "dapi..."
  ## Temp token: dbutils.notebook.entry_point.getDbutils().notebook().getContext().apiToken().get()
  DATABRICK_TOKEN = dbutils.notebook.entry_point.getDbutils().notebook().getContext().apiToken().get()
  # DATABRICKS_TOKEN = """

  def get_response(SQL_TEMPLATE, query_text):
    completions_response = ChatCompletion.create(model="databricks-dbrx-instruct",
                                    messages=[{"role": "system", "content": SQL_TEMPLATE},
                                              {"role": "user","content": query_text}],
                                    max_tokens=50)
    return completions_response

  sql_result = get_response(SQL_TEMPLATE, query_text)
  return sql_result

def get_df_from_sql(sql):
    cleaned_sql_query = sql_result.message.replace("\\", "")
    spark.sql(f"USE CATALOG {catalog}")
    spark.sql("USE SCHEMA default")
    df = spark.sql(cleaned_sql_query)
    return df
      

# COMMAND ----------

import re

def extract_sql_from_string(input_string):
    # Find the SQL statement inside triple backticks
    sql_match = re.search(r'```(.*?)```', input_string, re.DOTALL)
    if sql_match:
        return sql_match.group(1)
    else:
        return None 

# COMMAND ----------

query_text = dbutils.widgets.get("Query_String")

# COMMAND ----------

sql_result = get_sql(query_text)
# df = get_df_from_sql(sql_result)

sql_text = sql_result.message.replace("sql", "")

#Check if Inside Backticks 
formatted_sql_text = extract_sql_from_string(sql_text)
print(formatted_sql_text)

if formatted_sql_text == None:
    pass
else: 
    sql_text = formatted_sql_text.replace("sql", "")

df = get_df_from_sql(sql_text)
display(df)

# COMMAND ----------

rows = df.collect()
result_string = "\n".join([str(row) for row in rows])

print(result_string)

# COMMAND ----------

dbutils.notebook.exit(result_string)

# COMMAND ----------


