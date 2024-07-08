# FastAPI Web Application

This is a web application developed using FastAPI, with MySQL as a Database.

## Project Structure

The project is organized as follows:

- **api**: Contains FastAPI routes organized into separate modules for different functionalities.
- **config**: Holds configuration settings for the application, particularly related to the database.
- **crud**: Contains modules responsible for CRUD operations on database entities.
- **models**: Defines SQLAlchemy models representing the database schema.
- **schemas**: Contains Pydantic models for request and response validation.
- **utils**: Holds utility functions, particularly related to authentication.

## MVC Design Pattern

The project follows the MVC (Model-View-Controller) design pattern:

- **Models (M)**: SQLAlchemy models in the `models` directory represent the data schema.
- **Views (V)**: FastAPI route functions in the `api/routes` directory serve as views, handling incoming requests and returning responses.
- **Controllers (C)**: Business logic is distributed across various modules, including the `crud` directory, which handles interactions between views and models.

## Installation and Setup

1. Clone the repository:
    ```bash
    git clone <repository_url>
    ```

2. Navigate to the project directory:
    ```bash
    cd <project_directory>
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up the database configuration:
    - Edit the `config/database.py` file to configure your MySQL database connection.

5. Run the application:
    - In Development Mode:
        ```bash
        fastapi dev app/main.py
        ```
    - In Production Mode
         ```bash
        fastapi run main.py
        ```
