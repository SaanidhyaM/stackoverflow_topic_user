from google.cloud import bigquery


def expert_finder(topic, client):
    '''
    Returns a DataFrame with the user IDs who have written Stack Overflow answers on a topic.

    Inputs:
        topic: A string with the topic of interest
        client: A Client object that specifies the connection to the Stack Overflow dataset

    Outputs:
        results: A DataFrame with columns for user_id and number_of_answers. Follows similar logic to bigquery_experts_results shown above.
    '''
    my_query = """
               SELECT a.owner_user_id AS user_id, COUNT(1) AS number_of_answers
               FROM `bigquery-public-data.stackoverflow.posts_questions` AS q
               INNER JOIN `bigquery-public-data.stackoverflow.posts_answers` AS a
                   ON q.id = a.parent_Id
               WHERE q.tags like '%{topic}%'
               GROUP BY a.owner_user_id
               """

    # Set up the query (a real service would have good error handling for 
    # queries that scan too much data)
    safe_config = bigquery.QueryJobConfig(maximum_bytes_billed=10**10)      
    my_query_job = client.query(my_query, job_config=safe_config)

    # API request - run the query, and return a pandas DataFrame
    results = my_query_job.to_dataframe()

    return results

# Create a "Client" object
client = bigquery.Client()

# Construct a reference to the "stackoverflow" dataset
dataset_ref = client.dataset("stackoverflow", project="bigquery-public-data")

# API request - fetch the dataset
dataset = client.get_dataset(dataset_ref)