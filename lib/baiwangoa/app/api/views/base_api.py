from flask import abort, jsonify, abort
from flask.views import MethodView
from config import global_config


class BaseAPI(MethodView):

    def __init__(self):
        super(BaseAPI, self).__init__()
        self.response = APIResponse()
        self.config = global_config

    def to_int(self, arg, error_code, error_msg=''):
        try:
            return int(arg)
        except ValueError:
            abort(self.bad_request(error_code, error_msg))

    def bad_request(self, error_code, msg=''):
        self.response.result = 'failed'
        self.response.error = 'Bad Request'
        self.response.error_msg = msg
        self.response.error_code = error_code
        self.response.status_code = 400
        return self.response.make_response()

    def get(self):
        abort(405)

    def post(self):
        abort(405)

    def put(self):
        abort(405)

    def delete(self):
        abort(405)


class APIResponse(object):

    def __init__(self, result='failed', status_code=200, **kwargs):
        self.result = result
        self.status_code = status_code
        for k, v in kwargs.items():
            setattr(self, k, v)

    @staticmethod
    def get_all_attribute(obj, excloud_list=None, format_name=True, format_method=None):
        """
        Get object attribute from __dict__.
        default format : 'attribute_name' -> 'AtrributeName'
        """
        def _default_format_method(key):
            new_key = ''
            for k in key.split('_'):
                new_key += k.capitalize()
            return new_key

        if excloud_list is None:
            excloud_list = []
        else:
            excloud_list = set(excloud_list)

        if format_name and format_method is None:
            format_method = _default_format_method

        result = {}
        if hasattr(obj, '__dict__'):
            for k, v in obj.__dict__.items():
                if k in excloud_list:
                    continue
                else:
                    if format_name:
                        result[format_method(k)] = v
                    else:
                        result[k] = v
        return result

    def make_response(self):
        msg = self.get_all_attribute(self, excloud_list=['status_code'])
        response = jsonify(msg)
        response.status_code = self.status_code
        return response
