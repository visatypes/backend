import logging

from flask import Flask
from pydantic import ValidationError

from service.countries.views import country_view
from service.errors import AppError

app = Flask(__name__)

app.register_blueprint(country_view, url_prefix='/api/countries')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def handle_app_error(error: AppError):
    return {'error': str(error)}, error.code


def handle_valid_error(error: ValidationError):
    return {'error': str(error)}, 400


app.register_error_handler(AppError, handle_app_error)
app.register_error_handler(ValidationError, handle_valid_error)


def main():
    logger.info('Start')
    app.run()


if __name__ == '__main__':
    main()
