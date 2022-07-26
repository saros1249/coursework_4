from project.config import config
from project.server import create_app

app = create_app(config)

# @app.shell_context_processor
# def shell():
#    return {
#        "db": db,
#        "Genre": Genre,
#        "Director": Director,
#        "Movie": Movie,
#    }

if __name__ == '__main__':
    app.run()
