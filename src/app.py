from flask import Flask
from flask_cors import CORS
from config import config

# Routes
from routes import FragranceRoute, ReviewsRoute

app = Flask(__name__)
CORS(app, supports_credentials=True)


def page_not_found(error):
    return "<h1>Page not found</h1>", 404


if __name__ == "__main__":
    app.config.from_object(config['development'])

    # Blueprint
    app.register_blueprint(FragranceRoute.main, url_prefix='/api/v1/fragrance')
    app.register_blueprint(ReviewsRoute.main, url_prefix='/api/v1/review')

    # Error Handlers
    app.register_error_handler(404, page_not_found)

    app.run()