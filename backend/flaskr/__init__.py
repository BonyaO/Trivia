import logging
import os
from unicodedata import category
from wsgiref.util import request_uri
from flask import Flask, request, abort, jsonify
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page -1)*QUESTIONS_PER_PAGE
    end= start + QUESTIONS_PER_PAGE
    formatted_questions = [question.format() for question in selection]
    current_questions = formatted_questions[start:end]
    return current_questions

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)
    logging.getLogger('flask_cors').level = logging.DEBUG

    
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response


    @app.route('/categories')
    def get_categories():
        categories = Category.query.all()
        formatted_categories = {category.id: "{}".format(category.type) for category in categories}
        return jsonify({
            'success': True,
            'categories': formatted_categories,
            'total_categories': len(formatted_categories)
        })

    @app.route('/questions')
    def get_questions():

        questions = Question.query.order_by(Question.id).all()
        category = Category.query.filter_by(id=questions[0].category).one_or_none()
        return jsonify({
            'success':True,
            'questions':paginate_questions(request,questions),
            'total_questions': len(questions),
            'currentCategory': category.type,
            'categories': {category.id: "{}".format(category.type) for category in Category.query.all()}
        })

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.get(question_id)
            question.delete()
            return jsonify({
                'success': True,
                'deleted':question.id
            })
        except: 
            abort(422)

    
    @app.route('/questions', methods=['POST'])
    def handle_request():
        request_body = request.get_json()

        if request_body.get('searchTerm') is None:
            question = request_body.get('question')
            answer = request_body.get('answer')
            category = request_body.get('category')
            difficulty = request_body.get('difficulty')

            if question is None:
                abort(422)

            try:
                new_question = Question(question=question, answer=answer, category=category, difficulty=difficulty)
                new_question.insert()
                print(new_question)
                return jsonify({
                    'success': True,
                    'created': new_question.id,
                })
            
            except:
                abort(422)
        else:
            search_term = request.get_json()['searchTerm']
            try: 
                questions = Question.query.filter(Question.question.ilike("%" + search_term + "%")).all()
                category = Category.query.filter_by(id=questions[0].category).one_or_none()
                
                return jsonify({
                    'success': True,
                    'questions': [question.format() for question in questions],
                    'totalQuestions':len(questions),
                    'currentCategory': category.type

                })

            except: 
                abort(400)
     
    @app.route('/categories/<int:category_id>/questions')
    def get_questions_for_id(category_id):

        try: 
            questions = Question.query.filter_by(category=category_id).order_by(Question.id).all()
            category = Category.query.filter_by(id=category_id).one_or_none()

            return jsonify({
                'success':True,
                'questions':paginate_questions(request,questions),
                'total_questions': len(questions),
                'currentCategory': category.type
            })
        except: 
            abort(400)

    @app.route('/quizzes', methods=['POST'])
    def get_quiz():
        request_body = request.get_json()
        past_questions = request_body.get('previous_questions')
        category = request_body.get('quiz_category')
        try:
            questions = Question.query.filter_by(category=int(category['id'])).all()
            new_question = None
            # Chooses a random question from the list of questions in that category
            # and verifies if the question is in the previous questions list
            # This is repeated till a question not on the list is found
            while new_question is None:
                 random_num = random.randint(0, len(questions)-1)
                 if questions[random_num].id not in past_questions:
                    new_question = questions[random_num]
                    break
            return jsonify({
                'question': new_question.format()
            })
        except:
            abort(404)

    @app.errorhandler(405)
    def handle_not_allowed(error):
        return jsonify({
            "success":False,
            "error":405,
            "message": "The method is not allowed for the requested URL."
        }), 405


    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success":False,
            "error":422,
            "message": "Unprocessable"
        }), 422
    
    @app.errorhandler(400)
    def handle_bad_request(error):
        return jsonify({
            "success":False,
            "error":400,
            "message": "Bad Request"
        }), 400
    @app.errorhandler(404)
    def handle_not_found(error):
        return jsonify({
            "success":False,
            "error":404,
            "message": "Not Found"
        }), 404

    return app

