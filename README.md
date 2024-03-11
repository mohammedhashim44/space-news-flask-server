# Space Flight News Articles Data Pipeline

This repository contains a data pipeline that fetches articles from the SpaceFlight News API and stores them in a SQLite database. It also includes a Flask server that serves the data from the database as a JSON API.

## Prerequisites

- Python 3.x
- pip (Python package installer)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/mohammedhashim44/space-news-flask-server.git
```

2. Navigate to the project directory:

```bash
cd space-news-flask-server
```

3. Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Usage

### Fetch and Store Data

To fetch and store articles from the SpaceFlight News API, run the following command:

```bash
python fetch_data.py
```

This will fetch the latest articles published since yesterday and store them in the SQLite database (`database.db`).

You can also specify a custom date to fetch articles from by using the `--date` argument:

```bash
python fetch_data.py --date dd-mm-yyyy
```

Replace `dd-mm-yyyy` with the desired date in the format `day-month-year` (e.g., `09-02-2023`).

### Run the Flask Server

To run the Flask server and serve the data from the SQLite database as a JSON API, run the following command:

```bash
python server.py
```

The server will start running on `http://localhost:5000`. You can access the JSON data by visiting `http://localhost:5000/api/data` in your web browser or making a GET request to that URL.

## Configuration

You can configure the following settings in the `config.py` file:

- `SQLITE_FILE`: The name of the SQLite database file (default: `database.db`).
- `ACTION_IF_DATA_EXIST`: The action to take if the table already exists in the database. Set to `"replace"` to overwrite the existing data or `"append"` to append new data (default: `"replace"`).
- `TABLE_NAME`: The name of the table in the SQLite database where the articles are stored (default: `articles`).
