# aipiping-de-exercise

The repo is structured as follows:

- analytics: contains python files for running data cleansing and basic statistics for the Academic Field mapping csv files.
- api: contains python files for the mock api server, serving the linkedin data json file.
- data_pipeline: contains the main ELT Process.
- database: contains Mongodb Document Models, an Initial Load operation (init_load) to initialize the database and collections, a Mongodb Connector, a S3 Connector.
- infra_deployments: contains a Docker Compose file that was used to run the Mongodb Instance.
- persona_mapping: contains a python file to perfom persona mapping, given a lead_id.
- test_data: contains data files, csv and json, for development and testing purposes.
- tests: contains unit tests for all the methods and classes in this repo.
- utils: contains utility functions for this project.
- configs.py: contains configurations for the project.

# Steps to run the application 
1. Using a local deployment of Mongodb, if not, a Docker Compose file is provided in the infra_deployments folder, cd into the infra_deployments folder and run the following command:
```docker-compose up```

2. Install the required packages by running the following command:
```pip install -r requirements.txt```

3. Initialize the database and collections by running the following command:
```python -m database.init_load```

4. Start the API Server (in dev mode) by running the following command:
```fastapi dev api/server.py```

5. Run the ELT Process by running the following command:
```python -m data_pipeline.etl_process```

6. Run the Data Cleaning and Analytics for the Academic Field CSV file by running the following command:
```python -m analytics.analytics```

7. Run the Persona Mapping by running the following command:
```python -m persona_mapping.persona_mapping```

8. Run the tests by running the following command:
```pytest```

# Assumptions
