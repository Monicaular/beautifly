import pycountry


def get_iso_country_code(country_name):
    """
    Return the ISO 3166-1 alpha-2 country code for the given country name.

    If the country name cannot be found, return 'GB' as the default.
    """
    try:
        country = pycountry.countries.lookup(country_name)
        return country.alpha_2
    except LookupError:
        return "GB"
