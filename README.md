# API Development and Documentation Final Project

## Trivia App

The Trivia app is the final project for the API Development and Documentation course of the Udacity's Fullstack Web-developer nanodegree. It is a webapp that allows you to play a game by answering questions from different sets of categories. You can see all the questions and can search for questions as well as view questions per category. You can also add new questions. 

## Getting Started
The app is divided into the backend and frontend folders. The backend is build with python and the frontend with react. Instructions to run each of the environments are listed below

### Backend
Navigate to [backend](backend/) and create your python virtual environment

From the backend folder run
```bash
# Mac users
python3 -m virtualenv venv
source venv/bin/activate
# Windows users
> py -3 -m virtualenv venv
> venv\Scripts\activate
```

* **Install dependencies**<br>
From the backend folder run 
```bash
# All required packages are included in the requirements file. 
pip3 install -r requirements.txt
```

**Setup Database**
With Postgres running, create a `trivia` database:

```bash
createdb trivia
```
Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```
Create a database user `student` with password `student` or edit [models.py](backend/models.py) to replace the database user and password to a local user.

**Run the backend server**
```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

### frontend
Navigate to the [frontend](frontend/) and run the following commands
```
npm install
npm start
```

## API Endpoints Documentation
`GET '/api/v1.0/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.

```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```

`GET '/api/v1.0/questions?page=page_number'`
- Fetches a paginated list of questions, the total number of questions and a dictionary of categories as well as the current category
- Request Arguments: page_number
- Returns: An object with four keys: a list of `questions`, `currentCategory`, `total_questions` and a dictionary of `categories`

```json
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "currentCategory": "Entertainment", 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }
  ], 
  "success": true, 
  "total_questions": 19
}
```

`DELETE '/api/v1.0/questions/<int:id>'`
- Deletes a questions with id specified in the url
- Request Arguments: question id
- Returns: A json object with the success status and the `id` of the deleted question

```json
{
    "success":true,
    "deleted":22
}

```

`POST '/api/v1.0/questions'`
- This endpoint either creates a new question in the database or searches for an existing question depending on data passed to the endpoint
- Case1: Request Argument is json object of the form `{"searchTerm":"World"}`
- Returns a list of questions that matches the searchterm, the current category and the total number of questions that matches the search

```json
{
  "currentCategory": "Sports", 
  "questions": [
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }
  ], 
  "success": true, 
  "totalQuestions": 2
}
```

- Case2: Request argument is json object that contains the `question`, `answer`, `category` and `difficulty` 
- Adds a new question in the database and returns a json object with the id of the question created

```json
{
    "success":true,
    "created":27
}
```

`GET '/api/v1.0/categories/<int:category_id>/questions'`
- Fetches all questions for a particular category
- Request Arguments: `category_id`
- Returns a list of questions in the category of id `category_id`

```json
{
  "currentCategory": "Geography", 
  "questions": [
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }, 
    {
      "answer": "Agra", 
      "category": 3, 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ], 
  "success": true, 
  "total_questions": 3
}
```

`POST /api/v1.0/quizzes`
- Fetches a question from the database that belongs to a particular category and has not been asked before in the quiz
- Request arguements: json object containing a list of previous questions and a category object `{"previous_questions":[21, 21], "category":{"id":4,"type":"History"}}`
- Respons is a single question formatted as json
```json
{
      "answer": "Agra", 
      "category": 3, 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }

```


