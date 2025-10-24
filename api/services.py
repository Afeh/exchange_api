import requests
import random
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from . import models, image_generator

COUNTRIES_API_URL="https://restcountries.com/v2/all?fields=name,capital,region,population,flag,currencies"
EXCHANGE_RATE_API_URL="https://open.er-api.com/v6/latest/USD"


class ExternalServiceError(Exception):
    def __init__(self, service_name: str, details: str):
        self.service_name = service_name
        self.details = details
        super().__init__(f"Could not fetch data from {self.service_name}")


def refresh_countries_data(db: Session):
    try:
        countries_response = requests.get(COUNTRIES_API_URL, timeout=10)
        if not countries_response.ok:
            raise ExternalServiceError("restcountries.com", countries_response.status_code)
        countries_data = countries_response.json()

        exchange_response = requests.get(EXCHANGE_RATE_API_URL, timeout=10)
        if not exchange_response.ok:
            raise ExternalServiceError("open.er-api.com", exchange_response.status_code)
        exchange_rates = exchange_response.json().get("rates", {})

    except requests.exceptions.RequestException as e:
        raise ExternalServiceError(str(e.request.url), 503) from e


    for country_data in countries_data:
        name = country_data.get("name")
        population = country_data.get("population")

        if not name or population is None:
            continue

        currency_code = None
        exchange_rate = None
        currencies = country_data.get("currencies")
        if currencies and isinstance(currencies, list) and len(currencies) > 0:
            currency_code = currencies[0].get("code")
            if currency_code:
                exchange_rate = exchange_rates.get(currency_code)


        estimated_gdp = 0
        if population and exchange_rate and exchange_rate > 0:
            multiplier = random.uniform(1000, 2000)
            estimated_gdp = (population * multiplier)/exchange_rate
        elif exchange_rate is None and currency_code is not None:
            estimated_gdp = None


        existing_country = db.query(models.Country).filter(models.Country.name == name).first()

        country_fields = {
            "capital": country_data.get("capital"),
            "region": country_data.get("region"),
            "population": population,
            "currency_code": currency_code,
            "exchange_rate": exchange_rate,
            "estimated_gdp": estimated_gdp,
            "flag_url": country_data.get("flag"),
        }

        if existing_country:
            for key, value in country_fields.items():
                setattr(existing_country, key, value)
        else:
            new_country = models.Country(name=name, **country_fields)
            db.add(new_country)

    now = datetime.now(timezone.utc)
    status = db.query(models.AppStatus).first()
    if status:
        status.last_refreshed_at = now
    else:
        db.add(models.AppStatus(last_refreshed_at=now))

    db.commit()

    total_countries = db.query(models.Country).count()
    top_5_countries = db.query(models.Country).filter(models.Country.estimated_gdp.isnot(None)).order_by(desc(models.Country.estimated_gdp)).limit(5).all()
    image_generator.generate_summary_image(total_countries, top_5_countries, now)

    return {"message": "Country data refreshed successfully."}
