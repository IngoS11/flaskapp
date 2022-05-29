
template = {
  "swagger": "2.0",
  "info": {
    "title": "Bookmark Application API",
    "description": "API for the bookmark demo application",
    "contact": {
      "responsibleOrganization": "",
      "responsibleDeveloper": "",
      "email": "",
      "url": "",
    },
    "termsOfService": "",
    "version": "0.0.1"
  },
  "basePath": "/api/v1",  # base bash for blueprint registration
  "schemes": [
    "http",
    "https"
  ],
  "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: \"Authorization: Bearer {token}\""
        }
  },
  "operationId": "getmyData"
}

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True, # all in
            "model_filter": lambda rule: True, # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/"
}
