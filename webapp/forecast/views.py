from flask import abort, Blueprint, current_app, flash, render_template, redirect, request, url_for
import plotly
import pandas as pd
import plotly.graph_objects as go
import json
blueprint = Blueprint('forecast', __name__)

#Need to make model.py for this
pie_chart_data = pd.read_csv('https://gist.githubusercontent.com/Konstantin-Parfenov/b1f3bbaf0cc8cf75921a9070954e7723/raw/bb3e21f7424fb882ef224ba5ca66779ad6a0d520/weights.csv')
forecast_chrt_data = pd.read_csv('https://gist.githubusercontent.com/Konstantin-Parfenov/b1f3bbaf0cc8cf75921a9070954e7723/raw/bb3e21f7424fb882ef224ba5ca66779ad6a0d520/submissions.csv')

def create_plot_pie():

    data = [
        go.Pie(
            
            labels=pie_chart_data['feature'],
            values=pie_chart_data['weight']
        )
    ]

    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON



def create_plot_forecast(avg_type):
    #default SMA
    period=60
    roll=21
    roll_func= avg_type 
    function='mean'
    trace=go.Scatter(
        x=forecast_chrt_data.date.iloc[-period:],
        y=forecast_chrt_data.pet.iloc[-period:]
    )
    if roll_func=='EMA':
        y=forecast_chrt_data.pet.ewm(span=roll).agg(function).iloc[-period:]
    if roll_func=='SMA':
        y=forecast_chrt_data.pet.rolling(roll).agg(function).iloc[-period:]
    trace1=go.Scatter(
        x=forecast_chrt_data.date.iloc[-period:],
        y=y
    )
    fig=go.Figure(data=[trace,trace1])

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON
    


@blueprint.route('/forecast_pie', methods = ['GET','POST'])
def forecast_pie():
    pie_chart_weights = create_plot_pie()
    return render_template('forecast/piechart.html', plot_pie_chart_weights = pie_chart_weights )


@blueprint.route('/forecast_chart/<avg_type_main>', methods = ['GET','POST'])
def forecast_chart(avg_type_main):
    avg_type=avg_type_main
    forecast_chart = create_plot_forecast(avg_type)
    return render_template('forecast/forecast.html', plot_forecast_chart = forecast_chart , avg_type = avg_type_main)
