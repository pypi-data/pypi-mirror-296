from PyJotformAJM.PyJotformAJM import JotForm

# PyJotformAJM

## Overview
This project is a Python-based implementation to handle interactions with the JotForm API. It includes functions for client initialization, validation, and error handling to ensure smooth data operations. The package is designed to streamline the process of interfacing with JotForm for data submission and retrieval tasks.

## Features
- **Client Initialization**: Ensures the JotForm client is properly initialized for API interactions.
- **Validation**: Validates the client to check for a valid session or API token.
- **Error Handling**: Custom exceptions for handling authentication errors and client issues.
- **Submission Handling**: Properties and methods to manage and check for new entries and submission IDs.

## Installation
Make sure you have [Python 3.12.2](https://www.python.org/downloads/release/python-3122/) installed. Then install required packages using pip.
```bash
pip install -r requirements.txt
```

## Usage
Here is an example of how you can use the provided functionalities:

### Initialization
```python
# Ensure the client is properly initialized
JotForm._initialize_client()
```

### Validation
```python
# Validate the client session 
if has_valid_client:
    print("Client is valid.")
else:
    print("Invalid client.")
```

### Check for New Entries
```python
# Check if there are new entries
if has_new_entries:
    print("There are new entries.")
else:
    print("No new entries at the moment.")
```

### Retrieve Last Submission ID
```python
# Get the last submission ID
last_id = last_submission_id
print(f"Last submission ID: {last_id}")
```

## Error Handling
The project defines custom exceptions for handling different types of errors:
- `NoJotformClientError`: Raised when the client is not properly initialized.
- `JotFormAuthenticationError`: Inherits from `HTTPError` and is raised for authentication-related errors.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your changes. Ensure your code follows the project's coding standards and includes relevant tests.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.