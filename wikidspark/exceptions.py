import requests

class IDNotFoundError(Exception):
    def __init__(self, ID):
        self.message = f"ID '{ID}' not found in WikiData database."
        super().__init__(self.message)

class IDMatchError(Exception):
    def __init__(self, search_str):
        self.message = f"Failed to find a matching WikiData ID for '{search_str}'."
        super().__init__(self.message)

class LanguageError(Exception):
    def __init__(self, language_title: str) -> None:
        self.message = f"Language '{language_title}' is not a recognised WikiData language"
        super().__init__(self.message)

class ConnectionError(Exception):
    def __init__(self, request: requests.Response):
        self.message = f"Failed to retrieve response from '{request.url}' with code {request.status_code}"
        super().__init__(self.message)

class PropertyNotFoundError(Exception):
    def __init__(self, prop):
        self.message = f"'{prop}' is not a valid property name."
        super().__init__(self.message)
