from  App import app
# import views
from App import db
# from posts.blueprint import posts
from api.v1.views.path import *
from flask import make_response

# app.register_blueprint(posts, url_prefix='/blog')
app.register_blueprint(app_views)

@app.teardown_appcontext
def close_db(error):
    """close the session connection when done"""
    db.session.close()


@app.errorhandler(404)
def not_found(error):
    """404 Error handler if the route is wrong"""
    return make_response(jsonify({'error': "Not found"}), 404)

if __name__ == '__main__':
    app.run()
