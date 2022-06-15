import click
from flask.cli import FlaskGroup

from . import create_app
from .extensions import db
from .models import User, Secret


def create_cli_app():
    app = create_app()

    @app.shell_context_processor
    def make_shell_context():
        return {'app': app, 'db': db}

    return app


@click.group(cls=FlaskGroup, create_app=create_cli_app)
def cli():
    """
    CLI for geocolab.
    """
    pass


@cli.command()
@click.option('--email')
def make_admin(email):
    if email:
        user = User.query.filter_by(email=email).one_or_none()
        if not user:
            click.echo(f'User "{email}" does not exist.', err=True)
            raise click.Abort
    else:
        user = User.query.filter_by(email='admin').one_or_none()
        if not user:
            user = User(email='admin', given_name='GeoCoLab', family_name='Admin', country='GB')
            user.password_set(click.prompt('Password', hide_input=True))
            db.session.add(user)
            db.session.commit()
    user.role = 'admin'
    db.session.commit()
    click.echo(f'Updated {email or "admin"}.')


@cli.command()
@click.argument('key')
def set_secret(key):
    secret = Secret.query.filter_by(key=key).one_or_none()
    if not secret:
        secret = Secret(key=key)
        db.session.add(secret)
    secret.value_set(click.prompt('Secret value', hide_input=True))
    db.session.commit()


if __name__ == '__main__':
    cli()
