from pyramid.config import Configurator
from pyramid_zodbconn import get_connection
from .models import appmaker
#from .views import notfound_view
#from pyramid.exceptions import NotFound

def root_factory(request):
    conn = get_connection(request)
    return appmaker(conn.root())

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(root_factory=root_factory, settings=settings, autocommit=True)
    config.add_static_view('static', 'static', cache_max_age=3600)
    
    config.scan()
    #config.add_view(notfound_view, context=NotFound)
    return config.make_wsgi_app()
