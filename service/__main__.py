import logging
from service.countries import app

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    logger.info('Start')
    app.run()

if __name__ == '__main__':
    main()