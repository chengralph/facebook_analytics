import os, sys
import json
import datetime
from datetime import datetime
import csv
import unicodedata
import pandas as pd
import plotly.graph_objects as go

directory = os.path.join(os.getcwd(), "messages")
folders = os.listdir(directory)

def write_to_csv():
    with open("output.csv", "a") as csv_file:
        headers = ["Date", "Sender Name", "Type", "Content", "Photos", "Videos", "Call Duration"]
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(headers)
        for folder in folders:
            absolute_directory = os.path.join(directory, folder)
            for filename in os.listdir(absolute_directory):
                if filename.endswith(".json"):
                    absolute_file_path = os.path.join(absolute_directory, filename)
                    data = json.load(open(absolute_file_path, "r+"))
                    for message in data["messages"]:

                        date = datetime.fromtimestamp(message.get("timestamp_ms", 0) / 1000).strftime("%Y-%m-%d %H:%M:%S")
                        sender = message.get("sender_name")
                        type = message.get("type")
                        photos = str("photos" in message)  #type: generic
                        videos = str("videos" in message) #type: generic
                        content = message.get("content", "")  #fuck u \u123 (<3)
                        call_duration = int(message.get("call_duration", 0))
                        normalized_content = unicodedata.normalize('NFKD', content).encode('ascii','ignore')
                        writer.writerow([date,sender,type, normalized_content, photos, videos, call_duration])


df = pd.read_csv("output.csv")

def convert_date(date_time_str):
    date_time_object = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
    return date_time_object

def strip_date(date_time_str):
    return date_time_str.split(" ")[0]

date_index_0 =  df["Date"].iloc[0]
date_index_1 = df["Date"].iloc[-1]

number_of_days_spanned = convert_date(date_index_0) - convert_date(date_index_1)

date_group_by = df.groupby(lambda x: strip_date(df["Date"].iloc[x]))
number_of_days_interacted = len(date_group_by)

number_of_messages = len(df[(df["Type"]=="Generic") | (df["Type"]=="Share")])
number_of_texts = len(df[(df["Type"]=="Generic") & (df["Photos"]==0) & (df["Videos"]==0)])
number_of_photos = len(df[(df["Photos"]>0)])
number_of_photos = len(df[(df["Photos"]>0)])
series_number_of_calls = date_group_by.apply(lambda x: len(x[x["Type"]=="Call"]))
number_of_calls = len(series_number_of_calls.to_numpy().nonzero()[0])
sum_of_call_duration = int(df["Call Duration"].sum() / 3600)

stat_table = f"""
Number of Days Spanned: {number_of_days_spanned.days}
Number of Days Interacted: {number_of_days_interacted}
Numbers of Messages Sent: {number_of_messages}
Number of Texts Sent: {number_of_texts}
Number of Photos Sent: {number_of_photos}
Number of Days Video Called: {number_of_calls}
Hours Spent Talked: {sum_of_call_duration}
Average Call Duration Per Day Called(hours): {(sum_of_call_duration/number_of_calls):.2f}
"""
print(stat_table)

series_message = date_group_by.apply(lambda x: len(x[(x["Type"]=="Generic") | (x["Type"]=="Share")]))

graph1_x_axis = series_message.keys()
graph1_y_axis = series_message.values


fig = go.Figure()
fig.add_trace(go.Scatter(x=graph1_x_axis, y = graph1_y_axis, line=dict(color='firebrick', width=4)))

fig.update_layout(title="Messages Sent Per Day", xaxis_title="Date", yaxis_title="Number of Messages") # xaxis=dict(title="Hello", type='category')
fig.update_layout({'plot_bgcolor': 'rgba(1,1,1,0)’, 'paper_bgcolor': 'rgba(0,0,0,0)'})
fig.show()


series_call = date_group_by["Call Duration"].sum()/3600
graph2_x_axis = series_call.keys()
graph2_y_axis = series_call.values

fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=graph2_x_axis, y = graph2_y_axis, line=dict(color='royalblue', width=4)))

fig2.update_layout(title="Video Call Duration Per Day", xaxis_title="Date", yaxis_title="Duration of Calls(hours)") # xaxis=dict(title="Hello", type='category')
fig2.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)', 'paper_bgcolor': 'rgba(0,0,0,0)'})
fig2.show()




sender_groupby = df.groupby("Sender Name")
sender_name_list = list(sender_groupby.groups.keys())
sender_name_1 = sender_name_list[0]
sender_name_2 = sender_name_list[1]

sender1_value = len(df[(df["Sender Name"]==sender_name_1)])
sender2_value = len(df[(df["Sender Name"]==sender_name_2)])

pie_chart1_labels = ["Ralph","Nicole"]
pie_chart1_values = [sender1_value, sender2_value]

pie_chart1 = go.Figure(data=[go.Pie(labels=pie_chart1_labels, values=pie_chart1_values)])
pie_chart1.show()

"""
Generic: Photo/Video/Text
Share: Attachment/Video
Call: Video Call

Pandas for csv coounting/data manipulation
Stats:
    +Days Spanned: diff of dates
    +Days Messaged: messaged dates
    +Messages Sent:  Generic + Share
    +Texts Sent:    Generic + Photo False + Video False
    +Photos Sent:   Photo True
    +Days Video Calls:  Group call date
    +Minutes talking: Sum(call_duration)
    + Average call duration per day(Call duration/Number of days spanned or Call duration/Number of days called)

plotly:

    Graph 1: Total Message Line graph Sept-July (Nicole, Ralph) Generic + Share
    Graph 2: Duration is Video Call Line graph sept-july (Nicole, Ralph) Sum of video call per day
    Graph 3: Average messages Sent over 24hours
    Pie Chart 1: Messages  (Nicole, Ralph) Generic + Share
    Pie Chart 2: Types of messages (Ralph)   Photo true, Video true, Generic + false + false, type = attachemnt=share
    Pie Chart 3: Types of messages (Nicole)  Photo true, Video true, Generic + false + false, type = attachemnt=share


"""
