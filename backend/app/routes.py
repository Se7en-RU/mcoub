from modules.search import search_bp

def route(app):
    app.register_blueprint(search_bp)