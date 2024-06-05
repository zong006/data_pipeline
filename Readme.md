# Simulation of Real-Time Data Pipeline

This project implements a real-time data pipeline for streaming data from an API to Kafka, processing it with Spark Streaming, and persisting it to PostgreSQL.

## Components

### 1. API Data Source
The data is fetched from the [Random User Generator API](https://randomuser.me/api/?results=1), which provides random user data in JSON format.

### 2. Kafka Cluster
Kafka acts as the message broker for the data pipeline. The Kafka cluster is hosted on [Upstash](https://upstash.com/), providing a scalable and reliable platform for handling streaming data.

### 3. Kafka Producer
The Kafka Producer component fetches data from the API and publishes it as messages to a Kafka topic. Each message represents a single user record obtained from the API.

### 4. Spark Streaming Consumer
Spark Streaming consumes messages from the Kafka topic and processes them in real-time. Spark provides powerful tools for data manipulation, analytics, and machine learning, making it suitable for processing large volumes of streaming data efficiently.

### 5. PostgreSQL Database
PostgreSQL is used to simulate data persistence. Spark writes the processed data to PostgreSQL tables, where it can be queried, analyzed, and used for various applications. In this project, PostgreSQL is run as a Docker container.

## Usage
To run the data pipeline, follow these steps:

1. Set up the Kafka cluster on Upstash.
2. Run the PostgreSQL Docker container.
3. Execute the Kafka Producer script to fetch data from the API and publish it to the Kafka topic.
4. Run the Spark Streaming application to consume messages from the Kafka topic, process them, and write the results to PostgreSQL.

## Requirements
See requirements.txt

