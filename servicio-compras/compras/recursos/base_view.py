from flask_classy import FlaskView
import compras


class BaseView(FlaskView):
    @classmethod
    def build(self, app):
        self.conexion = compras.database.conexion
        self.register(app)
