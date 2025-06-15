class UserClient:
    def __init__(self, request_handler):
        self.request_handler = request_handler

    def get_current_user_profile(self):
        return self.request_handler.get("/me")
