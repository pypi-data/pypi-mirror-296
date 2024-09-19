# pyfris

pyfris is a Python API that allows you to interact with the SOAP API server of the Flanders Research Information Space (FRIS).

## Installation

You can install pyfris using pip:

```
pip install pyfris
```

## Requirements

- Python 3.8 or higher
- Required packages: requests, bs4

## Usage

Here's a quick example of how to use pyfris:

```python
from pyfris.fris_api import FRIS_API

# Create an instance of the FRIS_API
fris = FRIS_API()

# Search for projects
projects = fris.search_projects("protein", 10)
print(projects)

# Search for publications
publications = fris.search_pubs("protein", 10)
print(publications)

# Get project details
project_id = list(projects.keys())[1]
project_details = fris.get_project(project_id)
print(project_details)

# Get publication IDs for a project
pub_ids = fris.get_pub_ids(project_id)
print(pub_ids)

# Get publication details
publication_details = fris.get_publication(pub_ids[0])
print(publication_details)

# Create a second instance of the FRIS_API
# to see if the VODS data is already cached
fris2 = FRIS_API()
```

## Features

- Search for projects and publications
- Retrieve detailed information about projects and publications
- Get publication IDs associated with a project
- Pretty print XML responses

## API Reference

### FRIS_API

The main class for interacting with the FRIS API.

#### Methods

- `search_projects(query: str, n: int = 10, verbose: bool = False)`: Search for projects given a query.
- `search_pubs(query: str, n: int = 10, verbose: bool = False)`: Search for publications given a query.
- `get_pub_ids(uuid: str, verbose: bool = False)`: Retrieve all publication IDs for a project given its UUID.
- `get_project(uuid: str, verbose: bool = False)`: Retrieve project information given its UUID.
- `get_publication(pub_id: str, verbose: bool=False)`: Retrieve publication information given its ID.
- `ppxml(xml)`: Pretty print XML responses. Only used when verbose=True. Example output snippet below.

![snippet](pretty_print_xml.png?raw=true "Pretty Print XML")

## Testing

To run the tests, use the following command:

```
python -m unittest -v tests/test_fris_api.py
```

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Authors

- H. Görkem Uyanık

## Acknowledgements

This package interacts with the Flanders Research Information Space (FRIS) API. We thank FRIS for providing access to their research information system.