# Wave Challenge App

This repository contains a payroll reporting system that allows you to configure job groups, upload payroll CSV files, and review the uploaded reports through a REST API. The application is containerized using Docker and provides interactive API documentation via Swagger UI.

The challenge is completed using PostgreSQL as a database to store timesheet entries, FastAPI as a backend-server with SQLAlchemy for table models, Pydantic for Schema models and Docker for running the containerized application.

# Prerequisite:
  - Python 3.10+
  - Docker 

Install docker and make sure it is up and running.

## Getting Started

### 1. Clone the Repository

Open a terminal and execute the following commands:

```bash
git clone sivakumar_manoharan.bundle sivakumar_app
cd sivakumar_app
```

### 2. Build and Run the Application

Build and start the application using Docker Compose:
### For  Windows/macOS/Linux
```bash
docker compose up --build
```

### 3. Access the API Documentation

Once the build is complete, open your browser and navigate to:

```
http://localhost:8000/docs
```

This will load the Swagger UI, where you can interact with the API endpoints.

### 4. Closing the container

#### List all containers:
```bash
  docker ps -a
```
### Remove the listed containers one by one:
```bash
  docker rm container_id
```
### List all volumes:

```bash
docker volume ls
```

### Remove the required volume with pg_data
```bash
docker volume rm volume_name
```

# Demo Video 
### [Click here to watch the demo](https://youtu.be/K6Cgkd7NEIE)

## API Usage

### Configure Job Groups

To set up the job groups, use the `/job-group` API endpoint. Send a JSON payload with the required job group details. For example:

```json
{
  "job_group_id": "A",
  "wages": 20
}
```

### Upload Payroll Reports

Upload a payroll CSV file using the POST API endpoint `/payroll-report`. On successful upload, the server returns a **201 Created** response. If you attempt to upload the same file again, the API responds with a **405 Method Not Allowed** error, indicating that the record already exists. If you attempt to upload a file, other than a CSV, then it would throw a **400 Bad Request** exception. If you attempt a file that contains non-configured job groups, it will throw a **405 Method not allowed** exception stating that job group is not configured.

### Check Payroll Reports

To view the payroll reports:

1. Open Swagger UI at `http://localhost:8000/docs`.
2. Locate the **GET /payroll-report** endpoint.
3. Click **Try it out** and then **Execute**.

### Uploading Multiple CSV Files

- You can upload multiple CSV files.
- Ensure that every CSV file uses the same columns.
- If reusing the same file name, change the record number accordingly to avoid duplicate records.

## Implementation Details & Developer Notes

### How did you test that your implementation was correct?

- **Manual Testing via Swagger UI:**  
  Endpoints were manually tested using the interactive Swagger UI at `http://localhost:8000/docs`, ensuring that each endpoint behaved as expected.
- **API Response Verification:**  
  Specific scenarios, such as duplicate CSV uploads returning a **405 Method Not Allowed** and successful uploads returning a **201 Created** response, were verified using test cases and tools like cURL or Postman.

### If this application was destined for a production environment, what would you add or change?

- **Environment Variable Separation:**
  - As it is in a deployment setting and there are no crucial variables configured, those are within the code. But if it is aimed to get deployed in a production setting, hiding secret details is crucial.
  - Hence, I would hide the most secret variables such as connection strings, API token passwords etc. in a separate .env file and configure those environment variables in the webapps separately.
- **Security Enhancements:**  
  - While deploying in a production environment, I will add authentication methods to verify such as JWT token verification for individual users that contains persona and access levels of the user.
- **Enhanced Exceptions Handling:**
  -  If it is getting deployed in a production setting, I will add more scenarios such as Column mismatches while uploading CSV files etc.
- **Persistent Data Storage:**  
  - When it comes to production environment, I will implement Redis Caching or any other in-memory storage in order to reduce the time taken for fetching of data using GET API requests.
- **Scalability Improvements:**  
  - Coming to the scalability of the application, I will implement the integration of performance monitoring tools such as Kubernetes, Prometheus etc.
- **CI/CD Pipeline:**  
  -I have already automated the development flow using Docker. But if it is destined to a production setting, I would implement automated testing pipelines using GitHub Actions.
- **Branch Protection:**
  - While coming to a deployment setting, I would definitely implement branching rules and the access levels in a such a way that who should directly merge the main branch and who has the access to merge the Pull Requests raised by the contributors.
- **Comprehensive Documentation:**  
  - When targeting to a production environment, I would strongly adhere in writing a comprehensive documentation with different scenarios and what happens when different types of files are given as inputs.

### What compromises did you have to make as a result of the time constraints of this challenge?

- **Limited Test Coverage:**  
  While core functionalities were tested, the application may lack extensive unit and integration tests that would be expected in a production-grade solution.
- **Basic Error Handling:**  
  Error handling is upto the requirements and could be expanded to provide more detailed diagnostics and resilience.
- **Non-implementation of security measures**  
  The API is not implemented with the security measures such as verification of personas or access levels.
- **Minimal Optimization:**  
  Certain performance optimizations and code refactoring efforts were deferred in favor of delivering a functional minimum viable product.

## Conclusion

This README provides you with the necessary steps to deploy, test, and use the payroll reporting system. The included developer notes offer insights into the testing process, production-readiness enhancements, and compromises made due to time constraints. Feel free to enhance the application further based on your requirements.

