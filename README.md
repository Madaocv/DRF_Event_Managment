# EDjango REST-Api for Event Management

## Project Description
The primary goal of this task is to create a Django-based REST-Api that manages events (like conferences, meetups, etc.). The application will allow users to create, view, update, and delete events. It should also handle user registrations for these events.

### Features
- **Event Model**
Design an Event model with fields such as title, description, date, location, and organizer.
- **CRUD Operations**
Implement CRUD (Create, Read, Update, Delete) operations for the Event model.
- **JWT**
Basic User Registration and Authentication.
- **Rest Request for Event Registration**
Event Registration
- **API documentation**
Generate beautiful API documentation from OpenAPI with Redoc
- **Search Filtering**
Implement an advanced feature like event search or filtering.

## Build and Run Commands

### Manual Setup using Virtualenv

1. **Clone the repository**:
```sh
git clone https://github.com/Madaocv/DRF_Event_Managment.git
cd eva00
```

2. **Create and activate a virtual environment**:
```sh
virtualenv -p python3 venv
source venv/bin/activate
```

3. **Install the required packages**:
```sh
pip install -r requirements.txt
```

4. **Database settings**:
```sh
python manage.py migrate
```

5. **Load initial data (optional)**:
```sh
python manage.py loaddata initial_data.json
```

6. **Start the local development server**:
```sh
python manage.py runserver
```

7. **Review of the project**:
Open a browser and go to http://127.0.0.1:8000/ to see your working project.


### Setup using Docker

1. **Clone the repository**:
```sh
git clone https://github.com/Madaocv/DRF_Event_Managment.git
cd eva00
```

1. **Build the Docker containers**:
```sh
docker build -t rest_event_eliiashiv_app .
```

2. **Run the Docker containers**:
```sh
docker run -d -p 8000:8000 rest_event_eliiashiv_app
```

The application should now be running and accessible at http://localhost:8000.