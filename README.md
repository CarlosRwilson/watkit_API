

# Watkit API


This API automates client management by providing automated follow-up triggers and structured data storage for client information. 
It is designed with a clean, layered architecture to ensure maintainability and scalability.


## Tech Stack
**Framework**: *FastAPI* (High performance, easy to use, auto-generated docs).

**ORM**: SQLAlchemy (Robust SQL ORM database management).

**Migrations**: Alembic (Automated database schema management).

**Database**: PostgreSQL (Relational data storage).

**Containerization**: Docker (Ensures a consistent, reproducible environment).

**Asynchrony**: asyncio (Asynchronous programming, optimizing I/O bound tasks).

**Language**: Python 3.13+



### Project Architecture


The application follows a layered design pattern to separate concerns and maintain clean code:

**api & v1 (FastAPI)**: Handles HTTP requests, routing, and response formatting.

**Domain & Services**: Processes the core business rules and workflows (e.g., validation logic, inventory, stock updates, processing incoming client messages).

**Infrastructure**: Manages the core configuration and database connections.


**Repositories**: The persistence layer. Functions here manage data storage and retrieval, execute data queries, and act as the bridge between the database and the services layer.



#### How to Run Locally


This project uses Docker to ensure a seamless setup process.

**Build and Run the Container**
Make sure Docker desktop is running on your machine, then execute:

**Build the Docker image**
> docker build -t watkit-api -f dockerfile .

**Run the container**

> docker-compose --build

**Run Database Migrations**

Before adding data, apply the latest database schemas using Alembic:

> docker exec -it watkit-app alembic upgrade head

**Seed the Database**

To *populate* the database with initial testing data (like product catalogs), run the seed script:

> docker exec -it watkit-app python seed.py


**API Documentation**

Once the container is running, you can interact with the API directly through the browser:


> Swagger UI: http://localhost:8000/docs (Interactive testing interface)


> ReDoc: http://localhost:8000/redoc (Clean, read-only documentation)



**credentials information**
To see your DB_PASSWORD and all the information related to your database execute this command:
> docker exec -it watkit-api env

if everything is all right you might see the port connection and all related information.

You can see the example_env.txt file to create .env file.

### Unit testing

The service layer is tested using asynchronous unit test with mocked dependencies.Instead of relying on real database connections or external services, mocks are used to simulate the behavior of repositories and services in isolation.

The test leverage AsyncMock from Python's unittest.mock to properly handle async functions, allowing the business logic to be executed and validated without side effects.

this approach ensures:

- Fast and reliable test execution.
- Isolation of Business Logic.
- Full control over dependency behavior

This allows testing complex workflows in a deterministic and reproducible way.




