# pjatk_bgd

This project is a data processing pipeline for managing user and order data. It uses Python, PostgreSQL, and Docker to load, process, and store data from CSV files into a relational database. The project is designed for educational purposes as part of a lab at PJATK.

## Features

- Reads user and order data from CSV files.
- Merges and processes the data using pandas.
- Stores the data in a PostgreSQL database using SQLAlchemy.
- Supports bulk insertion of data for efficiency.
- Fully containerized using Docker and Docker Compose.

## Prerequisites

- Python 3.12
- Docker and Docker Compose
- Fedora 41 (tested environment)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd pjatk_bgd
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the `.env` file:
   Create a `.env` file in the root directory with the following structure. **Keep this file secret and do not share it publicly.**
   ```
   DB_USERNAME=<your_database_username>
   DB_PASSWORD=<your_database_password>
   DB_HOST=<your_database_host>
   DB_NAME=<your_database_name>
   DB_PORT=<your_database_port>
   ```

4. Build and start the Docker containers:
   ```bash
   docker-compose up --build
   ```

## Usage

1. Place your user and order CSV files in the appropriate directories:
   - User data: `data/users/`
   - Order data: `data/orders/`

2. Run the application:
   The application will automatically process the data and insert it into the PostgreSQL database when the container starts.

3. Access the PostgreSQL database:
   The database is exposed on port `5432`. You can connect using any PostgreSQL client with the credentials specified in the `.env` file.

## Project Structure

- `__main__.py`: Entry point for the application.
- `python/read.py`: Functions for reading and merging CSV files.
- `python/postgres.py`: Database models and utility functions for interacting with PostgreSQL.
- `data/`: Directory containing user and order CSV files.
- `docker-compose.yml`: Docker Compose configuration.
- `Dockerfile`: Docker image definition.

## Environment Information

- Python dependencies are listed in `requirements.txt`.
- The project uses the following key libraries:
  - `pandas` for data processing.
  - `SQLAlchemy` for database interaction.
  - `psycopg2-binary` for PostgreSQL connection.

## Testing

The project was tested on Fedora 41 with Python 3.12. Ensure your environment matches these specifications for optimal performance.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
