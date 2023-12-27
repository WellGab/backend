# WellGab - AI-Powered Symptom and Diagnosis Guidance

WellGab is an AI-powered application designed to provide users with symptom analysis and guidance for potential health issues. This is the backend API, it utilizes Opeanai chat APIs for AI recommendations, FastApi a Python web framework for the web server, MongoDB for data management, and Socketio for efficient chat functionality.

## Features

- **AI Symptom Analysis powered by OpeanAI:** WellGab leverages Openai's advanced AI algorithms to analyze user-entered symptoms and provide potential health issue guidance.

- **FastApi:** Fastapi is a simple and efficient Python web framework.

- **Efficient Data Management with Mongodb:** Data is the new oil and every user's data is saved with their permission and can also be deleted if they want to, thanks to Mongodb.

- **Efficient Chatting with Socketio:** Socketio was used to implement web-socket communications between users and the AI chatbot.

- **Decent Test Coverage with Pytest:** Pytest was used to achieve a 70% test coverage knowing the importance it is to maintaining a stable system. With the tests in place breaking changes can be easily caught before pushing to production.
  
- **CI/CD with GitHub Actions:** It is important to be able to ship features as fast as possible and also fix bugs very quickly that was why we used GitHub Actions to automate pushing our API to an EC2 instance on aws on git push
  
- **Containerization with Docker:** The application was containerized using Docker for easy deployment
-   
- **Cloud deployment on AWS EC2:** The application was deployed on an AWS EC2 instance for high availability  

## Getting Started

### Prerequisites

- Python installed on your machine
- Package manager (pip)

### Installation

1. clone the repository:
2. start the virtual environment in the project folder
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
- explore the different endpoints available

## Technologies Used

- Fastapi
- MongoDB
- OpenAI
- Socketio
- GitHub Actions
- Pytest
- Docker
- AWS EC2

## Language
[![Python Version](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9-blue.svg)](https://www.python.org/downloads/)

## License
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)
