# aipiping-de-exercise

# Project Structure
The repo is structured as follows:
1. **analytics**: Contains the python files for running data cleansing and basic statistics for the Academic Field mapping csv files.
2. **api**: Contains the python files for the mock api server, serving the linkedin data json file.
3. **data_pipeline**: Contains the main ELT Process.
4. **database**: Contains Mongodb Document Models, an Initial Load operation (init_load) to initialize the database and collections, a Mongodb Connector, a S3 Connector.
5. **infra_deployments**: Contains a Docker Compose file that was used to run the Mongodb Instance.
6. **persona_mapping**: Contains a python file to perfom persona mapping, given a lead_id.
7. **test_data**: Contains data files, csv and json, for development and testing purposes.
8. **tests**: Contains unit tests for all the methods and classes in this repo.
9. **utils**: Contains utility functions for this project.
10. **configs.py**: Contains configurations for the project.
# Steps to run the application

1. Using a local deployment of Mongodb, if not, a Docker Compose file is provided in the infra_deployments folder, cd into the infra_deployments folder and run the following command:
   ``docker-compose up``
2. Install the required packages by running the following command:
   ``pip install -r requirements.txt``
3. Initialize the database and collections by running the following command:
   ``python -m database.init_load``
4. Start the API Server (in dev mode) by running the following command:
   ``fastapi dev api/server.py``
5. Run the ELT Process by running the following command:
   ``python -m data_pipeline.etl_process``
   The **etl_process** module will extract the data from the mock api server, load the data into the MongoDB database, and load the data into a raw json file in S3.
6. Run the Data Cleaning and Analytics for the Academic Field CSV file by running the following command:
   ``python -m analytic.field_analysis``
   The **field_analysis** module will clean the data, and provide basic statistics for the Academic Field Mapping CSV file.
7. Run the Persona Mapping by running the following command:
   ``python -m persona_mapping.persona_mapper``
   The **persona_mapper** takes a lead_id as an argument, and returns the persona mapping for that lead_id.
8. Run the tests by running the following command:
   ``pytest``

# Technical Details
### Database Connection
Directory **database** contains the following files:
- Database connection to MongoDB is initialized using Beanie.
- Database connectors are defined to interact with the MongoDB database and S3. Having them as separate methods allows for easy testing and maintenance.
- MongoDB data extractions in this project are done using **Projection** to only get the required data fields, without pulling all the document details.

### Data Pipeline
The overall flow of the data pipeline is as follows:

1. Extract data from the LinkedIn JSON file, via the mock api endpoint **get_linkedin_data(email: str)**.
2. Load the data into the MongoDB database, and a raw json file in S3.
3. Extract the relevant data from the raw MongoDB collection, named *linkedin_data*, using *projection* to only extract the required data to form a **Lead** document.
4. Load the *Lead* document into the MongoDB collection, named *leads*.

## Persona Mapping
The persona mapping is done by using the **Lead** document, and the **Academic Field** document. The persona mapping is done by using the following rules:

1. Given a *lead_id*, get the *linkedin_id* lead document from the MongoDB collection.
2. From the *linkedin_id* document, get the raw document stored in collection *linkedin_data*.
3. From the raw document, we can get the corresponding academic field (default to the latest education) and the company's employee count.
4. Perform mapping based on the academic field and the company's employee count.
5. Return the persona mapping for the given *lead_id*, insert the persona mapping into the MongoDB collection, named *personas*.

### Persona Finder given a Lead ID
The persona finder is implemented in the **persona_finder** module. The module takes a *lead_id* as an argument, and returns the persona mapping for that *lead_id*.

### Analytic
The **field_analysis** module provides data cleaning and basic statistics for the Academic Field Mapping CSV file. The module cleans the data, and provides basic statistics such as the number of unique fields.

### API Server
The API Server is implemented using FastAPI. The API Server serves the LinkedIn data JSON file, and provides an endpoint to get the LinkedIn data given an email.

### Testing
The **tests** directory contains unit tests for all the methods and classes in this repo. The tests are implemented using pytest and unittest.

# Rationale for the Technical choices, and future improvements
1. CSV Files: The Field of Study file is clean fairly easily, I perfromed some basic. manual mapping for the missing *levels* and *level name*, and then I drop all the null records. This is by far not the best way if we want the best result, however, in my opinion, it is the fastest way to get a clean dataset.
--> Future Improvements: We can use a more sophisticated method to clean the data, such as using a machine learning model to predict the missing values. In the *test_data* folder, there is a file called *academic_field_filled.csv*, which is filled using **Generative AI**. It is fast, and quite accurate, so I think this can be a good way moving forward.

2. ELT Process: The ELT Process is implemented with a *stateless* approach, with the idea that every the ELT Process can be triggered with an event, in this case it is the API Call to get the Linkedin data. In my opinion, stateless pipelines are generally easier to scaled, and maintain.

3. S3: I chose S3 instead of Grid FS because I have more experience with S3, and I think it is easier to use. However, Grid FS is a good choice if we want to store large files in MongoDB and deep integration with MongoDB.

# Persona Mapping and Data Model considerations
1. The Persona data model is implemented with a few fields, and in the future, when the number of features grow, in my navie opinion, we can simply add more fields to the Persona document, or we can use an embedded approach, where we keep a certain number of fixed fields and the fields that keep growing can be embedded, thus reducing the needs to adjust the document model.

2. In the current Persona document model, I am implemening the *lead_ids* as list, and we can keep growing the list, however, in the future, if the list grows too large, we can consider using an another collection to specifically store the reference to the *lead_ids*.

