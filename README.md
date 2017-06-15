# Parlalize

Where the magic happens. Parlalize requests data from Parladata every 24 hours and runs all the calculations. It provides the data through a JSON API.

## Parlalize API

The Parlalize API serves calculated and organized data and metrics. The calculations are performed on data accessible at the Parladata API endpoint. Most of the metrics are calculated every 24 hours or less with a few notable exceptions. If you want to access the data as it was calculated on a given day, append the date (localized to slovenian) behind the last slash in your query. The API is organized like Parladata but enforces grouping for endpoint URLs. /p for MPs, /pg for parliamentary groups, and /s for sessions.

### API documentation

https://dev.parlameter.si/doc/parlalize/

## Installation

This is your typical Django app. Copy `settings.sample.py` to `settings.py` and edit accordingly. After you're set up and you've installed all the requirements (we suggest you use `virtualenv` and `pip`) run `python manage.py runserver` and enjoy.

## Bug reports and feature requests

Please submit an issue if you find anything out of order or wish for anything to happen.
