from flask_classy import FlaskView
import auth


class BaseView(FlaskView):
    @classmethod
    def build(self, app):
        self.conexion = auth.database.conexion
        self.register(app)
        self.API_KEY = "91f5167c34c400758115c2a6826ec2e3"
