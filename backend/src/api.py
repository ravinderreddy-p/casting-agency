from flask import Flask, jsonify, abort, request, url_for, redirect
from flask_cors import CORS

from .database.models import setup_db, Actor, Movie


def create_app(test_config=None):
    # create and config the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r"/api/*": {"origins": '*'}})

    @app.route('/actors')
    def get_actors():
        actors = Actor.query.all()

        actors_name = [actor.name for actor in actors]
        actors_age = [actor.age for actor in actors]
        actors_gender = [actor.gender for actor in actors]

        if len(actors) == 0:
            abort(404)

        return jsonify({
            'name': actors_name,
            'age': actors_age,
            'gender': actors_gender
        })

    @app.route('/movies')
    def get_movies():
        movies = Movie.query.all()

        movie_names = [movie.name for movie in movies]
        movie_release_dates = [movie.release_date for movie in movies]

        if len(movies) == 0:
            abort(404)

        return jsonify({
            'name': movie_names,
            'release_date': movie_release_dates
        })

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    def delete_actor(actor_id):
        try:
            actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
            if actor is None:
                abort(404)
            actor.delete()
            return jsonify({
                'success': True
            })

        except:
            abort(405)

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    def delete_movie(movie_id):
        try:
            movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
            if movie is None:
                abort(404)
            movie.delete()
            return jsonify({
                'success': True
            })
        except:
            abort(405)

    @app.route('/actors', methods=['POST'])
    def add_actor():
        body = request.get_json()
        actor_name = body.get('name', None)
        actor_age = body.get('age', None)
        actor_gender = body.get('gender', None)
        actor = Actor(name=actor_name, age=actor_age, gender=actor_gender)
        actor.insert()
        # return redirect(url_for('get_actors'))
        return jsonify({
            'success': True
        })

    @app.route('/movies', methods=['POST'])
    def add_movie():
        body = request.get_json()
        movie_name = body.get('name', None)
        movie_release_date = body.get('release_date', None)
        movie = Movie(name=movie_name, release_date=movie_release_date)
        movie.insert()
        # return redirect(url_for('get_actors'))
        return jsonify({
            'success': True
        })

    '''
    Route handler for editing existing actors.
    Requires 'patch:actors' permission.
    '''
    @app.route('/actors/<int:id>', methods=['PATCH'])
    def update_actors(id):
        actor = Actor.query.filter_by(id=id).one_or_none()

        if actor is None:
            abort(404)

        body = request.get_json()

        if 'name' in body:
            actor.name = body['name']

        if 'age' in body:
            actor.age = body['age']

        if 'gender' in body:
            actor.gender = body['gender']

        try:
            # update drink in database
            actor.insert()

        except Exception as e:
            # catch exception
            print('EXCEPTION: ', str(e))

            # Bad request
            abort(400)

        return jsonify({
            'success': True
        })

    '''
       Route handler for editing existing actors.
       Requires 'patch:actors' permission.
       '''

    @app.route('/movies/<int:id>', methods=['PATCH'])
    def update_movies(id):
        movie = Movie.query.filter_by(id=id).one_or_none()

        if movie is None:
            abort(404)

        body = request.get_json()

        if 'name' in body:
            movie.name = body['name']

        if 'release_date' in body:
            movie.release_date = body['release_date']

        try:
            # update drink in database
            movie.insert()

        except Exception as e:
            # catch exception
            print('EXCEPTION: ', str(e))

            # Bad request
            abort(400)

        return jsonify({
            'success': True
        })


    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    return app

