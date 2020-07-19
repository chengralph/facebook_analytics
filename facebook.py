import os, sys
import json
import datetime
from datetime import datetime
import csv
import unicodedata
import pandas as pd
import plotly.graph_objects as go
import warnings

class facebook:
    def write_to_csv(self, output_path="output.csv"):
        if not isinstance(output_path, str):
            raise TypeError("Hey name me a string bro")
        if not os.path.isfile(output_path):
            directory = os.path.join(os.getcwd(), "messages")
            folders = os.listdir(directory)
            with open(output_path, "a") as csv_file:
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
                                photos = str("photos" in message)
                                videos = str("videos" in message)
                                content = message.get("content", "")
                                call_duration = int(message.get("call_duration", 0))
                                normalized_content = unicodedata.normalize('NFKD', content).encode('ascii','ignore')
                                writer.writerow([date,sender,type, normalized_content, photos, videos, call_duration])

    def set_df(self, input_path="output.csv"):
        if type(input_path) != str:
            raise TypeError("Hey make me csv bro")
        self.df = pd.read_csv(input_path)

    def set_data(self):
        warnings.filterwarnings("ignore", 'This pattern has match groups')

        df = self.df

        date_index_0 =  df["Date"].iloc[0]
        date_index_1 = df["Date"].iloc[-1]
        self.number_of_days_spanned = convert_date(date_index_0) - convert_date(date_index_1)

        self.date_group_by = df.groupby(lambda x: strip_date(df["Date"].iloc[x]))
        self.ily_pattern = "(i?\s*love\s*you)|lubby|ily"

        self.number_of_days_interacted = len(self.date_group_by)
        self.number_of_messages = len(df[(df["Type"]=="Generic") | (df["Type"]=="Share")])
        self.number_of_texts = len(df[(df["Type"]=="Generic") & (df["Photos"]==0) & (df["Videos"]==0)])
        self.number_of_photos = len(df[(df["Photos"]>0)])
        self.number_of_videos = len(df[(df["Videos"]>0)])
        self.number_of_attachments = len(df[(df["Type"]=="Share")])
        self.series_number_of_calls = self.date_group_by.apply(lambda x: len(x[x["Type"]=="Call"]))
        self.number_of_calls = len(self.series_number_of_calls.to_numpy().nonzero()[0])
        self.sum_of_call_duration = int(df["Call Duration"].sum() / 3600)
        self.average_call_duration = self.sum_of_call_duration/self.number_of_calls
        self.number_of_ily = self.df["Content"].str.contains(self.ily_pattern).sum()

        self.series_message = self.date_group_by.apply(lambda x: len(x[(x["Type"]=="Generic") | (x["Type"]=="Share")]))
        self.series_call = self.date_group_by["Call Duration"].sum()/3600
        self.sender_groupby = df.groupby("Sender Name")
        self.series_sender = self.sender_groupby.apply(lambda x: x["Content"].str.contains(self.ily_pattern).sum())
        self.sender_name_list = list(self.sender_groupby.groups.keys())
        self.time_groupby = df.groupby(lambda x: get_time(df["Date"].iloc[x]))
        self.series_time = self.time_groupby.apply(len)

    def get_data_table(self):
        data_table = f"""
        Number of Days Spanned: {self.number_of_days_spanned.days}
        Number of Days Interacted: {self.number_of_days_interacted}
        Numbers of Messages Sent: {self.number_of_messages}
        Number of Texts Sent: {self.number_of_texts}
        Number of Photos Sent: {self.number_of_photos}
        Number of Videos Sent: {self.number_of_videos}
        Number of Attachemnts Sent: {self.number_of_attachments}
        Number of Days Video Called: {self.number_of_calls}
        Total Hours Video Called: {self.sum_of_call_duration}
        Average Call Duration Per Day Called(hours): {self.average_call_duration:.2f}
        Number of "I Love You's": {self.number_of_ily}
        """
        return data_table

    def plot_message_graph(self):
        graph_x_axis = self.series_message.keys()
        graph_y_axis = self.series_message.values

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=graph_x_axis, y = graph_y_axis, line=dict(color='firebrick', width=4)))

        fig.update_layout(title="Messages Sent Per Day", xaxis_title="Date", yaxis_title="Number of Messages")
        fig.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)', 'paper_bgcolor': 'rgba(0,0,0,0)'})
        fig.show()

    def plot_videocall_graph(self):
        graph_x_axis = self.series_call.keys()
        graph_y_axis = self.series_call.values

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=graph_x_axis, y = graph_y_axis, line=dict(color='royalblue', width=4)))

        fig.update_layout(title="Video Call Duration Per Day", xaxis_title="Date", yaxis_title="Duration of Calls(hours)")
        fig.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)', 'paper_bgcolor': 'rgba(0,0,0,0)'})
        fig.show()

    def plot_24hour_graph(self):
        graph_x_axis = self.series_time.keys()
        graph_y_axis = self.series_time.values

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=graph_x_axis, y = graph_y_axis, line=dict(color='black', width=4)))

        fig.update_layout(title="Average Messages Per 24hours", xaxis_title="Time", yaxis_title="Average Number of Messages")
        fig.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)', 'paper_bgcolor': 'rgba(0,0,0,0)'})
        fig.show()


    def plot_message_pie_chart(self):
        df = self.df
        pie_chart_labels = []
        pie_chart_values = []

        for i,_ in enumerate(self.sender_name_list):
            sender_name = self.sender_name_list[i]
            sender_value = len(df[(df["Sender Name"]==sender_name)])
            pie_chart_labels.append(sender_name)
            pie_chart_values.append(sender_value)
        colors = ["#fad9d3", "lightskyblue"]
        pie_chart = go.Figure(data=[go.Pie(labels=pie_chart_labels, values=pie_chart_values)])
        pie_chart.update_traces(hoverinfo='label+percent', textfont_size=20, textinfo='none',
                  marker=dict(colors=colors))
        pie_chart.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)', 'paper_bgcolor': 'rgba(0,0,0,0)'})
        pie_chart.update_layout(title_text = "Messages sent per sender")
        pie_chart.show()

    def plot_senders_pie_chart(self):
        pie_chart_labels = ["Photos", "Videos", "Plain Text", "Attachments"]
        pie_chart_values = []

        for i,_ in enumerate(self.sender_name_list):
            sender_name = self.sender_name_list[i]
            sender_name_photos = self.sender_groupby.apply(lambda x: len(x[x["Photos"]>0]))[i]
            sender_name_videos = self.sender_groupby.apply(lambda x: len(x[x["Videos"]>0]))[i]
            sender_name_plain_text = self.sender_groupby.apply(lambda x: len(x[(x["Type"]=="Generic") & (x["Photos"]==0) & (x["Videos"]==0)]))[i]
            sender_name_attachment = self.sender_groupby.apply(lambda x: len(x[x["Type"]=="Share"]))[i]
            pie_chart_values = [sender_name_photos, sender_name_videos, sender_name_plain_text, sender_name_attachment]
            colors = ["#3a63df", "#7357fd", "#fad9d3", "lightskyblue"]
            pie_chart = go.Figure(data=[go.Pie(labels=pie_chart_labels, values=pie_chart_values)])
            pie_chart.update_traces(hoverinfo='label+percent', textfont_size=20, textinfo='none', marker=dict(colors=colors))
            pie_chart.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)', 'paper_bgcolor': 'rgba(0,0,0,0)'})
            pie_chart.update_layout(title_text = sender_name)
            pie_chart.show()

    def plot_distribution_pie_chart(self):
        pie_chart_labels = ["Photos", "Plain Text", "Attachemnts", "Videos"]
        pie_chart_values = [self.number_of_photos, self.number_of_texts, self.number_of_attachments, self.number_of_videos]
        colors = ["lightskyblue", "#fad9d3", "#ffd480", "#b3b3ff"]
        pie_chart = go.Figure(data=[go.Pie(labels=pie_chart_labels, values=pie_chart_values)])
        pie_chart.update_traces(hoverinfo='label+percent', textfont_size=20, textinfo='none', marker=dict(colors=colors))
        pie_chart.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)', 'paper_bgcolor': 'rgba(0,0,0,0)'})
        pie_chart.update_layout(title_text = "Distrubution Chart")
        pie_chart.show()

    def plot_count_love_chart(self):
        df = self.df

        pie_chart_labels = []
        pie_chart_values = self.series_sender.values

        for i,_ in enumerate(self.sender_name_list):
            sender_name = self.sender_name_list[i]
            pie_chart_labels.append(sender_name)
        colors = ["#f1a29b", "#fad9d3"]
        pie_chart = go.Figure(data=[go.Pie(labels=pie_chart_labels, values=pie_chart_values)])
        pie_chart.update_traces(hoverinfo='label+percent', textfont_size=20, textinfo='none',
                  marker=dict(colors=colors))
        pie_chart.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)', 'paper_bgcolor': 'rgba(0,0,0,0)'})
        pie_chart.update_layout(title_text = "Who said 'I love you' more?")
        pie_chart.show()

def convert_date(date_time_str):
    date_time_object = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
    return date_time_object

def strip_date(date_time_str):
    return date_time_str.split(" ")[0]

def get_time(date):
    time = date.split(" ")[1][0:5]
    return time
