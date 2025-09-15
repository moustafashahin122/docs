# Docker Essential Commands Guide

This comprehensive guide covers the most important Docker commands you'll need for daily development and container management.

## Table of Contents
1. [Most Used Commands](#most-used-commands)
2. [Docker Basics & Installation](#docker-basics--installation)
3. [Essential Commands](#essential-commands)
4. [Container Management](#container-management)
5. [Image Management](#image-management)
6. [Docker Compose](#docker-compose)
7. [Networking & Volumes](#networking--volumes)
8. [Container Lifecycle Management](#container-lifecycle-management)
9. [Troubleshooting & Debugging](#troubleshooting--debugging)
10. [Best Practices](#best-practices)

---

## Most Used Commands

*This section contains your frequently used Docker commands. Update it periodically as you discover new workflows.*

### to deploy manually

```bash

source  /home/odoo17/odoo-17-custom-addons/app_fiebase_creds.sh

cd  /home/odoo17/odoo-17-custom-addons/staging/epm-betaegypt

git  pull

docker-compose  -f  docker-compose-stage.yml  down && \

docker-compose  -f  docker-compose-stage.yml  up  -d  --build

```
### To upagrade modules man

```bash
docker exec -it my-app-container bash

--gevent-port 8333

python3 /bin/odoo   --stop-after-init -d flow_staging_server -p 8112  -c  /etc/odoo/odoo.conf -u real_estate_inventory  --logfile= 

```

### Daily Workflow Commands
```bash
# Add your most common commands here
# Example commands to get you started:

# Check Docker status
docker --version
docker info

# Show environment variables in compose
docker-compose config

# Options:
  # -a, --attach               Attach STDOUT/STDERR and forward signals
  #     --detach-keys string   Override the key sequence for detaching a container
  # -i, --interactive          Attach container's STDIN
docker start -ia <container_id>


# Open container shell

#### Inside the container shell - process management:

# To upgrade modules form terminal
docker exec -it my-app-container bash
# To list all the processes
ps aux
# or
top
# List processes by name
ps aux | grep <process_name>
# Kill a process by PID
kill <process_id>
# Kill a process by name
pkill <process_name>
# Force kill a process
kill -9 <process_id>


# For non-systemd containers, restart application manually:
# Stop the process and start it again
pkill <process_name> && /path/to/your/application &


show compiled conf
docker-compose -f docker-compose-stage.yml config

logs
docker logs -f odoo


# Check if Docker is installed
docker --version

# Pull an image (e.g., Ubuntu)
docker pull ubuntu

# Run a container (interactive mode)
docker run -it ubuntu bash

# List running containers
docker ps

# List all containers (running + stopped)
docker ps -a

# Stop a running container
docker stop <container_id>

# Remove a container
docker rm <container_id>

# Remove an image
docker rmi <image_id>




### Notes
```bash
Add any notes about your workflow, reminders, or project-specific information:

- Remember to use docker-compose-stage.yml for staging environment
- Odoo container name: odoo
- Common ports: 8080, 3000, 5432
- 
```
---
## Docker Basics & Installation

### What is Docker?
Docker is a containerization platform that allows you to package applications and their dependencies into lightweight, portable containers.

### Check Docker Installation
```bash
# Check if Docker is installed and running
docker --version
docker info

# Test Docker installation
docker run hello-world
```

---

## Essential Commands

### System Information
```bash
# Display Docker system information
docker info

# Show Docker disk usage
docker system df

# Clean up unused resources (images, containers, networks, build cache)
docker system prune

# Clean up everything including volumes (⚠️ Use with caution)
docker system prune -a --volumes
```

### Getting Help
```bash
# General help
docker --help

# Help for specific command
docker run --help
docker build --help
```

---

## Container Management

### Running Containers
```bash
# Run a container (basic)
docker run ubuntu

# Run container interactively with terminal
docker run -it ubuntu bash

# Run container in detached mode (background)
docker run -d nginx

# Run container with custom name
docker run --name my-container nginx

# Run container with port mapping
docker run -p 8080:80 nginx

# Run container with environment variables
docker run -e MYSQL_ROOT_PASSWORD=mypassword mysql

# Run container with volume mount
docker run -v /host/path:/container/path ubuntu

# Run container with automatic removal after exit
docker run --rm ubuntu echo "Hello World"
```

### Container Lifecycle
```bash
# List running containers
docker ps

# List all containers (running + stopped)
docker ps -a

# List only container IDs
docker ps -q

# Start a stopped container
docker start <container_name_or_id>

# Stop a running container
docker stop <container_name_or_id>

# Restart a container
docker restart <container_name_or_id>

# Pause/unpause a container
docker pause <container_name_or_id>
docker unpause <container_name_or_id>

# Kill a container (force stop)
docker kill <container_name_or_id>

# Remove a container
docker rm <container_name_or_id>

# Remove all stopped containers
docker container prune
```

### Interacting with Containers
```bash
# Execute command in running container
docker exec -it <container_name> bash

# Copy files between host and container
docker cp file.txt <container_name>:/path/to/destination
docker cp <container_name>:/path/to/file.txt ./local-file.txt

# View container logs
docker logs <container_name>

# Follow logs in real-time
docker logs -f <container_name>

# Show last 100 lines of logs
docker logs --tail 100 <container_name>

# Inspect container details
docker inspect <container_name>

# Show container resource usage
docker stats

# Show processes running in container
docker top <container_name>
```

---

## Image Management

### Working with Images
```bash
# List local images
docker images
docker image ls

# Pull an image from registry
docker pull ubuntu
docker pull ubuntu:20.04  # specific tag

# Search for images on Docker Hub
docker search nginx

# Remove an image
docker rmi <image_name_or_id>

# Remove unused images
docker image prune

# Remove all unused images (including tagged ones)
docker image prune -a

# Show image history/layers
docker history <image_name>

# Inspect image details
docker inspect <image_name>
```

### Building Images
```bash
# Build image from Dockerfile in current directory
docker build .

# Build image with tag
docker build -t my-app:v1.0 .

# Build image with build arguments
docker build --build-arg VERSION=1.0 -t my-app .

# Build without using cache
docker build --no-cache -t my-app .
```

### Registry Operations
```bash
# Login to Docker registry
docker login

# Tag an image for registry
docker tag my-app:latest username/my-app:latest

# Push image to registry
docker push username/my-app:latest

# Pull image from registry
docker pull username/my-app:latest
```

---

## Docker Compose

### Basic Docker Compose Commands
```bash
# Start services defined in docker-compose.yml
docker-compose up

# Start services in detached mode
docker-compose up -d

# Build and start services
docker-compose up --build

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# View running services
docker-compose ps

# View service logs
docker-compose logs

# Follow logs for specific service
docker-compose logs -f <service_name>

# Execute command in service container
docker-compose exec <service_name> bash

# Scale a service
docker-compose up --scale <service_name>=3

# Show compiled configuration
docker-compose config

# Restart services
docker-compose restart
```

### Docker Compose with Custom Files
```bash
# Use specific compose file
docker-compose -f docker-compose-stage.yml up

# Use multiple compose files
docker-compose -f docker-compose.yml -f docker-compose.override.yml up
```

---

## Networking & Volumes

### Networking
```bash
# List networks
docker network ls

# Create network
docker network create my-network

# Connect container to network
docker network connect my-network <container_name>

# Disconnect container from network
docker network disconnect my-network <container_name>

# Inspect network
docker network inspect my-network

# Remove network
docker network rm my-network
```

### Volumes
```bash
# List volumes
docker volume ls

# Create volume
docker volume create my-volume

# Inspect volume
docker volume inspect my-volume

# Remove volume
docker volume rm my-volume

# Remove unused volumes
docker volume prune

# Run container with named volume
docker run -v my-volume:/data ubuntu
```

---

## Container Lifecycle Management

This comprehensive section covers building, running, shutting down, and restarting containers using both Dockerfiles and Docker Compose, including common problems and solutions.

### Building and Running from Dockerfile

#### Basic Dockerfile Operations
```bash
# Build image from Dockerfile in current directory
docker build -t my-app:latest .

# Build with specific Dockerfile
docker build -f Dockerfile.prod -t my-app:prod .

# Build with build arguments
docker build --build-arg NODE_ENV=production -t my-app .

# Build without cache (clean build)
docker build --no-cache -t my-app .

# Build and run in one command
docker build -t my-app . && docker run -d --name my-container my-app
```

#### Advanced Build Options
```bash
# Build with custom build context
docker build -f /path/to/Dockerfile /path/to/context

# Build with target stage (multi-stage builds)
docker build --target production -t my-app:prod .

# Build with memory and CPU limits
docker build --memory=2g --cpus=2 -t my-app .

# Build with custom network
docker build --network=host -t my-app .

# Build and tag multiple versions
docker build -t my-app:latest -t my-app:v1.0 -t my-app:stable .
```

#### Running Built Containers
```bash
# Run with automatic restart policy
docker run -d --restart=unless-stopped --name my-app my-app:latest

# Run with resource limits
docker run -d --memory=512m --cpus=0.5 --name my-app my-app

# Run with environment file
docker run -d --env-file .env --name my-app my-app

# Run with volume mounts and port mapping
docker run -d \
  --name my-app \
  -p 8080:3000 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/logs:/app/logs \
  my-app:latest

# Run with health check
docker run -d \
  --name my-app \
  --health-cmd="curl -f http://localhost:3000/health || exit 1" \
  --health-interval=30s \
  --health-timeout=10s \
  --health-retries=3 \
  my-app:latest
```

### Docker Compose Lifecycle Management

#### Building and Starting Services
```bash
# Build all services defined in docker-compose.yml
docker-compose build

# Build specific service
docker-compose build web

# Build without cache
docker-compose build --no-cache

# Build with parallel processing
docker-compose build --parallel

# Build and start services
docker-compose up --build

# Start services in background (detached)
docker-compose up -d

# Start specific services only
docker-compose up -d web database

# Start with custom compose file
docker-compose -f docker-compose.prod.yml up -d

# Start with environment variables
ENV=production docker-compose up -d

# Start with scaling
docker-compose up -d --scale web=3 --scale worker=2
```

#### Advanced Compose Operations
```bash
# Force recreate containers
docker-compose up -d --force-recreate

# Recreate only changed services
docker-compose up -d --no-deps web

# Start with timeout
docker-compose up -d --timeout 30

# Start with custom project name
docker-compose -p myproject up -d

# Start services one by one (no parallel)
docker-compose up -d --no-parallel
```

### Shutdown Strategies

#### Graceful Shutdown Methods
```bash
# Stop single container gracefully (SIGTERM then SIGKILL after 10s)
docker stop my-container

# Stop with custom timeout
docker stop -t 30 my-container

# Stop all running containers
docker stop $(docker ps -q)

# Stop Docker Compose services gracefully
docker-compose down

# Stop compose with timeout
docker-compose down -t 30

# Stop specific services only
docker-compose stop web worker
```

#### Force Shutdown Methods
```bash
# Kill container immediately (SIGKILL)
docker kill my-container

# Kill with custom signal
docker kill -s SIGINT my-container

# Kill all running containers
docker kill $(docker ps -q)

# Force stop compose services
docker-compose kill

# Force stop specific services
docker-compose kill web database
```

#### Complete Cleanup Shutdown
```bash
# Stop and remove containers, networks, volumes
docker-compose down -v

# Stop and remove everything including images
docker-compose down --rmi all -v

# Stop and remove orphaned containers
docker-compose down --remove-orphans

# Stop, remove, and clean up everything
docker-compose down -v --rmi all --remove-orphans
```

### Restart Strategies

#### Container Restart Methods
```bash
# Restart single container
docker restart my-container

# Restart with timeout
docker restart -t 30 my-container

# Restart all running containers
docker restart $(docker ps -q)

# Restart stopped container
docker start my-container

# Start container and attach to it
docker start -a my-container

# Start container interactively
docker start -i my-container
```

#### Compose Restart Methods
```bash
# Restart all services
docker-compose restart

# Restart specific services
docker-compose restart web database

# Restart with timeout
docker-compose restart -t 30

# Stop and start (full restart)
docker-compose down && docker-compose up -d

# Recreate and restart specific service
docker-compose up -d --force-recreate web

# Rolling restart (one service at a time)
for service in web worker database; do
  docker-compose restart $service
  sleep 10
done
```

#### Restart Policies
```bash
# Set restart policy when running container
docker run -d --restart=no my-app           # Never restart
docker run -d --restart=on-failure my-app   # Restart on failure
docker run -d --restart=always my-app       # Always restart
docker run -d --restart=unless-stopped my-app # Restart unless manually stopped

# Update restart policy of existing container
docker update --restart=unless-stopped my-container

# Check restart policy
docker inspect my-container --format='{{.HostConfig.RestartPolicy.Name}}'
```

### Common Problems and Solutions

#### Build Problems

**Problem: Build fails with "no space left on device"**
```bash
# Solution: Clean up Docker system
docker system prune -a
docker builder prune -a

# Check disk usage
docker system df
```

**Problem: Build is very slow**
```bash
# Solution: Use .dockerignore file
echo "node_modules" >> .dockerignore
echo "*.log" >> .dockerignore
echo ".git" >> .dockerignore

# Use multi-stage builds
# Use BuildKit for faster builds
DOCKER_BUILDKIT=1 docker build -t my-app .
```

**Problem: Can't find Dockerfile**
```bash
# Solution: Specify Dockerfile path
docker build -f /path/to/Dockerfile .

# Or navigate to correct directory
cd /path/to/project && docker build .
```

#### Runtime Problems

**Problem: Container exits immediately**
```bash
# Debug: Check container logs
docker logs my-container

# Debug: Run container interactively
docker run -it my-app bash

# Debug: Check exit code
docker ps -a --format "table {{.Names}}\t{{.Status}}"
```

**Problem: Port already in use**
```bash
# Solution: Find what's using the port
netstat -tulpn | grep :8080
# or on Windows
netstat -ano | findstr :8080

# Use different port
docker run -p 8081:8080 my-app

# Stop conflicting service
docker stop $(docker ps -q --filter "publish=8080")
```

**Problem: Permission denied errors**
```bash
# Solution: Run as specific user
docker run --user $(id -u):$(id -g) my-app

# Or fix file permissions
docker exec -it my-container chown -R appuser:appuser /app/data
```

#### Compose Problems

**Problem: Services can't communicate**
```bash
# Debug: Check network
docker-compose ps
docker network ls
docker network inspect myproject_default

# Solution: Ensure services are on same network
# Use service names as hostnames in your app
```

**Problem: Volume mount issues**
```bash
# Debug: Check volume mounts
docker-compose exec web ls -la /app/data

# Solution: Fix volume paths in docker-compose.yml
volumes:
  - ./data:/app/data:rw  # Add read-write permission
```

**Problem: Environment variables not working**
```bash
# Debug: Check environment inside container
docker-compose exec web env

# Solution: Use .env file or environment section
environment:
  - NODE_ENV=production
  - DATABASE_URL=${DATABASE_URL}
```

### Debugging Commands and Techniques

#### Container Inspection
```bash
# Get detailed container information
docker inspect my-container

# Check container processes
docker top my-container

# Monitor resource usage
docker stats my-container

# Check container filesystem changes
docker diff my-container

# Export container as tar archive
docker export my-container > container-backup.tar
```

#### Log Analysis
```bash
# View logs with timestamps
docker logs -t my-container

# Follow logs in real-time
docker logs -f --since=10m my-container

# Show last N lines
docker logs --tail=50 my-container

# Compose service logs
docker-compose logs -f web

# All service logs with timestamps
docker-compose logs -t --tail=100
```

#### Network Debugging
```bash
# Test connectivity between containers
docker exec -it web ping database

# Check DNS resolution
docker exec -it web nslookup database

# Inspect network configuration
docker network inspect bridge

# Test external connectivity
docker exec -it web curl -I https://google.com
```

#### Performance Debugging
```bash
# Check resource usage
docker exec -it my-container top
docker exec -it my-container df -h
docker exec -it my-container free -m

# Monitor container events
docker events --filter container=my-container

# Check container limits
docker inspect my-container | grep -A 10 "Memory\|Cpu"
```

### Recovery Procedures

#### Container Recovery
```bash
# Recover from crashed container
docker start my-container
docker logs my-container  # Check what went wrong

# Recover data from stopped container
docker cp my-container:/app/data ./backup/

# Create new container from same image
docker run -d --name my-container-new my-app:latest
```

#### Compose Recovery
```bash
# Recover all services
docker-compose down
docker-compose up -d

# Recover with fresh containers
docker-compose down
docker-compose up -d --force-recreate

# Recover specific service
docker-compose up -d --force-recreate web
```

#### Emergency Procedures
```bash
# Stop all containers (emergency shutdown)
docker stop $(docker ps -q)

# Kill all containers (force shutdown)
docker kill $(docker ps -q)

# Remove all containers (nuclear option)
docker rm -f $(docker ps -aq)

# Complete system reset (⚠️ DANGER: removes everything)
docker system prune -a --volumes
```

---

## Troubleshooting & Debugging

### Container Debugging
```bash
# View container logs with timestamps
docker logs -t <container_name>

# Check container resource usage
docker stats <container_name>

# Inspect container configuration
docker inspect <container_name>

# Check container processes
docker top <container_name>

# Get container IP address
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' <container_name>

# Check port mappings
docker port <container_name>
```

### System Monitoring
```bash
# Monitor all containers resource usage
docker stats

# Show system-wide information
docker system df
docker system info

# Show Docker events in real-time
docker events

# Show events for specific container
docker events --filter container=<container_name>
```

### Common Troubleshooting
```bash
# Remove all stopped containers
docker container prune

# Remove all unused images
docker image prune -a

# Remove all unused volumes
docker volume prune

# Remove all unused networks
docker network prune

# Complete cleanup (⚠️ removes everything unused)
docker system prune -a --volumes

# Check if Docker daemon is running
docker version

# Restart Docker daemon (Linux)
sudo systemctl restart docker

# View Docker daemon logs (Linux)
sudo journalctl -u docker.service
```

---

## Best Practices

### Security
```bash
# Run containers as non-root user
docker run --user 1000:1000 ubuntu

# Limit container resources
docker run --memory=512m --cpus=0.5 ubuntu

# Use read-only containers when possible
docker run --read-only ubuntu

# Don't expose unnecessary ports
docker run -p 127.0.0.1:8080:80 nginx  # Bind to localhost only
```

### Performance
```bash
# Use multi-stage builds for smaller images
# Use .dockerignore to exclude unnecessary files
# Clean up package managers in same RUN command
# Use specific image tags, not 'latest'
# Leverage build cache by ordering Dockerfile commands properly
```

### Development Workflow
```bash
# Development with live reload
docker run -v $(pwd):/app -p 3000:3000 node:alpine

# Quick container inspection
docker run --rm -it alpine sh

# Temporary containers for testing
docker run --rm ubuntu echo "test"
```

---

## Quick Reference Cheat Sheet

| Task | Command |
|------|---------|
| Run container | `docker run -it ubuntu bash` |
| List containers | `docker ps -a` |
| Stop container | `docker stop <name>` |
| Remove container | `docker rm <name>` |
| List images | `docker images` |
| Remove image | `docker rmi <name>` |
| View logs | `docker logs -f <name>` |
| Execute in container | `docker exec -it <name> bash` |
| Build image | `docker build -t name .` |
| Clean up system | `docker system prune` |
| Start compose | `docker-compose up -d` |
| Stop compose | `docker-compose down` |

---

## Legacy Commands (for reference)

```bash
# Your existing commands
show compiled conf
docker-compose -f docker-compose-stage.yml config

logs
docker logs -f odoo
```

