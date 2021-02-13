
import pandas as pd
import xlsxwriter
import plotly.offline as pyo
import plotly.graph_objs as go
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_auth
from Google import Create_Service
from googleapiclient.http import MediaFileUpload
# from pydrive.auth import GoogleAuth
# from pydrive.drive import GoogleDrive
from dash.dependencies import Input, Output

from functools import reduce

# def main():

workbook = xlsxwriter.Workbook('Covid19Dataset.xlsx')
worksheet = workbook.add_worksheet()

df = pd.read_excel('time_series_covid_19_confirmed.xlsx')
df = df.drop(columns=['Lat','Long'])
df2 = pd.read_excel('time_series_covid_19_deaths.xlsx')
df2 = df2.drop(columns=['Lat','Long'])
df3 = pd.read_excel('time_series_covid_19_recovered.xlsx')
df3 = df3.drop(columns=['Lat','Long'])

df_series = df.max(axis=1)
df.drop(df.columns.difference(['Country/Region']), 1, inplace=True)
df['Confirmed'] = df_series

# df_out = pd.DataFrame()

df_series = df2.max(axis=1)
df2.drop(df2.columns.difference(['Country/Region']), 1, inplace=True)
df2['Deaths'] = df_series

df_series = df3.max(axis=1)
df3.drop(df3.columns.difference(['Country/Region']), 1, inplace=True)
df3['Recovered'] = df_series

df = df.merge(df2, on = "Country/Region", how = "outer")
df = df.merge(df3, on = "Country/Region", how = "outer")

df['Active'] = df['Confirmed'] - df['Recovered'] - df['Deaths']
# df_out['primary_key'] = []
# df_out['confirmed_cases'] = []
# df_out['deaths'] = []
# df_out['recovered_cases'] = []

# dfs = [df, df2, df3]
# df = df[["Province/State", "Country/Region"]]
# df_out['primary_key']=df[['Province/State','Country/Region']].values.tolist()
# df_out['primary_key']=df_out['primary_key'].apply(''.join)

# df_series = df[["Province/State", "Country/Region"]]
# df_series = pd.concat([df.iloc[:,1]+(' ')+df.iloc[:,0]]).rename('primary_key').fillna(df.iloc[:,1]).to_frame()
# deaths = df2[["Province/State", "Country/Region"]]
# deaths_key = pd.concat([deaths.iloc[:,1]+(' ')+deaths.iloc[:,0]]).rename('deaths_cases').fillna(deaths.iloc[:,1]).to_frame()
# recovered = df3[["Province/State", "Country/Region"]]
# recovered_key = pd.concat([recovered.iloc[:,1]+(' ')+recovered.iloc[:,0]]).rename('recovered_cases').fillna(recovered.iloc[:,1]).to_frame()

# primary_key = df[["Province/State", "Country/Region"]].merge(df2[["Province/State",
#                                                                   "Country/Region"]],
#                                                              on = "Country/Region",
#                                                              how = "right")

# join = pd.concat(primary_key)
# print(join.head(10))
# join.to_excel('primary key.xlsx')
#
# df["primary key"].to_excel('primary.xlsx')

# key = pd.concat([confirmed.iloc[:,1]+(' ')+confirmed.iloc[:,0]]).rename('Primary_Key').fillna(confirmed.iloc[:,1])

# df = df.max(axis=1).to_frame()
# df2 = df2.max(axis=1).to_frame()
# df3 = df3.max(axis=1).to_frame()

#dataframe = df.key(columns= ["key", 'maxconfirmed', 'maxdeaths', 'maxrecovered'])

# df_out = reduce(lambda left,right: pd.merge(left,right,on='Country/Region'), dfs)
#
# df_out.drop(df_out.columns.difference(['Country/Region']), 1, inplace=True)


# for index, country in df_out.iterrows():
#     df_out.loc['confirmed_cases'] = df
# for confirmed in df_out.iterrows():
#     if df_out != df.loc[['Country/Region']]:
#         print(df)
writer = pd.ExcelWriter("Covid19.xlsx", engine='xlsxwriter')

df.to_excel(writer, sheet_name='Covid19_Analysis', index=False)

workbook = writer.book
worksheet = writer.sheets['Covid19_Analysis']

worksheet.set_column('A:A',30)
worksheet.set_column('B:E',10)

writer.save()

#GOOGLE DRIVE upload app

CLIENT_SECRET_FILE = 'client_secrets.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

folder_id = '1fgOX8hScgzxXEADZX9_yO462MMYtrKlJ'
file_names = ['Covid19.XLSX']
mime_types = ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']

for file_name, mime_type in zip(file_names, mime_types):
    file_metadata = {
        'name': file_name,
        'parents': [folder_id]
    }

    media = MediaFileUpload(filename=file_name, mimetype=mime_type)

    service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()

# gauth = GoogleAuth()
# gauth.LocalWebserverAuth
# drive = GoogleDrive(gauth)
#
# file1 = drive.CreateFile({'title':'Covid19.xlsx'})
# file1.SetContentFile(writer)
#
# file1.Upload()
                      #plotting using plotly and dassh
trace4 = go.Bar(
    x=df['Country/Region'],
    y=df['Confirmed'],
    name= 'Confirmed',
    marker=dict(color='#00cdcd')
)

trace3 = go.Bar(
    x=df['Country/Region'],
    y=df['Recovered'],
    name= 'Recovered',
    marker=dict(color='#eead0e')
)

trace2 = go.Bar(
    x=df['Country/Region'],
    y=df['Deaths'],
    name= 'Deaths',
    marker=dict(color='#ee6a50')
)

trace1 = go.Bar(
    x=df['Country/Region'],
    y=df['Active'],
    name= 'Active',
    marker=dict(color='#ff3030')
)

data = [trace1, trace2, trace3, trace4]
layout = go.Layout(
    title='Covid19 Summary for Each Country',
    barmode='stack'
)

USERNAME_PASSWORD_PAIRS = [['username','password'],['covid19','2019']]

country = df['Country/Region']

app = dash.Dash()
auth = dash_auth.BasicAuth(app,USERNAME_PASSWORD_PAIRS)

server = app.server

                    # Dash with all traces
app.layout = html.Div(children=[html.H1(children='Covid19 Analysis by Country'),
                                dcc.Graph(
                                    id='bar',
                                    figure = {
                                        'data':[trace1, trace2, trace3, trace4],
                                        'layout': go.Layout(title='Covid19 Summary for Each Country',
                                                            barmode='group',
                                                            xaxis= {'title': 'Country'},
                                                            yaxis={'title': 'Cases'}
                                                            )
                                    }
                                )]
                      )


if __name__ == '__main__':
    app.run_server()

# fig = go.Figure(data=data, layout=layout)
#
# fig['layout'].update(height=700)
#
# pyo.plot(fig, filename='Covid19 Summary for Each Country.html')
