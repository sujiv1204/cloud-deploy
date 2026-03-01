# cloud-deploy

A Flask-based web application designed to simulate heavy CPU workloads for cloud infrastructure testing and benchmarking. This project demonstrates CPU-intensive operations through 2D image convolution processing and serves as a practical implementation of cloud computing concepts including auto-scaling, load balancing, and security best practices on Google Cloud Platform (GCP).

## Assignment Overview

This project was developed as part of a cloud computing assignment focused on:

- **VM Deployment**: Creation and configuration of virtual machine instances on Google Cloud Platform
- **Auto-Scaling Implementation**: Dynamic resource provisioning based on CPU utilization metrics
- **Security Measures**: Implementation of IAM roles for access control and firewall rules for network security
- **Load Balancing**: Distribution of traffic across multiple instances with health monitoring

### Assignment Objectives Accomplished

**VM Instance Creation**: Deployed e2-micro instances on GCP using instance templates for consistency

**Auto-Scaling Policies**: Configured Managed Instance Group with:

- CPU-based scaling (60% threshold)
- Instance range: 1 (min) to 5 (max)
- 120-second initialization period

**IAM Security**:

- Created secondary auditor account with read-only roles
- Enforced Principle of Least Privilege
- Roles: Compute Viewer, Monitoring Viewer, Compute Instances Viewer

**Firewall Configuration**:

- `allow-webapp-traffic`: Public HTTP access (0.0.0.0/0 → TCP:80)
- `allow-ssh-iap`: Secure SSH via Identity-Aware Proxy
- `allow-lb-healthcheck`: Load balancer health monitoring

**Load Balancing**: Global HTTP(S) Load Balancer with backend health checks

## Project Structure

```
cloud-deply/
├── app.py                                    # Main Flask application
├── startup.sh                                # Cloud VM deployment script
├── .gitignore                                # Git ignore configuration
├── oha.log                                   # Load testing results
├── architechtural_diagram.png                # System architecture diagram
├── M25CSE011_VCC_Assignment2_report.pdf      # Project documentation
```

### File Descriptions

#### `app.py`

The core Flask application that provides two endpoints:

- **`/`** - Health check endpoint returning server status
- **`/process-image`** - CPU-intensive endpoint simulating 2D convolution on a 600x600 pixel image with a 3x3 kernel

The application uses nested loops (O(N² × K²) complexity) to intentionally maximize CPU utilization for stress testing. It runs on port 80 with threading enabled to handle concurrent requests.

#### `startup.sh`

Automated deployment script for cloud virtual machines (e.g., Google Compute Engine). This bash script:

- Updates the system and installs Python 3, pip, and Git
- Clones the repository to `/opt/webapp`
- Creates a Python virtual environment
- Installs Flask dependencies
- Starts the application in the background with logging to `webapp.log`

Use this script as a startup/user-data script when provisioning cloud VMs for automated deployment.

#### `.gitignore`

Excludes the `venv/` directory from version control to prevent committing large virtual environment files.

#### `oha.log`

Contains load testing results from the `oha` tool (a modern HTTP load testing tool written in Rust). The log shows:

- **Test parameters:** 60-second duration, 50 concurrent connections
- **Performance metrics:** ~2.15 requests/sec, average response time of 2.95 seconds
- **Success rate:** 100% for completed requests
- **Target:** Deployed instance at `34.120.3.231/process-image`

This demonstrates the application's behavior under sustained load on a cloud deployment.

#### `architechtural_diagram.png`

Visual representation of the system architecture, showing the deployment topology, components, and data flow.

#### `M25CSE011_VCC_Assignment2_report.pdf`

Comprehensive project report documenting the assignment objectives, implementation details, testing methodology, and results analysis.

## GCP Infrastructure Configuration

This project implements a complete cloud architecture on Google Cloud Platform with auto-scaling, load balancing, and security hardening.

### Infrastructure Components

| Component Category           | Resource Name             | Key Configurations & Parameters                                       | Primary Purpose                                                               |
| ---------------------------- | ------------------------- | --------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| **Application Logic**        | `app.py`                  | Python 3, Flask framework, Port 80                                    | Executes $O(N^2 \cdot K^2)$ 2D image convolution to simulate high CPU load    |
| **Automation**               | `startup.sh`              | Bash script, apt-get, git clone, nohup                                | Automates immutable VM provisioning, dependency installation, and server boot |
| **IAM Security**             | Secondary Auditor Account | Roles: Compute Viewer, Monitoring Viewer, Compute Instances Viewer    | Enforces the Principle of Least Privilege for infrastructure auditing         |
| **VPC Firewall**             | `allow-webapp-traffic`    | Ingress, TCP: 80, Source: 0.0.0.0/0, Target Tag: web-server           | Permits global HTTP traffic to reach the web instances                        |
| **VPC Firewall**             | `allow-ssh-iap`           | Ingress, TCP: 22, Source: 35.235.240.0/20, Target Tag: web-server     | Secures administrative SSH access via Google's Identity-Aware Proxy           |
| **VPC Firewall**             | `allow-lb-healthcheck`    | Ingress, TCP: 80, Source: 130.211.0.0/22, 35.191.0.0/16               | Allows the Global Load Balancer to ping backend VMs to verify health          |
| **Compute Blueprint**        | `webapp-template`         | Machine Type: e2-micro, Network Tag: web-server, Metadata: startup.sh | Defines the exact hardware and software state for newly provisioned nodes     |
| **Auto-Scaling Engine**      | `webapp-autoscaler-group` | Min: 1, Max: 5, Target CPU: 60%, Initialization: 120s                 | Dynamically provisions or terminates VMs based on real-time CPU telemetry     |
| **Load Balancer (Backend)**  | `webapp-backend`          | Protocol: HTTP, Backend Type: Instance Group, Timeout: 120s           | Distributes traffic to the MIG; extended timeout prevents 502 Gateway errors  |
| **Load Balancer (Health)**   | `webapp-health-check`     | Protocol: HTTP, Port: 80                                              | Continuously polls instances to ensure traffic is only routed to healthy VMs  |
| **Load Balancer (Frontend)** | `webapp-frontend`         | IP Version: IPv4 (Ephemeral), Port: 80                                | Provides the single, global entry point (Public IP) for the application       |

### Architecture Highlights

**Security Implementation:**

- **IAM Roles**: Secondary auditor account with read-only access (Compute Viewer, Monitoring Viewer) following the Principle of Least Privilege
- **Firewall Rules**:
    - Public HTTP access (port 80) restricted to web-server tagged instances
    - SSH access secured through Identity-Aware Proxy (IAP) only
    - Load balancer health check access from Google's IP ranges

**Auto-Scaling Configuration:**

- Minimum instances: 1 (ensures availability)
- Maximum instances: 5 (controls costs)
- Scaling trigger: 60% CPU utilization
- Initialization period: 120 seconds (allows instances to warm up before evaluation)

**Load Balancing:**

- Global HTTP(S) Load Balancer for traffic distribution
- Backend timeout: 120 seconds (accommodates CPU-intensive operations)
- Health checks ensure traffic routing only to healthy instances

## Installation

### Local Setup

1. Clone the repository:

```bash
git clone https://github.com/sujiv1204/cloud-deploy.git
cd cloud-deploy
```

2. Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip3 install Flask
```

4. Run the application:

```bash
python3 app.py
```

The application will be available at `http://localhost:80` (requires sudo/admin privileges) or modify the port in `app.py`.

## API Endpoints

### `GET /`

**Home endpoint** - Health check for the application.

**Response:**

```
Compute Engine is running. Hit /process-image for heavy load.
```

### `GET /process-image`

**CPU-intensive processing endpoint** - Simulates a 2D convolution operation on a 600x600 image using a 3x3 kernel.

**Response:**

```json
{
    "status": "success",
    "message": "2D Image Convolution complete.",
    "pixels_processed": 358404,
    "processing_time_seconds": 12.3456
}
```

**Note:** This endpoint intentionally uses nested loops to maximize CPU utilization for stress testing purposes.

## Usage Examples

### Basic health check:

```bash
curl http://localhost:80/
```

### Trigger CPU-intensive operation:

```bash
curl http://localhost:80/process-image
```

### Load testing with multiple concurrent requests:

```bash
# Using Apache Bench
ab -n 100 -c 10 http://localhost:80/process-image

# Using oha (modern alternative)
oha -n 100 -c 10 http://localhost:80/process-image
```

## Performance Testing Results

The application was load tested on GCP using the `oha` tool against the deployed instance at `34.120.3.231`:

**Test Parameters:**

- Duration: 60 seconds
- Concurrent connections: 50
- Target endpoint: `/process-image`

**Results:**

- **Success Rate**: 100% (for completed requests)
- **Throughput**: ~2.15 requests/sec
- **Average Response Time**: 2.95 seconds
- **Response Time Range**: 1.05s (fastest) to 4.29s (slowest)
- **Total Requests**: 79 successful (50 aborted due to 60s deadline)

**Performance Distribution:**

- 50% of requests completed in ≤ 2.77 seconds
- 90% of requests completed in ≤ 4.06 seconds
- 95% of requests completed in ≤ 4.25 seconds

These results demonstrate the application's consistent performance under sustained load, with the CPU-intensive convolution operations consuming 1-4 seconds per request depending on instance resource availability and concurrent load.

## Technical Details

- **Simulated image size:** 600x600 pixels
- **Convolution kernel:** 3x3 matrix
- **Algorithm complexity:** O(N² × K²)
- **Output pixels:** 358,404 (598 × 598)
- **Server:** Flask development server with threading enabled

## Assignment Information

- **Roll Number**: M25CSE011
- **Course**: Virtual Cloud Computing (VCC)
- **Assignment**: Assignment 2
- **Platform**: Google Cloud Platform (GCP)
- **GitHub Repository**: [sujiv1204/cloud-deploy](https://github.com/sujiv1204/cloud-deploy)
- **Drive**: [Google Drive](https://drive.google.com/drive/folders/1bQuWmw-pZdUvbY0KBw4rxkVnVGdvrs8Z?usp=sharing)
