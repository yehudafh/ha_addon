import json

# Load the configuration from the JSON file
with open('/etc/pool_monitor/config.json', 'r') as f:
    config = json.load(f)

# Example of using the configuration values
pool_volume = config.get('pool_volume_liters', 10000)
pool_type = config.get('pool_type', 'chlorine')

print(f"Monitoring pool with volume {pool_volume} liters, type: {pool_type}")
