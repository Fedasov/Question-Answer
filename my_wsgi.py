from pprint import pformat

result = b"OK!!\n"
def simple_app(environ, start_response):
    """Simplest possible application object"""
    status = '200 OK'
    if environ['REQUEST_METHOD'] == 'POST':
        print("POST data: ", pformat(environ['wsgi.input'].read()))
    if environ['REQUEST_METHOD'] == 'GET':
        if environ['QUERY_STRING'] != '':
            print("GET data: ", environ['QUERY_STRING'])
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)
    return [result]

application = simple_app

class AppClass:
    """Produce the same output, but using a class

    (Note: 'AppClass' is the "application" here, so calling it
    returns an instance of 'AppClass', which is then the iterable
    return value of the "application callable" as required by
    the spec.

    If we wanted to use *instances* of 'AppClass' as application
    objects instead, we would have to implement a '__call__'
    method, which would be invoked to execute the application,
    and we would need to create an instance for use by the
    server or gateway.
    """

    def __init__(self, environ, start_response):
        self.environ = environ
        self.start = start_response

    def __iter__(self):
        status = '200 OK'
        response_headers = [('Content-type', 'text/plain')]
        self.start(status, response_headers)
        yield HELLO_WORLD