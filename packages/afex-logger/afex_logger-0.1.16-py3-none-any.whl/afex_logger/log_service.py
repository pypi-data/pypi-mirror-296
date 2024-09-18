from afex_logger.http_agent import HttpAgent


class AppLogService:

    def __init__(self):
        from afex_logger.util import LogTypes, LogUtil

        self.path_mappings = {
            LogTypes.activities: "activities",
            LogTypes.errors: "errors",
            LogTypes.process: "process",
            LogTypes.requests: "requests",
        }

        self.util = LogUtil()
        self.config_provider = self.util.get_config_provider()

        api_key = self.config_provider.get_api_key()
        base_url = self.config_provider.get_base_url()

        self.https_agent = HttpAgent(
            api_key, base_url + "/api/v1/logs/"
        )

    def fetch_logs(self, log_type, filter_params):
        return self.https_agent.make_get_request(self.path_mappings[log_type], filter_params)

    def submit_log(self, log_type, payload):
        from afex_logger.repo_service import repository

        repository.repo.aggregate(log_type, payload)
        return "Log data aggregated", None

    def send_logs(self):
        from afex_logger.repo_service import repository

        repo = repository.repo
        # pick first nth logs from the stack and send
        payload = repo.peck()
        res, error = self.https_agent.make_post_request("", payload)
        if error:
            repo.re_stack(payload)

        if self.config_provider.is_test_mode():
            if error:
                self.util.debug_print(error)
            else:
                self.util.debug_print(res)
