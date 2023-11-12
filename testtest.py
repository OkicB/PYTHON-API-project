from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn, psycopg2, json
from google.cloud import bigquery, pubsub, pubsub_v1
from google.cloud.pubsub_v1.types import PullRequest

#publisher = pubsub_v1.PublisherClient.from_service_account_file('COPY YOUR_CREDENTIALS_FILE.json')
bq_client = bigquery.Client.from_service_account_json('COPY YOUR_CREDENTIALS_FILE.json /app/credentials/project-id.json')
subscriber = pubsub.SubscriberClient.from_service_account_file('COPY YOUR_CREDENTIALS_FILE.json /app/credentials/project-id.json')
publisher = pubsub_v1.PublisherClient.from_service_account_file('COPY YOUR_CREDENTIALS_FILE.json /app/credentials/project-id.json')
topic_path = publisher.topic_path('PROJECT_ID', 'YOUR_TOPIC')
subscription_path = subscriber.subscription_path('PROJECT_ID', 'SUBS_PATH')


app = FastAPI(debug=True)

DB_HOST = "YOUR_HOST"
DB_PORT = "YOUR_PORT"
DB_NAME = "YOUR_NAME"
DB_USER = "YOUR_USER"
DB_PASSWORD = "YOUR_PASS"

class User(BaseModel):
    id: int
    name: str

def get_db():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return conn

'''@app.get("/")
async def root_func():
    print('hello: ' 'world')
'''
@app.get("/api/test", response_model=List[User])
async def get_user():
    try:
        conn = get_db()
        with conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id, name FROM test;")
                rows = cursor.fetchall()
        
        users = [User(id=row[0], name=row[1]) for row in rows]
        return users
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/bigquery_data", response_model=List[dict])
async def get_bigquery_data():
    try:
        dataset_id = "YOUR_PROJECT_ID.DATASET"
        table_name = "test"

        sql_query = f"SELECT id, name FROM `{dataset_id}.{table_name}`;"

        query_job = bq_client.query(sql_query)
        results = query_job.result()

        data = [{"id": row.id, "name": row.name} for row in results]

        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/post_to_bigquery", response_model=User)
async def post_to_bigquery(user: User):
    try:
        data_to_insert = [{"id": user.id, "name": user.name}]
        dataset_id = "YOUR_DATASET"
        table_name = "test"
        table_ref = bq_client.dataset(dataset_id).table(table_name)
        table = bq_client.get_table(table_ref)

        bq_client.insert_rows(table, data_to_insert)

        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
try:
    topic = publisher.create_topic(request={"name": topic_path})
except Exception as e:
    print("Topic already exists.")


#PUB SUB Message publishing route
@app.post("/publish_message")
async def publish_message(message: str):
    try:
        data = message.encode('utf-8')
        publisher.publish(topic_path, data=data)
        return {"message": "Message published successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

dataset_id = "YOUR_DATASET"
table_name2 = "subs-table"
table_ref = bq_client.dataset(dataset_id).table(table_name2)
table = bq_client.get_table(table_ref)
#PUB SUB SUBS HANDLING ROUTE
@app.post("/receive_message")
async def receive_message():
    try:
        pull_request = PullRequest(subscription_path, max_messages=10, return_immediately=True)
        response = subscriber.pull(request=pull_request)
        messages = response.received_messages

        for message in messages:
            data = message.message.data.decode('utf-8')
            parsed_data = json.loads(data)
            id = parsed_data['id']
            name = parsed_data['name']
            row_to_insert = [(id, name)]
            errors = bq_client.insert_rows(table, row_to_insert)

            if errors:
                print("Encountered errors while inserting rows: {}".format(errors))
            subscriber.acknowledge(subscription_path, [message.ack_id])
            
        return {"messages": len(messages)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

'''
@app.post("/test", response_model=User)
async def create_user(user: User):
    try:
        conn = get_db()
        with conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO test (id, name) VALUES (%s, %s);", (user.id, user.name)
                )
        return user
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    

#PUB SUB Message publishing route
@app.post("/publish_message")
async def publish_message(message: str):
    try:
        topic = subscriber.topic('YOUR_TOPIC')
        topic.publish(message.encode('utf-8'))
        return {"message": "Message published successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#PUB SUB SUBS HANDLING ROUTE
@app.post("/receive_message")
async def receive_message():
    try:
        subscription = subscriber.subscription('YOUR_SUBSCRIPTION')
        received_messages = subscription.pull(return_immediately=True)
        messages = []
        for ack_id, message in received_messages:
            messages.append(message.data.encode('utf-8'))
        subscription.acknowledge([ack_id for ack_id, _ in received_messages])
        return {"messages": messages}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
'''
