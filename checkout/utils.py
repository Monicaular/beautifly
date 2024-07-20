import pycountry

def get_iso_country_code(country_name):
    try:
        country = pycountry.countries.lookup(country_name)
        return country.alpha_2
    except LookupError:
        return 'GB'