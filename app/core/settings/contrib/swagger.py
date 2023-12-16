# Swagger Settings
SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Auth Token eg [Bearer (JWT)]": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "flow": "Bearer",
        },
    },
    "DEFAULT_MODEL_RENDERING": "example",
}
