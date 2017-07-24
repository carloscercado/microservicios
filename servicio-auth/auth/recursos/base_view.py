from flask_classy import FlaskView
import auth


class BaseView(FlaskView):
    @classmethod
    def build(self, app, KEY):
        self.conexion = auth.database.conexion
        self.register(app)
        self.API_KEY = KEY
