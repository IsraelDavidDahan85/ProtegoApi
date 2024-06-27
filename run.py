from app import create_app
from logger.log import log

app = create_app()

if __name__ == '__main__':
    log.info('Starting server...')
    app.run(host="0.0.0.0", port=5555, debug=True)
