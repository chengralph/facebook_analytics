from facebook import facebook

fb_analysis = facebook()

fb_analysis.set_df()
fb_analysis.set_data()

print(fb_analysis.get_data_table())
fb_analysis.plot_message_graph()
fb_analysis.plot_videocall_graph()
fb_analysis.plot_24hour_graph()
fb_analysis.plot_message_pie_chart()
fb_analysis.plot_senders_pie_chart()

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

love you
lubby

"""
