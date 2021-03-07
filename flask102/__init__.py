
import os

from flask import Flask




def create_app(test_config=None):
    app=Flask(__name__,instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flask102.sqlite'),
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    @app.route('/hello')
    def main():
        return 'hello world'

    from . import db
    db.init_app(app)

    from . import index
    app.register_blueprint(index.bp)

    return app


# to run go to parent dir, not this package dir and issue flask run
# to initialize database run $ flask init-db