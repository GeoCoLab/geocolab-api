from . import home, auth, misc, forms, blog, analysis, application, facility, offer, org, slot


def init_app(app):
    blueprints = [home.bp, auth.bp, misc.bp, forms.bp, blog.bp, analysis.bp, application.bp, facility.bp, offer.bp,
                  org.bp, slot.bp]

    for bp in blueprints:
        app.register_blueprint(bp)
