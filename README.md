**Watkit API**
This API automates client management by providing automated follow-up triggers and structured data storage for client information. It is designed with a clean, layered architecture to ensure maintainability and scalability.

*Tech Stack*
Framework: FastAPI (High performance, easy to use, auto-generated docs).

ORM: SQLAlchemy (Robust SQL database management).

Migrations: Alembic (Automated database schema management).

Database: PostgreSQL (Relational data storage).

Containerization: Docker (Ensures a consistent, reproducible environment).

Asynchrony: asyncio (Asynchronous programming, optimizing I/O bound tasks).

Language: Python 3.13+

Project Architecture
The application follows a layered design pattern to separate concerns and maintain clean code:

Endpoints (FastAPI): Handles HTTP requests, routing, and response formatting.

Services: Processes the core business rules and workflows (e.g., validation logic, inventory/stock updates, processing incoming client messages).

Infrastructure: Manages the core configuration and database connections.

config.py: Contains the core settings, PostgreSQL configuration, and asynchronous database connection setup.

database.py: Houses the SQLAlchemy models and database mapping.

Repositories: The persistence layer. Functions here manage data storage and retrieval, execute data queries, and act as the bridge between the database and the services layer.

*How to Run Locally*
This project uses Docker to ensure a seamless setup process.

*1. Build and Run the Container*
Make sure Docker is running on your machine, then execute:

# Build the Docker image
docker build -t watkit-api .

# Run the container on port 8000
docker run -d -p 8000:8000 --name watkit-app watkit-api

*2. Run Database Migrations*
Before adding data, apply the latest database schemas using Alembic:

docker exec -it watkit-app alembic upgrade head

*3. Seed the Database*
To populate the database with initial testing data (like product catalogs), run the seed script:

docker exec -it watkit-app python seed.py

**API Documentation**
Once the container is running, you can interact with the API directly through the browser:

# Swagger UI: http://localhost:8000/docs (Interactive testing interface)

# ReDoc: http://localhost:8000/redoc (Clean, read-only documentation)

**Known Issues & Future Modifications**
This project is under active development. Current focus areas and upcoming improvements include:

Message Service Integration: The external messaging webhook (via Twilio/ngrok) is currently experiencing routing timeouts. The next iteration will migrate testing to the WhatsApp Sandbox to bypass carrier registration locks and ensure reliable local testing.

Enhanced Test Coverage: Add pytest integration to automatically test the Service and Repository layers to ensure rock-solid data validation.