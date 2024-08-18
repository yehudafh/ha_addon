# Pool Monitor Add-on for Home Assistant

This add-on allows you to monitor and maintain your pool's chemical levels directly from Home Assistant.

## Configuration

| Option | Description | Default |
|--------|-------------|---------|
| `pool_volume_liters` | The volume of the pool in liters | 10000 |
| `pool_type` | The type of pool (chlorine/salt) | chlorine |

## Installation

1. Copy the `pool_monitor` folder to your Home Assistant `addons` directory.
2. In Home Assistant, navigate to "Supervisor" -> "Add-on store" -> "Add-on Repositories" and add the repository.
3. Find "Pool Monitor" in the add-on store and install it.
4. Configure the add-on via the "Configuration" tab.
5. Start the add-on.

## Usage

The add-on will print the current pool settings and simulate monitoring.

## Author

Your Name
