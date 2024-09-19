import json
import traceback

from django.http import HttpResponse
from django.utils import timezone

from afex_logger.util import LogUtil

successful_status = {200, 201, 302, 301}


class LogMiddleware:

    def __init__(self, get_response) -> None:
        self.get_response = get_response
        self.request_time = timezone.now()

    def __call__(self, request, *args, **kwargs):
        self.process_request(request)
        response = self.process_response(request)
        return response

    def process_request(self, request):
        return None

    def process_response(self, request):
        data = None
        try:
            raw_body = request.body
            raw_body = raw_body.decode("utf-8")
            if raw_body:
                data = json.loads(raw_body)
        except:
            pass

        response = self.get_response(request)

        has_exception = not isinstance(response, HttpResponse)

        path = request.path_info

        util = LogUtil()
        config_provider = util.get_config_provider()

        excluded_path_patterns = config_provider.get_excluded_path_patterns()

        for p in excluded_path_patterns:
            if p in path:
                return response

        response_time = timezone.now()

        if request.method in config_provider.get_excluded_request_method():
            return response

        if hasattr(request, 'user') and request.user.is_authenticated:
            user = request.user
        else:
            user = None

        rest_content_types = config_provider.get_rest_content_types()
        api_path_prefix = config_provider.get_api_path_prefix()
        req_content_type = request.META.get('CONTENT_TYPE', '')

        response_type = 'http'

        if api_path_prefix in path or req_content_type in rest_content_types:
            response_type = 'rest'

        if response_type == 'http':
            response_body = 'http content'
        else:
            if response.streaming:
                response_body = "Streamed Content"
            else:
                res_body = response.content.decode('utf-8')
                try:
                    response_body = json.loads(res_body)
                except Exception as _:
                    response_body = res_body

        if not data:
            data = {}

        keys = config_provider.get_excluded_data_fields()

        for key in keys:
            if key in data:
                data[key] = "**********"

        log_data = {
            "date": timezone.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
            'ip_address': get_real_ip_address(request),
            'user': {"id": user.id, "username": user.username} if user else None,
            'http_method': request.method,
            'path_info': path,
            "request": {
                "body": data,
                "headers": request.META
            },
            "response": {
                'status_code': response.status_code,
                'response_type': response_type,
                'reason_phrase': response.reason_phrase,
                'body': response_body if not has_exception else None,
                "headers": response.headers
            },
            'attempt_time': self.request_time,
            'response_time': response_time
        }
        try:
            util.submit_requests_log(log_data)
        except Exception as e:
            util.report_exception(e)
        return response

    def process_exception(self, request, exception):
        self.exception = str(exception)
        self.traceback = traceback.format_exc()


def get_real_ip_address(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip
