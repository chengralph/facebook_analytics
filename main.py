from facebook import facebook

fb_analysis = facebook.FaceBook()


print(fb_analysis.get_data_table())
fb_analysis.plot_message_graph()
fb_analysis.plot_videocall_graph()
fb_analysis.plot_24hour_graph()
fb_analysis.plot_message_pie_chart()
fb_analysis.plot_senders_pie_chart()
fb_analysis.plot_distribution_pie_chart()
fb_analysis.plot_count_love_chart()
