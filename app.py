import time
import docker
from prometheus_client import start_http_server, Gauge, REGISTRY, CollectorRegistry
import prometheus_client as prom_client

def initialize_docker_client():
    try:
        client = docker.DockerClient(base_url='unix://var/run/docker.sock')
        client.ping()  # Check if the Docker daemon is accessible
        print(f"Connected to Docker daemon at unix://var/run/docker.sock")
        return client
    except docker.errors.DockerException as e:
        print(f"Error connecting to Docker daemon: {e}")
        exit(1)

# Define Prometheus metrics
DOCKER_CONTAINER_STATUS = Gauge('docker_container_status', 'Status of Docker containers', ['container_name'], registry=REGISTRY)

# Function to check and update container statuses
def check_container_status(client):
    while True:
        try:
            containers = client.containers.list(all=True)
            container_names = [container.name for container in containers]

            for container in containers:
                status = 1 if container.status == 'running' else 0
                DOCKER_CONTAINER_STATUS.labels(container.name).set(status)

            # Remove metrics for non-existent containers
            for label in list(DOCKER_CONTAINER_STATUS._metrics.keys()):
                if label[0] not in container_names:
                    DOCKER_CONTAINER_STATUS.remove(label[0])
        except Exception as e:
            print(f"Error checking container status: {e}")
        time.sleep(120) 

if __name__ == '__main__':

    client = initialize_docker_client()

    default_collectors = [
        prom_client.GC_COLLECTOR,
        prom_client.PLATFORM_COLLECTOR,
        prom_client.PROCESS_COLLECTOR
    ]

    for collector in default_collectors:
        try:
            REGISTRY.unregister(collector)
        except KeyError:
            pass

    # Start up the server to expose the metrics
    start_http_server(8123, registry=REGISTRY)

    # Start the container status check
    check_container_status(client)
