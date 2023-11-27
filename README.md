# WellGab - AI-Powered Symptom and Diagnosis Guidance

WellGab is an AI-powered application designed to provide users with symptom analysis and guidance for potential health issues. This is the basck end api, it utilizes Opeanai chat apis for ai recommendations, FastApi a python web framework for the web server, Mongodb for data management, and Socketio for efficient chat functionality.

## Features

- **AI Symptom Analysis powered by OpeanAI:** WellGab leverages openai's advanced AI algorithms to analyze user-entered symptoms and provide potential health issue guidance.

- **FastApi:** State management is handled efficiently with Recoil, making it easy to manage and share the application's state across components.

- **Efficient Data Management with Mongodb:** The UI is designed to be responsive and visually appealing, thanks to Tailwind CSS.

- **Efficient Chatting with Socketio:** React Query is employed for data fetching, ensuring optimal performance and a smooth user experience.

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

## Language
[![Python Version](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9-blue.svg)](https://www.python.org/downloads/)

## License
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)