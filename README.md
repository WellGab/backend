# WellGab - AI-Powered Symptom and Diagnosis Guidance

WellGab is an AI-powered application designed to provide users with symptom analysis and guidance for potential health issues. This is the basck end api, it utilizes Opeanai chat apis for ai recommendations, FastApi a python web framework for the web server, Mongodb for data management, and Socketio for efficient chat functionality.

## Features

- **AI Symptom Analysis powered by OpeanAI:** WellGab leverages openai's advanced AI algorithms to analyze user-entered symptoms and provide potential health issue guidance.

- **FastApi:** Fastapi is a simple and efficient python web framework.

- **Efficient Data Management with Mongodb:** Data is the new oil and every user data is saved with their permission and can also be deleted if they want to, thanks to Mongodb.

- **Efficient Chatting with Socketio:** Socketio was used to implement websockets communications between users and the ai chatbot.

- **Decent Test Coverage with Pytest:** Pytest was used to achieve a 70% test coverage knowing the importance it is to maintain a stable with system. With the tests in place breaking changes can be easily be caught before pushing to production.
  
- **CI/CD with Github Actions:** It is important to be able to ship features as fast as possible and also fix bugs very quickly that was why we used github actions to automate pushing our api to an ec2 instance on aws on git push
  
- **Containerization with Docker:** The application was containerized using docker for easy deployment
-   
- **Cloud deployment on AWS EC2:** The application was deployed on an AWS EC2 instance for high availability  

## Getting Started

### Prerequisites

- Python installed on your machine
- Package manager (pip)

### Installation

1. clone the repository:
2. start virtual environment in project folder
3. install dependencies
4. create .env file from .env.example
5. run app

```bash
git clone https://github.com/WellGab/backend.git
cd backend
python -m venv venv
. venv/bin/activate    
pip install -r requirements.txt
gunicorn app.main:app -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Usage
- open [http://127.0.0.1:8000/api/v1](http://127.0.0.1:8000/docs) with your browser to see the result.
- wxplore the different endpoints available

## Technologies Used

- Fastapi
- Mongodb
- OpenAI
- Socketio
- Github Actions
- Pytest
- Docker
- AWS EC2

## Language
[![Python Version](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9-blue.svg)](https://www.python.org/downloads/)

## License
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)