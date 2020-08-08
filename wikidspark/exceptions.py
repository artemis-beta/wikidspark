class IDNotFoundError(Exception):
    def __init__(self, ID):
        self.message = f"ID '{ID}' not found in WikiData database."
        super().__init__(self.message)

class IDMatchError(Exception):
    def __init__(self, search_str):
        self.message = f"Failed to find a matching WikiData ID for '{search_str}'."
        super().__init__(self.message)

class PropertyNotFoundError(Exception):
    def __init__(self, prop):
        self.message = f"'{prop}' is not a valid property name."
        super().__init__(self.message)
