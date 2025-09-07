# Setup
### Assumptions
The following assumptions are made for the setup of the application:
1. Python 3.10 or higher is installed on the system.
2. Postgres is installed on the system.

### Steps:
Follow the following steps for setting up and running the application:
1. Clone the repository:
```bash
git clone https://github.com/Rutvik-Trivedi/knowledge-llm.git
```
2. Navigate to the cloned repository:
```bash
cd knowledge-llm
```
3. Install requirements
```bash
pip install -r requirements.txt
```
4. Run the DB setup script
```bash
sudo su postgres -c psql < scripts/db_setup.sql
```
In case this results in an error, try running each line of the file manually separately after running `psql`
5. Run the DB setup
```bash
./manage.py migrate
```
6. Run the server
```bash
./manage.py runserver 0.0.0.0:8000
```

# Using Docker
### Assumptions
It is assumed that docker is installed in the system to use the app in docker

### Steps
Follow the following steps for setting up and running the application in docker:
1. Pull the latest docker image
```bash
docker pull rutvik04/knowledge-llm:latest
```
2. Run the docker image
```bash
docker run -p 8000:8000 rutvik04/knowledge-llm:latest
```

# API
The API documentation is as follows:

1. Analyse (`/analyse`):
    - Method: POST
    - Description: Analyse the given text and return/save structured information.
    - Parameters (JSON body):
        - text: The text to be analysed.
    - Headers:
        - X-Api-Key: The LLM API key for authentication (Uses OpenRouter here).
    - Returns:
        - title: The title of the text.
        - summary: A brief summary of the text.
        - sentiment: The sentiment of the text.
        - topics: A list of main topics discussed in the text.
        - keywords: A list of important keywords in the text.

2. Search (`/search?topic=<topic>`):
    - Method: GET
    - Description: Search for structured information based on the given topic.
    - Parameters (query parameters):
        - topic: The topic or comma separated list of topics to search for.
    - Returns: A list of structured information objects that match the given topic.


Tech Stack:
- Django: For flexibity creating API as well as managing the database. Easier to integrate frontend.
- PostgreSQL: For storing the structured information.
- Docker: For easy deployment of the application.
The structure of the code is such that the application is easy to understand, modify, maintain and modular which facilitates adding more features with minimal refactor