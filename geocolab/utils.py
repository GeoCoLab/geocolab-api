from geonamescache import GeonamesCache

countries_cache = GeonamesCache().get_countries()
countries = [(c[0], c[1]['name']) for c in countries_cache.items()]
currencies = list(
    set([(c[1]['currencycode'], f"{c[1]['currencyname']} ({c[1]['currencycode']})") for c in countries_cache.items() if c[1]['currencycode'] != '']))


def init_app(app):
    @app.template_filter('country_name')
    def country_name(iso_code):
        return countries_cache.get(iso_code)['name']
