from distutils.core import setup

setup(name='Distutils',
      version='1.0.0',
      description='Servicio de ubicacion del sistema de inventario',
      author='Carlos Cercado, Nidia Cabello, Fabiola Marin',
      author_email='cercadocarlos@gmail.com',
      packages=['ubicacion'],
      install_requires=[
       "Flask==0.12.2",
       "Flask-Classy==0.6.10",
       "WTForms==2.1",
       "peewee==2.10.1",
       "psycopg2==2.7.1",
       "Flask-Cors==3.0.3",
       "flake8==3.3.0",
       "WTForms-JSON==0.3.3",
       "PyJWT==1.5.2"
      ])
