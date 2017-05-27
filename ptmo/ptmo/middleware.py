import re
import threading 
request_cfg = threading.local()


class RouterMiddleware(object):
    def process_request( self, request):
        import pdb; pdb.set_trace()
        pattern = re.compile("\\b(http://|https://|www.|.com|8000|:|//)\\W\\d+", re.I)
        words = request.get_host()        
        db_name = [pattern.sub("", words)][0].split('.')[0]
        request_cfg.cfg = db_name
        return None

    def process_response( self, request, response ):
        if hasattr( request_cfg, 'cfg' ):
            del request_cfg.cfg
        return response


class DatabaseRouter (object):
    def _default_db( self ):
        if hasattr( request_cfg, 'cfg' ):
            return request_cfg.cfg
        else:
            return 'default'

    def db_for_read( self, model, **hints ):
        return self._default_db()

    def db_for_write( self, model, **hints ):
        return self._default_db()