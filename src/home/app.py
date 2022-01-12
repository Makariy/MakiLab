def get_blueprint():
    from .routes import bp
    bp.url_prefix = ''
    return bp


