from __future__ import absolute_import
import os
try:
    import urlparse ## PY2
except ImportError:
    from urllib import parse as urlparse ## PY3
    
import redis

class RedisManager(object):

    def __init__(self, app=None):

        if app is not None:
            self.init_app(app)
        else:
            self.app = None
            self.instance = None

    def init_app(self, app):
        """
        Used to initialize redis with app object
        """
        
        ## Redis To Go on Heroku
        #     see: http://stackoverflow.com/questions/10598641/the-herokus-python-doesnt-find-redisredistogo-for-import
        #
        redis_url = urlparse.urlparse(os.environ.get('REDISTOGO_URL', 'redis://localhost:6379'))
            

        app.config.setdefault('REDIS_HOST', redis_url.hostname)
        app.config.setdefault('REDIS_PORT', redis_url.port)
        app.config.setdefault('REDIS_DB', 0)
        app.config.setdefault('REDIS_PASSWORD', redis_url.password)

        self.app = app
        self._connect()


    def _connect(self):
        self.instance = redis.Redis(host=self.app.config['REDIS_HOST'],
                           port=self.app.config['REDIS_PORT'],
                           db=self.app.config['REDIS_DB'],
                           password=self.app.config['REDIS_PASSWORD'])

    def get_instance(self):
        return self.instance
