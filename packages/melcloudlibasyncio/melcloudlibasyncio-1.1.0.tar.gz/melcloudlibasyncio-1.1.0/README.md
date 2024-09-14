# Project Name: asyncio-melcloud-lib

## Description:
This project is a Python library that provides an asynchronous interface for interacting with the MelCloud API. It allows users to control and monitor Mitsubishi Electric air conditioning units remotely using asyncio.

## Features:
- Asynchronous API calls for improved performance and responsiveness.
- Support for authentication and authorization with the MelCloud API.
- Ability to control and monitor multiple air conditioning units.
- Comprehensive documentation and examples for easy integration.

## Installation:
To install the asyncio-melcloud-lib library, simply run the following command:

```
pip install melcloudlibasyncio
```

## Usage:
To get started with the asyncio-melcloud-lib library, import it into your Python project:

```python
import melcloudlibasyncio
```

Then, create an instance of the `MelCloudClient` class and authenticate with your MelCloud credentials:

```python
client = melcloudlibasyncio.MelCloudClient(username='your_username', password='your_password')
await client.login()
```

Once authenticated, you can use the various methods provided by the library to control and monitor your air conditioning units.

## Examples:
Here are a few examples to help you get started:

- Get a list of all available devices:

```python
devices = await client.get_devices()
```

- Set the temperature of a specific device:

```python
await client.set_temp(device_id='device_id', temperature=22)
```

- Example of complete code (Login and turns off the device):

```python
import asyncio
from lib.melcloud.devices import Device
from lib.melcloud.melcloudclient import MelcloudClient
from lib.melcloud.jsongenerator import OperationMode
import logging

basicConfig = logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


client = MelcloudClient("your_undername", "your_password")

async def main():
    logging.debug(await client.login())
    await client.get_devices()
    await client.set_device_settings()
    for device in client.devices:
       await client.change_power_state(device.device_id, "true") # <---- set this to false to turn off the device
    await client.close()

if __name__ == "__main__":
    asyncio.run(main())
```

For more examples and detailed documentation, please refer to the [official documentation](https://github.com/your_username/asyncio-melcloud-lib).

## Contributing:
Contributions are welcome! If you have any ideas, suggestions, or bug reports, please open an issue or submit a pull request on the [GitHub repository](https://github.com/v0nNemizez/asyncio-melcloud-lib).

## License:
This project is licensed under the MIT License. See the [LICENSE](https://github.com/v0nNemizez/asyncio-melcloud-lib/blob/main/LICENSE) file for more information.