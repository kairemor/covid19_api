import os
from flask import Flask, send_from_directory
from flask_restplus import Api, Resource
from datetime import datetime, timedelta
import pandas as pd


from data import *

image_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'image')

app = Flask(__name__)
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

        for country in continents.values():
            data.append({country: {
                'confirmed': str(df.loc[country, 'Confirmed']),
                'recovery': str(df.loc[country, 'Recovered']),
                'death': str(df.loc[country, 'Deaths']),
                'active': str(df.loc[country, 'Active'])
            }})
        # print(data)
        return data


@country_data.route("/")
class CountryDataList(Resource):
    def get(self):
        yesterday = datetime.today() - timedelta(days=1)
        today = yesterday.strftime('%m-%d-%Y')
        # url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/"+today+".csv"
        url = 'data/'+today+".csv"
        df = pd.read_csv(url)
        death = df.Deaths.sum()
        confirmed = df.Confirmed.sum()
        recovery = df.Recovered.sum()
        active = df.Active.sum()
        last_update = df.Last_Update.values[0]
        data = {'confirmed': str(confirmed), 'death': str(death), 'recovery': str(
            recovery), 'last_updated': str(last_update), 'active': str(active)}
        return data


@country_data.route("/most-confirmed/<int:n>")
class MostCaseCountry(Resource):
    def get(self, n):
        df = most_cas_country(n)
        data = []

        for country in df.index:
            data.append({country: {
                'confirmed': str(df.loc[country, 'Confirmed']),
                'recovery': str(df.loc[country, 'Recovered']),
                'death': str(df.loc[country, 'Deaths']),
                'active': str(df.loc[country, 'Active'])
            }})
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
        yesterday = datetime.today() - timedelta(days=1)
        today = yesterday.strftime('%m-%d-%Y')
        url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/"+today+".csv"
        df = pd.read_csv(url)
        df = df[df['Country_Region'] == country]
        death = df.Deaths.sum()
        confirmed = df.Confirmed.sum()
        recovery = df.Recovered.sum()
        active = df.Active.sum()
        last_update = df.Last_Update.values[0]
        data = {'confirmed': str(confirmed), 'death': str(death), 'recovery': str(
            recovery), 'last_updated': str(last_update), 'active': str(active)}
        return data


if __name__ == "__main__":
    app.run(host='0.0.0.0')
