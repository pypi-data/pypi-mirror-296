<p align="center">
  <img src="./assets/jsonkit_logo.png" alt="JSONKit Logo"/>
</p>
<hr>
<h4 align="center">🚀 <i>Your toolkit for seamless JSON handling.</i></h4>

<p align="center">
  <a href="#️overview">Overview</a> •
  <a href="#features">Features</a> •
  <a href="#installation">Installation</a> •
  <a href="#usage">Usage</a> •
  <a href="#license">License</a> •
  <a href="#contributing">Contributing</a>
</p>

# Overview

JSONKit is a Python Library for enhanced JSON file handling with support for `datetime` and `UUID` objects. It provides both `synchronous` and `asynchronous` file operations.

## Features

- **Synchronous Operations**: Read and write JSON files with custom encoding and decoding for `datetime` and `UUID` objects.
- **Asynchronous Operations**: Handle JSON files asynchronously using `aiofiles`.
- **Custom Serialization**: Special handling for `datetime` and `UUID` types.

## Installation

You can install JSONKit via pip:

```bash
pip install ayrun-jsonkit
```

## Usage

#### Synchronous Usage:

```python
from jsonkit import JSONFile
from datetime import datetime
import uuid

# Initialize the JSONFile object
json_file = JSONFile('example.json')

# Write data to the file
data = {
    "name": "Alice",
    "age": 30,
    "created_at": datetime.now(),
    "id": uuid.uuid4()
}

# The 'write' function automatically returns the loaded data. So you can either choose to do this:
loaded_data = json_file.write(data, indent=4)
print(loaded_data)

# Or:
json_file.write(data, indent=4)
loaded_data = json_file.load()
print(loaded_data)
```

#### Asynchronous Usage:

```python
from jsonkit import AsyncJSONFile
from datetime import datetime
import uuid
import asyncio

async def main():
    # Initialize the AsyncJSONFile object
    async_json_file = AsyncJsonFile('data.json')

    # Write data to the file
    data = {
        "name": "Bob",
        "age": 25,
        "created_at": datetime.now(),
        "id": uuid.uuid4()
    }

    # The 'write' function automatically returns the loaded data. So you can either choose to do this:
    loaded_data = await async_json_file.write(data, indent=4)
    print(loaded_data)

    # Or:
    await async_json_file.write(data, indent=4)
    loaded_data = await async_json_file.load()
    print(loaded_data)

# Run the async main function
asyncio.run(main())
```

## License

JSONKit is licensed under the MIT License. See the [LICENSE](./LICENSE) file for more details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.
