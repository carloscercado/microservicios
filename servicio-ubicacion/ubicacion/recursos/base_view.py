from flask_classy import FlaskView
import ubicacion


class BaseView(FlaskView):
    @classmethod
    def build(self, app):
        self.conexion = ubicacion.database.conexion
        self.register(app)
