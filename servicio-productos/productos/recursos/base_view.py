from flask_classy import FlaskView
import productos


class BaseView(FlaskView):
    @classmethod
    def build(self, app):
        self.conexion = productos.database.conexion
        self.register(app)
