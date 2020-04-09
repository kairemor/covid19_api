import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as snb
# from matplotlib import ticker
import pycountry_convert as pc
# import folium
from datetime import datetime, date, timedelta
# from scipy.interpolate import make_interp_spline, BSpline
import os
import subprocess

# Defininng Function for getting continent code for country.


def country_to_continent_code(country):
    try:
        return pc.country_alpha2_to_continent_code(pc.country_name_to_country_alpha2(country))
    except:
        return 'na'


def data_processing():
    yesterday = datetime.today() - timedelta(days=1)
    today = yesterday.strftime('%m-%d-%Y')
    url = 'data/'+today+".csv"
    df = pd.read_csv(url)

    df = df.rename(
        columns={"Province_State": "state", "Country_Region": "country"})

    df.loc[df['country']
           == "US", "country"] = "United States"

    df.loc[df['country'] == 'Korea, South', "country"] = 'South Korea'

    df.loc[df['country'] == 'Taiwan*', "country"] = 'Taiwan'

    df.loc[df['country'] ==
           'Congo (Kinshasa)', "country"] = 'Democratic Republic of the Congo'

    df.loc[df['country'] ==
           "Cote d'Ivoire", "country"] = "Côte d'Ivoire"

    df.loc[df['country'] == "Reunion", "country"] = "Réunion"

    df.loc[df['country'] ==
           'Congo (Brazzaville)', "country"] = 'Republic of the Congo'

    df.loc[df['country'] == 'Bahamas, The', "country"] = 'The Bahamas'

    df.loc[df['country'] == 'Gambia, The', "country"] = 'The Gambia'

    df.loc[df['country'] == 'United States', 'Active'] = df.loc[df['country'] == 'United States', 'Confirmed'] - \
        df.loc[df['country'] == 'United States', 'Deaths'] - \
        df.loc[df['country'] == 'United States', "Recovered"]

    # getting all countries
    countries = np.asarray(df["country"])
    # Continent_code to Continent_names
    continents = {
        'NA': 'North America',
        'SA': 'South America',
        'AS': 'Asia',
        'OC': 'Australia',
        'AF': 'Africa',
        'EU': 'Europe',
        'na': 'Others'
    }

    # Collecting Continent Information
    df.insert(2, "continent", [
        continents[country_to_continent_code(country)] for country in countries[:]])

    return (df, continents)


def data_preprocessing():
    url1 = "data/time_series_covid19_confirmed_global.csv"
    url2 = "data/time_series_covid19_deaths_global.csv"
    url3 = "data/time_series_covid19_recovered_global.csv"
    url4 = "data/cases_country.csv"

    df_confirmed = pd.read_csv(url1)
    df_deaths = pd.read_csv(url2)
    df_recovered = pd.read_csv(url3)
    df_covid19 = pd.read_csv(url4)

    df_confirmed = df_confirmed.rename(
        columns={"Province/State": "state", "Country/Region": "country"})
    df_deaths = df_deaths.rename(
        columns={"Province/State": "state", "Country/Region": "country"})
    df_recovered = df_recovered.rename(
        columns={"Province/State": "state", "Country/Region": "country"})

    # Changing the conuntry names as required by pycountry_convert Lib
    df_confirmed.loc[df_confirmed['country']
                     == "US", "country"] = "United States"
    df_deaths.loc[df_deaths['country'] == "US", "country"] = "United States"
    df_recovered.loc[df_recovered['country']
                     == "US", "country"] = "United States"

    df_confirmed.loc[df_confirmed['country'] ==
                     'Korea, South', "country"] = 'South Korea'
    df_deaths.loc[df_deaths['country'] ==
                  'Korea, South', "country"] = 'South Korea'
    df_recovered.loc[df_recovered['country'] ==
                     'Korea, South', "country"] = 'South Korea'

    df_confirmed.loc[df_confirmed['country']
                     == 'Taiwan*', "country"] = 'Taiwan'
    df_deaths.loc[df_deaths['country'] == 'Taiwan*', "country"] = 'Taiwan'
    df_recovered.loc[df_recovered['country']
                     == 'Taiwan*', "country"] = 'Taiwan'

    df_confirmed.loc[df_confirmed['country'] ==
                     'Congo (Kinshasa)', "country"] = 'Democratic Republic of the Congo'
    df_deaths.loc[df_deaths['country'] ==
                  'Congo (Kinshasa)', "country"] = 'Democratic Republic of the Congo'
    df_recovered.loc[df_recovered['country'] ==
                     'Congo (Kinshasa)', "country"] = 'Democratic Republic of the Congo'

    df_confirmed.loc[df_confirmed['country'] ==
                     "Cote d'Ivoire", "country"] = "Côte d'Ivoire"
    df_deaths.loc[df_deaths['country'] ==
                  "Cote d'Ivoire", "country"] = "Côte d'Ivoire"
    df_recovered.loc[df_recovered['country'] ==
                     "Cote d'Ivoire", "country"] = "Côte d'Ivoire"

    df_confirmed.loc[df_confirmed['country']
                     == "Reunion", "country"] = "Réunion"
    df_deaths.loc[df_deaths['country'] == "Reunion", "country"] = "Réunion"
    df_recovered.loc[df_recovered['country']
                     == "Reunion", "country"] = "Réunion"

    df_confirmed.loc[df_confirmed['country'] ==
                     'Congo (Brazzaville)', "country"] = 'Republic of the Congo'
    df_deaths.loc[df_deaths['country'] ==
                  'Congo (Brazzaville)', "country"] = 'Republic of the Congo'
    df_recovered.loc[df_recovered['country'] ==
                     'Congo (Brazzaville)', "country"] = 'Republic of the Congo'

    df_confirmed.loc[df_confirmed['country'] ==
                     'Bahamas, The', "country"] = 'The Bahamas'
    df_deaths.loc[df_deaths['country'] ==
                  'Bahamas, The', "country"] = 'The Bahamas'
    df_recovered.loc[df_recovered['country'] ==
                     'Bahamas, The', "country"] = 'The Bahamas'

    df_confirmed.loc[df_confirmed['country'] ==
                     'Gambia, The', "country"] = 'The Gambia'
    df_deaths.loc[df_deaths['country'] ==
                  'Gambia, The', "country"] = 'The Gambia'
    df_recovered.loc[df_recovered['country'] ==
                     'Gambia, The', "country"] = 'The Gambia'

    # getting all countries
    countries = np.asarray(df_confirmed["country"])
    # Continent_code to Continent_names
    continents = {
        'NA': 'North America',
        'SA': 'South America',
        'AS': 'Asia',
        'OC': 'Australia',
        'AF': 'Africa',
        'EU': 'Europe',
        'na': 'Others'
    }

    # Collecting Continent Information
    df_confirmed.insert(2, "continent", [
                        continents[country_to_continent_code(country)] for country in countries[:]])
    df_deaths.insert(2, "continent",  [
                     continents[country_to_continent_code(country)] for country in countries[:]])
    df_recovered.insert(2, "continent",  [
                        continents[country_to_continent_code(country)] for country in countries[:]])

    df_confirmed = df_confirmed.replace(np.nan, '', regex=True)
    df_deaths = df_deaths.replace(np.nan, '', regex=True)
    df_recovered = df_recovered.replace(np.nan, '', regex=True)

    # getting country wise data
    confirmed_cases = df_confirmed.groupby(["country"]).sum().drop(
        ['Lat', 'Long'], axis=1).iloc[:, -1]
    recovered_cases = df_recovered.groupby(["country"]).sum().drop(
        ['Lat', 'Long'], axis=1).iloc[:, -1]
    deaths = df_deaths.groupby(["country"]).sum().drop(
        ['Lat', 'Long'], axis=1).iloc[:, -1]
    # active_cases = df_active.groupby(["country"]).sum().drop(['Lat','Long'],axis =1).iloc[:,-1]

    confirmed_cases.name = "Confirmed Cases"
    recovered_cases.name = "Recovered Cases"
    deaths.name = "Deaths Reported"
    # active_cases.name = "Active Cases"
    # df_countries_cases = pd.DataFrame([confirmed_cases,recovered_cases,deaths,active_cases]).transpose()
    df_countries_cases = pd.DataFrame(
        [confirmed_cases, recovered_cases, deaths]).transpose()

    # getting continent wise data
    confirmed_cases = df_confirmed.groupby(["continent"]).sum().drop(
        ['Lat', 'Long'], axis=1).iloc[:, -1]
    recovered_cases = df_recovered.groupby(["continent"]).sum().drop(
        ['Lat', 'Long'], axis=1).iloc[:, -1]
    deaths = df_deaths.groupby(["continent"]).sum().drop(
        ['Lat', 'Long'], axis=1).iloc[:, -1]
    # active_cases = df_active.groupby(["continent"]).sum().drop(['Lat','Long'],axis =1).iloc[:,-1]

    confirmed_cases.name = "Confirmed Cases"
    recovered_cases.name = "Recovered Cases"
    deaths.name = "Deaths Reported"
    # active_cases.name = "Active Cases"
    # df_continents_cases = pd.DataFrame([confirmed_cases,recovered_cases,deaths,active_cases]).transpose()
    df_continents_cases = pd.DataFrame(
        [confirmed_cases, recovered_cases, deaths]).transpose()

    return (df_confirmed, df_deaths, df_recovered, df_continents_cases, df_countries_cases)


def process_day_data(df):
    df = df.groupby('country').sum()

    df = df[df['Confirmed'] > 0]
    df['recovery_rate'] = df.apply(lambda x: x.Recovered/x.Confirmed, axis=1)
    df['death_rate'] = df.apply(lambda x: x.Deaths/x.Confirmed, axis=1)
    return df


def get_graph_data(pays=None):
    url = "data/time_series_covid19_confirmed_global.csv"
    url2 = "data/time_series_covid19_deaths_global.csv"
    url3 = "data/time_series_covid19_recovered_global.csv"

    df_confirmed = pd.read_csv(url)
    df_recovered = pd.read_csv(url3)
    df_deaths = pd.read_csv(url2)

    if pays:
        df_confirmed = df_confirmed[df_confirmed['Country/Region'] == pays]
        df_recovered = df_recovered[df_recovered['Country/Region'] == pays]
        df_deaths = df_deaths[df_deaths['Country/Region'] == pays]
    columns_name = [str(column)[:4]
                    for column in df_confirmed.columns if str(column).endswith('20')]
    columns_length = len(columns_name)
    number_of_point = 10
    step = columns_length // number_of_point

    columns_name.reverse()

    taked_name = [columns_name[(i*step)] for i in range(number_of_point)]
    taked_name.reverse()

    df2_confirmed = df_confirmed.sum()
    df2_recovered = df_recovered.sum()
    df2_deaths = df_deaths.sum()

    values_confirmed = list(df2_confirmed[4:].values)
    values_confirmed.reverse()

    values_recovered = list(df2_recovered[4:].values)
    values_recovered.reverse()

    values_deaths = list(df2_deaths[4:].values)
    values_deaths.reverse()
    taked_value_confirmed = [
        values_confirmed[(i*step)] for i in range(number_of_point)]
    taked_value_confirmed.reverse()

    taked_value_recovered = [
        values_recovered[(i*step)] for i in range(number_of_point)]
    taked_value_recovered.reverse()

    taked_value_deaths = [values_deaths[(i*step)]
                          for i in range(number_of_point)]
    taked_value_deaths.reverse()

    return (taked_name, taked_value_confirmed, taked_value_deaths, taked_value_recovered)


def initData():
    df_confirmed = pd.read_csv(
        "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")
    #df_recovery = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv")
    df_death = pd.read_csv(
        "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv")

    pays = set(df_confirmed['Country/Region'])
    columns_name = [str(column)[:4]
                    for column in df_confirmed.columns if str(column).endswith('20')]
    columns = []
    length_column = len(columns_name)
    for i in range(length_column):
        if i < (length_column - 5):
            if i % 3 == 0:
                columns.append(columns_name[i])
        else:
            columns.append(columns_name[i])

    columns_name = columns

    try:
        os.makedirs("image")
    except Exception:
        pass
    os.chdir("image")

    for pay in pays:
        print(pay)
        df2_confirmed = df_confirmed.loc[df_confirmed['Country/Region'] == pay].sum()
       #df2_recovery = df_recovery.loc[df_recovery['Country/Region'] == pay].sum()
        df2_death = df_death.loc[df_death['Country/Region'] == pay].sum()

        value_confirmed = df2_confirmed[4:]
        #value_recovery = df2_recovery[4:]
        value_death = df2_death[4:]

        values_confirmed = []
        #values_recovery = []
        values_death = []

        values_length = len(value_confirmed)
        for i in range(values_length):
            if i < (values_length - 5):
                if i % 3 == 0:
                    values_confirmed.append(value_confirmed[i])
                    # values_recovery.append(value_recovery[i])
                    values_death.append(value_death[i])
            else:
                values_confirmed.append(value_confirmed[i])
                # values_recovery.append(value_recovery[i])
                values_death.append(value_death[i])

        df1_confirmed = pd.DataFrame(
            {"jour_"+pay+"_Cas-Confirmes": columns_name, "value": values_confirmed})
        #df1_recovery = pd.DataFrame({"jour_"+pay+"_Gueris": columns_name, "value":values_recovery })
        df1_death = pd.DataFrame(
            {"jour_"+pay+"_Deces": columns_name, "value": values_death})

        fig = plt.figure(figsize=(10, 10))
        ax1 = fig.add_subplot(211)
        ax2 = fig.add_subplot(212)
        #ax3 = fig.add_subplot(313)

        snb.relplot(x="jour_"+pay+"_Cas-Confirmes", y="value",
                    data=df1_confirmed, ax=ax1, color="b")
        #snb.relplot(x="jour_"+pay+"_Gueris", y="value", data=df1_recovery, ax=ax3, color="g")
        snb.relplot(x="jour_"+pay+"_Deces", y="value",
                    data=df1_death, ax=ax2, color="r")

        #sns_plot.set_xticklabels(sns_plot.get_xticklabels(), rotation=45, horizontalalignment='right')
        fig.savefig(pay+".png")

    os.chdir("..")


def data_by_continent():
    df, continents = data_processing()
    print(df.columns)
    df_continent = df.groupby('continent').sum().drop(
        columns=['FIPS', 'Lat', 'Long_'])
    return (df_continent, continents)


def most_cas_country(n, continent=None):
    '''
    get the n country with the most confirmed cases 
    '''
    df, _ = data_processing()

    if(continent):
        df = df[df['continent'] == continent]
    df = process_day_data(df)
    df_country = df.drop(
        columns=['FIPS', 'Lat', 'Long_']).sort_values('Confirmed', ascending=False)[:n]
    return df_country


def most_death_country(n, continent=None):
    '''
    get the n country with the  most corona death case
    '''
    df, _ = data_processing()
    if(continent):
        df = df[df['continent'] == continent]
    df = process_day_data(df)
    df_country = df.drop(
        columns=['FIPS', 'Lat', 'Long_']).sort_values('Deaths', ascending=False)[:n]
    return df_country


def data_by_country(country):
    '''
    the country data
    '''
    df, _ = data_processing()
    df = process_day_data(df)
    df_country = df.loc[country]
    return df_country


def download_data():
    '''
    download the needded data from the github
    '''
    yesterday = datetime.today() - timedelta(days=1)
    today = yesterday.strftime('%m-%d-%Y')
    url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/"+today+".csv"
    url1 = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
    url2 = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
    url3 = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"
    url4 = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/web-data/data/cases_country.csv"
    try:
        os.makedirs('data')
    except Exception as e:
        pass
    os.chdir('data')
    try:
        for filename in os.listdir():
            os.remove(filename)
    except Exception:
        pass
    subprocess.call(['wget', url])
    subprocess.call(['wget', url1])
    subprocess.call(['wget', url2])
    subprocess.call(['wget', url3])
    subprocess.call(['wget', url4])
    os.chdir('..')


# if __name__ == "__main__":
#     initData()
