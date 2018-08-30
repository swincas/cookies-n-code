#!/usr/bin/env python
#==============================================================================
#title           :GUI_codereview.py
#description     :A 'bokeh' based python code to create GUIs for visualization and data analysis.
#authors         :Aditya Parthasarathy 
#year            :2018
#version         :0.1
#usage           :bokeh serve GUI_codereview.py --args -csv <filename>
#notes           :
#python_version  :3.6.4
#==============================================================================


#General imports
import pandas as pd
import numpy as np
import os
import sys
import glob
import argparse

#Bokeh imports
from bokeh.plotting import figure
from bokeh.layouts import layout, widgetbox, column, row
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.models.widgets import RangeSlider, Select, TextInput,PreText, Button, DataTable, TableColumn
from bokeh.io import curdoc


#Creating a pandas dataframe from the input csv file
parser = argparse.ArgumentParser(description="Example GUI for CodeReview @ CAS")
parser.add_argument("-csv",dest="csvfile",help="Path to the csv file", required=True)
args=parser.parse_args()

if os.path.exists(str(args.csvfile)):
    df = pd.read_csv(str(args.csvfile))
else:
    print ("Enter a valid data source")
    sys.exit()


#Defining the axis_map
axis_map = {
        "Price": "price",
        "Speed": "speed",
        "Harddisk": "hd",
        "RAM": "ram",
        }


#Setting up the widgets
x_axis = Select(title="X axis", options=sorted(axis_map.keys()), value="Price")
y_axis = Select(title="Y axis", options=sorted(axis_map.keys()), value="Speed")
codefeedback = PreText(text="",width=900)
screen_size = RangeSlider(title="Screen size", start=df["screen"].min(),end=df["screen"].max(),value=(df["screen"].min(),df["screen"].max()),step=1)
ram_size = RangeSlider(title="RAM", start=df["ram"].min(),end=df["ram"].max(),value=(df["ram"].min(),df["ram"].max()),step=1)
price_range = RangeSlider(title="Price Range", start=df["price"].min(),end=df["price"].max(),value=(df["price"].min(),df["price"].max()),step=1)
speed_range = RangeSlider(title="Speed", start=df["speed"].min(),end=df["speed"].max(),value=(df["speed"].min(),df["speed"].max()),step=1)
textoutput = PreText(text="",width=300)

#Defining ColumnDataSources
mainsource=ColumnDataSource(data=dict(x=[],y=[]))
sel_datasource = ColumnDataSource(data=dict(price=[],speed=[],hd=[],ram=[],screen=[],cd=[],multi=[],premium=[],ads=[],trend=[]))

#Defining Hover Tools
defaults = 'pan,box_zoom,box_select,lasso_select,reset,wheel_zoom,tap,undo,redo,save'
hover_userdefined = HoverTool(tooltips=[('CD-Drive','@cd_drive'),('Multiprocessor','@multi_process'),('PremiumCompany','@prem_comp')])
TOOLS = [defaults,hover_userdefined]

#Plots
p1 = figure(plot_height=600, plot_width=800, title="Generic Scatter plot", tools=TOOLS)
scatter1 = p1.circle(x='x',y='y',source=mainsource,size=7)
p2 = figure(plot_height=400, plot_width=600, title="Adverts vs Trends", tools=defaults)
p2.xaxis.axis_label="Number of Adverts"
p2.yaxis.axis_label="Trends"
lines = p2.line(x='ads',y='trends',source=mainsource,line_width=2)

#DataTable
columns=[
        TableColumn(field="price", title="Price"),
        TableColumn(field="speed", title="Speed"),
        TableColumn(field="hd", title="HardDisk"),
        TableColumn(field="ram", title="RAM"),
        TableColumn(field="screen",title="Screen"),
        TableColumn(field="cd",title="CD"),
        TableColumn(field="multi",title="MultiProcessor"),
        TableColumn(field="premium",title="Premium"),
        TableColumn(field="ads",title="Adverts"),
        TableColumn(field="trend", title="Trends"),
        ]
data_table = DataTable(source=sel_datasource, columns=columns, width=800, height=600)

#Filtering data
def filter_data():
    fdata = df[
            (df["price"] >= price_range.value[0]) &
            (df["price"] <= price_range.value[1]) &
            (df["speed"] >= speed_range.value[0]) &
            (df["speed"] <= speed_range.value[1]) &
            (df["screen"] >= screen_size.value[0]) &
            (df["screen"] <= screen_size.value[1]) &
            (df["ram"] >= ram_size.value[0]) &
            (df["ram"] <= ram_size.value[1])
            ]
    return fdata

#Callback routines
def update_gui():
    codefeedback.text="Welcome to CodeReview. Let's get started! You've loaded {0}.\n The columns are : {1}".format(args.csvfile,df.columns.values)
    data = filter_data()
    p1.xaxis.axis_label = x_axis.value
    p1.yaxis.axis_label = y_axis.value
    x_name=axis_map[x_axis.value]
    y_name=axis_map[y_axis.value]
    mainsource.data = dict(x=data[x_name],y=data[y_name],cd_drive=data["cd"],multi_process=data["multi"],prem_comp=data["premium"],ads=data["ads"],trends=data["trend"])

#Selected data
def update_selected(attr,old,new):
    inds = np.array(new['1d']['indices'])
    data = filter_data()
    sel_datasource.data = dict(price=data["price"].iloc[inds],speed=data["speed"].iloc[inds],hd=data["hd"].iloc[inds],ram=data["ram"].iloc[inds],screen=data["screen"].iloc[inds],cd=data["cd"].iloc[inds],multi=data["multi"].iloc[inds],premium=data["premium"].iloc[inds],ads=data["ads"].iloc[inds],trend=data["trend"].iloc[inds])
    textoutput.text= "Ah ha! - You've selected the \n {0} index in your dataset".format(inds)


#Callbacks for selected data points
scatter1.data_source.on_change('selected', update_selected)

#Widget callbacks
controls = [x_axis,y_axis]
for control in controls:
    control.on_change('value', lambda attr,old,new: update_gui())

rangesliders = [screen_size,ram_size,price_range,speed_range]
for slider in rangesliders:
    slider.on_change('value', lambda attr, old, new: update_gui())

#Widgetboxes
axes = widgetbox(*controls, sizing_mode='fixed')
sliders = widgetbox(*rangesliders, sizing_mode='fixed')
data_table_input = widgetbox(data_table,sizing_mode='fixed')

#Defining the layout for the GUI
filtering = column([axes,sliders,textoutput])

#Layout
gui_layout = layout([codefeedback],
                    [filtering,p1],
                    [p2,data_table_input],sizing_mode='fixed')

update_gui()

curdoc().add_root(gui_layout)
curdoc().title = "GUI_CodeReview"

