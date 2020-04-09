import os
from flask import Flask, send_from_directory
from flask_restplus import Api, Resource
from datetime import datetime, timedelta
import pandas as pd
from flask_cors import CORS

from data import *

image_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'image')

app = Flask(__name__)
CORS(app)
api = Api(app=app)

ns_conf = api.namespace('conferences', description='Conference operations')
app_home = api.namespace('', description='Test if a api is working')
data_update = api.namespace('data', description="Update the data")
country_data = api.namespace(
    'country', description="get data for all contries or one countries ")
continent_data = api.namespace(
    'continent', description="get data by continent ")
graph_image = api.namespace(
    'graph', description="get a image where we have a three graph showing the progression of confirmed deaths and recovery cas of covid 19")
graph_data = api.namespace(
    'grapth_data', description="get a list of evolution of covid19 cases deaths and recovered ")


@app_home.route("/")
class Home(Resource):
    def get(self):
        return "working"


@data_update.route("/")
class Data(Resource):
    def get(self):
        download_data()
        return "updated"


@continent_data.route("/")
class ContinentDataList(Resource):
    def get(self):
        df, continents = data_by_continent()
        data = []

        for continent in continents.values():
            data.append({
                'continent': continent,
                'confirmed': str(df.loc[continent, 'Confirmed']),
                'recovery': str(df.loc[continent, 'Recovered']),
                'death': str(df.loc[continent, 'Deaths']),
                'active': str(df.loc[continent, 'Active']),
                'recovery_rate': str(df.loc[continent, 'Recovered'] / df.loc[continent, 'Confirmed']),
                'death_rate': str(df.loc[continent, 'Deaths'] / df.loc[continent, 'Confirmed']),
            })
        # print(data)
        return data


@country_data.route("/")
class CountryDataList(Resource):
    def get(self):
        df, _ = data_processing()
        death = df.Deaths.sum()
        confirmed = df.Confirmed.sum()
        recovery = df.Recovered.sum()
        active = df.Active.sum()
        # last_update = df.Last_Update.values[0]
        recovery_rate = recovery / confirmed
        death_rate = death / confirmed
        last_update = ''
        data = {'confirmed': str(confirmed), 'death': str(death), 'recovery': str(
            recovery), 'last_updated': str(last_update), 'active': str(active), 'recovery_rate': recovery_rate,
            'death_rate': death_rate
        }
        return data


@country_data.route("/most-confirmed/<int:n>")
class MostCaseCountry(Resource):
    def get(self, n):
        df = most_cas_country(n)
        data = []

        for country in df.index:
            data.append({
                'country': country,
                'confirmed': str(df.loc[country, 'Confirmed']),
                'recovery': str(df.loc[country, 'Recovered']),
                'death': str(df.loc[country, 'Deaths']),
                'active': str(df.loc[country, 'Active']),
                'recovery_rate': str(df.loc[country, 'recovery_rate']),
                'death_rate': str(df.loc[country, 'death_rate']),
            })
        # print(data)
        return data


@country_data.route("/most-death/<int:n>")
class MostDeathCountry(Resource):
    def get(self, n):
        df = most_death_country(n)
        data = []

        for country in df.index:
            data.append({
                'country': country,
                'confirmed': str(df.loc[country, 'Confirmed']),
                'recovery': str(df.loc[country, 'Recovered']),
                'death': str(df.loc[country, 'Deaths']),
                'active': str(df.loc[country, 'Active'])
            })

        return data


@country_data.route("/most-confirmed/<int:n>/<string:continent>")
class MostCaseCountryByContinent(Resource):
    def get(self, n, continent):
        df = most_cas_country(n, continent)
        data = []

        for country in df.index:
            data.append({
                'country': country,
                'confirmed': str(df.loc[country, 'Confirmed']),
                'recovery': str(df.loc[country, 'Recovered']),
                'death': str(df.loc[country, 'Deaths']),
                'active': str(df.loc[country, 'Active']),
                'recovery_rate': str(df.loc[country, 'recovery_rate']),
                'death_rate': str(df.loc[country, 'death_rate']),
            })
        # print(data)
        return data


@country_data.route("/most-death/<int:n>/<string:continent>")
class MostDeathCountryByContinent(Resource):
    def get(self, n, continent):
        df = most_death_country(n, continent)
        data = []
        for country in df.index:
            data.append({
                'country': country,
                'confirmed': str(df.loc[country, 'Confirmed']),
                'recovery': str(df.loc[country, 'Recovered']),
                'death': str(df.loc[country, 'Deaths']),
                'active': str(df.loc[country, 'Active'])
            })
        # print(data)
        return data


@graph_image.route("/<string:path>")
class GraphImage(Resource):
    def get(self, path):
        path = path.replace("é", "e")
        return send_from_directory(image_dir, path+'.png')


@country_data.route("/<string:country>")
class CountryDataOne(Resource):
    def get(self, country):
        df = data_by_country(country)
        death = df.Deaths
        confirmed = df.Confirmed
        recovery = df.Recovered
        active = df.Active
        last_update = ""
        # last_update = df.Last_Update.values[0]
        data = {'confirmed': str(confirmed),
                'death': str(death),
                'recovery': str(recovery),
                'last_updated': str(last_update),
                'active': str(active),
                'recovery_rate': df.recovery_rate,
                'death_rate': df.death_rate
                }
        return data


@graph_data.route("/")
class GraphListData(Resource):
    def get(self):
        column_name, values_confirmed, values_deaths, values_recovered = get_graph_data()

        values_confirmed = [str(int(value)) for value in values_confirmed]
        values_recovered = [str(int(value)) for value in values_recovered]
        values_deaths = [str(int(value)) for value in values_deaths]

        column_str = ",".join(column_name)
        values_confirmed_str = ",".join(values_confirmed)
        values_recovered_str = ",".join(values_recovered)
        values_deaths_str = ",".join(values_deaths)

        return {'columns': column_str, 'values_confirmed': values_confirmed_str, 'values_deaths': values_deaths_str, 'values_recovered': values_recovered_str}


@graph_data.route("/<string:country>")
class GraphListData(Resource):
    def get(self, country):
        column_name, values_confirmed, values_deaths, values_recovered = get_graph_data(
            country)

        values_confirmed = [str(int(value)) for value in values_confirmed]
        values_recovered = [str(int(value)) for value in values_recovered]
        values_deaths = [str(int(value)) for value in values_deaths]

        column_str = ",".join(column_name)
        values_confirmed_str = ",".join(values_confirmed)
        values_recovered_str = ",".join(values_recovered)
        values_deaths_str = ",".join(values_deaths)

        return {'columns': column_str, 'values_confirmed': values_confirmed_str, 'values_deaths': values_deaths_str, 'values_recovered': values_recovered_str}


if __name__ == "__main__":
    app.run(host='0.0.0.0')
