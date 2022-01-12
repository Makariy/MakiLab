from .home.app import get_blueprint as home_get_blueprint
from .videos.app import get_blueprint as videos_get_blueprint


blue_print_routes = [
    home_get_blueprint,
    videos_get_blueprint,

]
