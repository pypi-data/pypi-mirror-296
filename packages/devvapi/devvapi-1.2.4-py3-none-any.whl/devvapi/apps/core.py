import re

class BodyInstance(object):
    def __init__(self, swagger) -> None:
        self.swagger = swagger

def Body(instance: object) -> BodyInstance:
    swagger_field_types = {
        str: "string",
        int: "integer"
    }

    swagger = []    
    for name, field_type in instance.__annotations__.items():
        swagger.append(
            {
                "name": f"{name}",
                "in": "path",
                "description": "The ID of the user",
                "required": True,
                "schema": {
                    "type": swagger_field_types[field_type]
                }
            },
        )
    
    return BodyInstance(swagger)

class AppConfig:
    path = None
    name = None
    version: int = 1

class App:
    def __init__(self, app_config: AppConfig):
        self.app_config = app_config
        self.routes = {}

    def add_route(self, path, method, handler, description="", parameters: BodyInstance = None):
        full_path = f"/v{self.app_config.version}{self.app_config.path}{path}"

        path_pattern = re.sub(r'{(\w+)}', r'(?P<>[^/]+)', full_path)
        path_regex = f'^{path_pattern}/?$'

        if path_regex not in self.routes:
            self.routes[path_regex] = {}

        self.routes[path_regex][method.upper()] = {"handler": handler, "description": description, "path": full_path, 'parameters': parameters}

    def get(self, path, description=""):
        return self.route(path, 'GET', description)

    def post(self, path, description="", parameters: BodyInstance = None):
        return self.route(path, 'POST', description, parameters)

    def put(self, path, description=""):
        return self.route(path, 'PUT', description)

    def delete(self, path, description=""):
        return self.route(path, 'DELETE', description)

    def patch(self, path, description=""):
        return self.route(path, 'PATCH', description)

    def route(self, path, method, description="", parameters: BodyInstance = None):
        def decorator(handler):
            self.add_route(path, method, handler, description, parameters)
            return handler
        return decorator

    def find_handler(self, method, path):
        for path_pattern, methods in self.routes.items():
            match = re.match(path_pattern, path)
            if match:
                route_info = methods.get(method.upper(), None)
                if route_info:
                    return route_info["handler"], match.groupdict()
        return None, None

    def get_routes(self):
        return self.routes
