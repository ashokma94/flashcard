import pyqtgraph as pg
from PyQt6.QtWidgets import QWidget, QGridLayout
from PyQt6.QtCore import Qt
from random import randint

class BuildGraph(QWidget):
    def __init__(self):
        super().__init__()

        # Create a grid layout to hold the plot graphs
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        # Create multiple plot widget
        self.plot_graphs = []

        self.multi_plot(0,0)
        self.multi_plot(0,1)
        self.multi_plot(0,2)
        self.multi_plot(1,0)
        self.multi_plot(1,1)
        self.multi_plot(1,2)
    
    def multi_plot(self, row, col):
        plot_graph = pg.PlotWidget()
        plot_graph.setBackground('w')  # Set background color
        plot_graph.showGrid(x=True, y=True)
        plot_graph.addLegend()
        plot_graph.setFixedSize(400, 400)

        # Generate random data for each graph
        time = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        temperature = [randint(36, 45) for _ in range(10)]

        pen = pg.mkPen(color='r', width=2, style=Qt.PenStyle.SolidLine)
        bar_chart = self.plot_bar_chart(time, temperature)
        plot_graph.addItem(bar_chart)
        line_chart = self.plot_line_graph(time, temperature, f"Graph {col+1}", pen)
        plot_graph.addItem(line_chart)

        self.plot_graphs.append(plot_graph)  # Store the plot widget
        
        # Add the plot widget to the grid layout
        self.layout.addWidget(plot_graph, row, col)  # Arrange in a grid (3 columns)

    def plot_line_graph(self, xaxis, yaxis, name, pen):
        line = pg.PlotDataItem(xaxis, yaxis, name=name, pen=pen, symbol='o')
        return line

    def plot_bar_chart(self, xaxis, yaxis):
        bar = pg.BarGraphItem(x=xaxis, height=yaxis, width=0.5, brush='g')
        return bar
    
# import sys
# import pyqtgraph as pg
# from PyQt6.QtWidgets import QApplication, QMainWindow
# from pyqtgraph import DateAxisItem
# import pandas as pd
# import datetime

# # Create sample datetime and temperature data using pandas
# data = {'datetime': ['2024-10-10 12:00:00', '2024-10-10 13:00:00', 
#                      '2024-10-10 14:00:00', '2024-10-10 15:00:00'],
#         'temperature': [22.5, 23.0, 23.7, 24.1]}

# df = pd.read_csv('sample.csv')
# df['Time'] = pd.to_datetime(df['Time'])  # Convert to datetime
# df['Time'] = df['Time'].apply(lambda x: x.timestamp())  # Convert to timestamps

# # Create a PyQtGraph application window
# app = QApplication(sys.argv)
# win = QMainWindow()
# plot_widget = pg.PlotWidget()

# # Use DateAxisItem to format x-axis as datetime
# axis = DateAxisItem(orientation='bottom')
# plot_widget = pg.PlotWidget(axisItems={'bottom': axis})

# # Plot the data from pandas DataFrame
# plot_widget.plot(df['Time'], df['Rx_Ch#1_MinimumLevel'], symbol='o', pen=pg.mkPen('b', width=2))

# # Set axis labels
# plot_widget.setLabel('left', 'Rx_Ch#1_MinimumLevel')
# plot_widget.setLabel('bottom', 'Time')

# # Show the window
# win.setCentralWidget(plot_widget)
# win.show()
# sys.exit(app.exec())

# import sys
# import pyqtgraph as pg
# from PyQt6.QtWidgets import QApplication, QMainWindow
# from pyqtgraph import DateAxisItem, ViewBox
# import pandas as pd
# import datetime

# # Create sample datetime, temperature, and humidity data using pandas
# data = {'datetime': ['2024-10-10 12:00:00', '2024-10-10 13:00:00', 
#                      '2024-10-10 14:00:00', '2024-10-10 15:00:00'],
#         'temperature': [22.5, 23.0, 23.7, 24.1],
#         'humidity': [55, 60, 58, 65]}

# df = pd.DataFrame(data)
# df['datetime'] = pd.to_datetime(df['datetime'])  # Convert to datetime
# df['timestamp'] = df['datetime'].apply(lambda x: x.timestamp())  # Convert to timestamps

# # Create a PyQtGraph application window
# app = QApplication(sys.argv)
# win = QMainWindow()
# plot_widget = pg.PlotWidget()

# # Use DateAxisItem to format x-axis as datetime
# axis = DateAxisItem(orientation='bottom')
# plot_widget = pg.PlotWidget(axisItems={'bottom': axis})

# # Add the first plot (temperature)
# plot_widget.plot(df['timestamp'], df['temperature'], symbol='o', pen=pg.mkPen('b', width=2), name="Temperature")
# plot_widget.setLabel('left', 'Temperature (°C)')

# # Create a second ViewBox for the humidity plot
# vb2 = ViewBox()
# plot_widget.scene().addItem(vb2)
# plot_widget.getAxis('right').linkToView(vb2)
# vb2.setXLink(plot_widget)  # Share the x-axis

# # Add the second plot (humidity)
# humidity_plot = pg.PlotDataItem(df['timestamp'], df['humidity'], symbol='x', pen=pg.mkPen('r', width=2), name="Humidity")
# vb2.addItem(humidity_plot)

# # Enable right y-axis and link it to the second ViewBox
# plot_widget.showAxis('right')
# plot_widget.getAxis('right').setLabel('Humidity (%)')

# # Adjust the view to match with the shared x-axis
# def update_views():
#     vb2.setGeometry(plot_widget.getViewBox().sceneBoundingRect())
#     vb2.linkedViewChanged(plot_widget.getViewBox(), vb2.XAxis)

# plot_widget.getViewBox().sigResized.connect(update_views)

# # Show the window
# win.setCentralWidget(plot_widget)
# win.show()
# sys.exit(app.exec())