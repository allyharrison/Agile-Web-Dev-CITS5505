# Tests

This directory contains the test files for the project.

## Test Files

-   `test_app.py`: This file contains the unit tests for the application.
-   `test_selenium.py`: This file contains the Selenium tests for the application.

## Running the Tests

Before running the tests, ensure you have the server running in the background, as well as the elasticsearch Docker container (see root README for instructions)

### Unit Tests

To run the unit tests, use the following command:

```sh
python3 -m unittest test_app.py
```

### Selenium Tests

To run the unit tests, use the following command:

```sh
python3 ./test_selenium.py
```
