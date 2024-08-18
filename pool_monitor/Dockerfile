# Use a base image
FROM alpine:3.14

# Set up the working directory
WORKDIR /usr/src/app

# Copy the add-on files to the container
COPY config/ /etc/pool_monitor/

# Install any dependencies
RUN apk add --no-cache python3 py3-pip

# Copy entry script
COPY pool_monitor.py /usr/src/app/

# Set entrypoint
ENTRYPOINT ["python3", "/usr/src/app/pool_monitor.py"]
