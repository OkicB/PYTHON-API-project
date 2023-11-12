# FastAPI Google Cloud Integration

Welcome to the FastAPI application integrated with Google Cloud services, specifically BigQuery and Pub/Sub. This project demonstrates the seamless interaction between a FastAPI backend and Google Cloud for data storage and message processing.

## Features

1. **PostgreSQL Interaction:** Retrieve user data from a PostgreSQL database.
2. **BigQuery Integration:** Fetch data from and post data to BigQuery for structured and scalable storage.
3. **Google Pub/Sub Messaging:** Utilize Pub/Sub for asynchronous communication by publishing and receiving messages.

## Project Structure

- **Main File (testtest.py):** The main FastAPI application handling database queries, BigQuery operations, and Pub/Sub messaging.
- **Requirements.txt:** Lists all Python dependencies for the project.
- **Dockerfile:** Configures the Docker image to run the FastAPI application.
- **CircleCI Configuration (config.yaml):** Defines the CircleCI workflow for building and testing the application.

## Setup and Configuration

1. **Database Configuration:** Configure PostgreSQL connection parameters in the `get_db` function.
2. **Google Cloud Credentials:** Replace the placeholder JSON file (`COPY YOUR_CREDENTIALS_FILE.json /app/credentials/`) with your Google Cloud service account credentials.
3. **BigQuery Dataset:** Create a BigQuery dataset named `COPY YOUR_CREDENTIALS_OF_DATASET`.
4. **Pub/Sub Topic and Subscription:** Modify topic and subscription names in the `topic_path` and `subscription_path` variables.

## Endpoints

- **GET /api/test:** Retrieve user data from PostgreSQL.
- **GET /bigquery_data:** Fetch data from BigQuery.
- **POST /post_to_bigquery:** Post data to BigQuery.
- **POST /publish_message:** Publish a message to a Pub/Sub topic.
- **POST /receive_message:** Receive messages from a Pub/Sub subscription.

## Deployment

1. **Google Cloud Deployment:** Deploy the FastAPI application to a Google Cloud Compute Engine or Cloud Run instance.
2. **Docker Image:** Build and deploy the application using the Docker image (`mydock_image`).

## Continuous Integration

- **CircleCI Workflow:** The CircleCI configuration ensures the build and deployment processes are seamless.

## Technologies Used

- **FastAPI:** The high-performance web framework for building APIs.
- **Google Cloud Services:**
  - **BigQuery:** For storing and retrieving structured data.
  - **Pub/Sub:** For asynchronous messaging between components.
- **Docker:** Containerization for easy deployment and scalability.

Feel free to customize this documentation based on your specific project details and additional features.
