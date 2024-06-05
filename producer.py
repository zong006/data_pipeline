import yaml
import requests
import json
import time
import logging
from kafka import KafkaProducer 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

with open('secrets.yml', 'r') as f:
    config = yaml.safe_load(f)

url = "https://randomuser.me/api/?results=1" 
topic = 'random_names' 

def get_response_dict(url: str) -> dict:
    """
    Creates the results JSON from the random user API call
    """
    response = requests.get(url)
    data = response.json()
    results = data["results"][0]

    return results

def get_json(results: dict) -> dict:
    """
    Creates the final JSON to be sent to Kafka topic only with necessary keys
    """
    kafka_data = {}

    kafka_data["full_name"] = f"{results['name']['title']}. {results['name']['first']} {results['name']['last']}"
    kafka_data["gender"] = results["gender"]
    kafka_data["location"] = f"{results['location']['street']['number']}, {results['location']['street']['name']}"
    kafka_data["city"] = results['location']['city']
    kafka_data["country"] = results['location']['country']

    try:
        kafka_data["postcode"] = int(results['location']['postcode'])
    except ValueError:
        kafka_data["postcode"] = "NaN"

    kafka_data["latitude"] = float(results['location']['coordinates']['latitude'])
    kafka_data["longitude"] = float(results['location']['coordinates']['longitude'])
    kafka_data["email"] = results["email"]

    return kafka_data

def create_kafkaProducer():
    """
    create a kafka producer and connect to cluster in upstash.
    """
    producer = KafkaProducer(
        bootstrap_servers = config['upstash_info']['bootstrap_server'],
        sasl_mechanism = 'SCRAM-SHA-256',
        security_protocol = 'SASL_SSL',
        sasl_plain_username = config['upstash_info']['sasl_plain_username'],
        sasl_plain_password = config['upstash_info']['sasl_plain_password']
        )
    return producer

def push_data():
    """
    Writes the API data every 5 seconds to Kafka topic "random_names"
    """
    logger.info("Starting data pushing to Kafka...")

    producer = create_kafkaProducer()
      

    end_time = time.time() + 60 
    while True:
        if time.time() > end_time:
            break

        try:
            results = get_response_dict(url=url)
            kafka_data = get_json(results=results)  
            logger.info("Sending data to Kafka...")

            producer.send(topic, json.dumps(kafka_data).encode('utf-8'))
            
            time.sleep(5)

        except Exception as e:
            logger.error(f"Error sending data to Kafka: {e}")
    
    producer.close()
    logger.info("Data pushing completed.")

push_data()


