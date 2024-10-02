from flask_swagger_ui import get_swaggerui_blueprint

def configure_swagger(app):
    # Swagger configuration
    SWAGGER_URL = '/swagger'
    API_URL = '/swagger.json'

    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': 'Talon Python API',
            'description': "Talon application api"
        }
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
