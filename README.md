# Docker Container Status Exporter

This project is a simple **Prometheus Exporter** to monitor the status of Docker containers and expose their status as metrics.

## 📌 Overview
The application connects to your local Docker daemon and periodically checks the status of all containers. It then exports these statuses as metrics that can be scraped by Prometheus.

## 🔍 Metrics Exposed
The main metric exposed is:

- `docker_container_status{container_name="<name>"}`:
  - `1` if the container is **running**.
  - `0` if the container is **stopped**.

## 📂 Requirements
- Python 3.8+
- Docker Engine (must be running on the same host as this script)
- Prometheus Client Library (`prometheus_client`)
- Docker SDK for Python (`docker`)

## 📦 Installation
1. Clone this repository:
```bash
git clone <repository-url>
cd <repository-directory>
```

2. Create a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```
> **Note:** The `requirements.txt` should contain:
> ```
> docker
> prometheus_client
> ```

## 🚀 Usage
1. Start Docker daemon if not already running.
2. Run the exporter:
```bash
python3 exporter.py
```
3. The metrics will be exposed at:
```
http://localhost:8123/metrics
```

## 🔒 Permissions
Ensure your user has permission to access Docker. Typically, you need to be part of the `docker` group:
```bash
sudo usermod -aG docker $USER
```
Then, restart your session for changes to take effect.

## 📖 Explanation of the Code
1. **Docker Client Initialization:**
   - Establishes connection to the Docker daemon using `docker.DockerClient`.
2. **Metric Definition:**
   - Defines a `Gauge` metric to store container statuses (`1` for running, `0` for stopped).
3. **Status Checker:**
   - Continuously checks containers every `120` seconds.
   - Updates Prometheus metrics accordingly.
4. **Metric Cleanup:**
   - Removes metrics for containers that no longer exist.
5. **Exposing Metrics:**
   - Metrics are exposed via `start_http_server()` on port `8123`.

## 📌 Unregistering Default Collectors
The code removes default collectors (`GC_COLLECTOR`, `PLATFORM_COLLECTOR`, `PROCESS_COLLECTOR`) to reduce noise in metrics and only focus on container statuses.



