import click
from flask.cli import FlaskGroup

from . import create_app
from .extensions import db
from .models import User


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
@click.option('--pw')
def make_admin(email, pw):
    if email:
        user = User.query.filter_by(email=email).one_or_none()
        if not user:
            click.echo(f'User "{email}" does not exist.', err=True)
            raise click.Abort
    else:
        user = User.query.filter_by(email='admin').one_or_none()
        if not user:
            user = User(email='admin', given_name='Admin', family_name='Istrator', country='GB')
            user.password_set(pw)
            db.session.add(user)
            db.session.commit()
    user.role = 'admin'
    db.session.commit()
    click.echo(f'Updated {email or "admin"}.')


if __name__ == '__main__':
    cli()
