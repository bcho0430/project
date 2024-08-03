import datetime
import bokeh.models
import bokeh.plotting
import panel as pn
import pandas as pd

# Load and display the CSV file
# Reason: To read the financial data into a DataFrame for processing and analysis.
df = pd.read_csv('ticker.csv')
print(df.head())

# Initialize Panel Extension
# Reason: To set up the Panel environment for creating a web application.
pn.extension(sizing_mode="stretch_width", template="fast")
pn.state.template.param.update(title="Finance Data Streaming App")

# Convert the timestamp column to datetime
# Reason: To ensure that the timestamp data is in a format suitable for time-based operations.
df['t'] = pd.to_datetime(df['t'], unit='ms')

# Calculate 20-minute rolling statistics for Bollinger Bands
# Reason: Bollinger Bands help in understanding the volatility and price levels over a period of time.
df['vwap'] = df['vwap'].astype(float)  # Ensure VWAP is float
df['volume'] = df['volume'].astype(float)  # Ensure volume is float
df.set_index('t', inplace=True)  # Set timestamp as index

# 20-minute rolling window
# Reason: To calculate moving averages and standard deviations for a 20-minute period.
rolling_window = df.rolling('20T')

# Calculate VWAP and standard deviation
# Reason: VWAP (Volume Weighted Average Price) and standard deviation are used for Bollinger Bands.
df['rolling_vwap'] = rolling_window['vwap'].mean()
df['rolling_std'] = rolling_window['vwap'].std()
df['bollinger_upper'] = df['rolling_vwap'] + 2 * df['rolling_std']
df['bollinger_lower'] = df['rolling_vwap'] - 2 * df['rolling_std']

# Calculate alerts
# Reason: To identify significant price movements and trigger alerts for trading actions.
df['is_alert'] = (df['volume'] > 10000) & ((df['vwap'] > df['bollinger_upper']) | (df['vwap'] < df['bollinger_lower']))
df['action'] = df.apply(lambda x: 'sell' if x['is_alert'] and x['vwap'] > x['bollinger_upper'] else ('buy' if x['is_alert'] and x['vwap'] < x['bollinger_lower'] else 'hold'), axis=1)

# Filter alerts
# Reason: To create a subset of data containing only the rows where alerts are triggered.
alerts = df[df['is_alert']]

# Function to create the statistics plot
# Reason: To visualize the Bollinger Bands, VWAP, and trading actions on a time-series plot.
def stats_plotter(src):
    actions = ["buy", "sell", "hold"]
    color_map = bokeh.models.CategoricalColorMapper(
        factors=actions, palette=("#00ff00", "#ff0000", "#00000000")
    )

    fig = bokeh.plotting.figure(
        height=400,
        width=600,
        title="20 minutes Bollinger bands with last 1 minute average",
        x_axis_type="datetime",
    )
    fig.line('t', 'vwap', source=src)
    band = bokeh.models.Band(
        base='t',
        lower='bollinger_lower',
        upper='bollinger_upper',
        source=src,
        fill_alpha=0.3,
        fill_color="gray",
        line_color="black",
    )
    fig.scatter(
        't',
        'vwap',
        color={'field': 'action', 'transform': color_map},
        size=10,
        marker="circle",
        source=src,
    )
    fig.add_layout(band)
    return fig

# Prepare data for Bokeh
# Reason: To create a ColumnDataSource for Bokeh, which is used for plotting.
df.reset_index(inplace=True)  # Ensure 't' is a column again for plotting and table display
bokeh_src = bokeh.models.ColumnDataSource(df)

# Combine plot and table in a Panel layout
# Reason: To create an interactive web-based dashboard that displays the plot and data table.
viz = pn.Row(
    stats_plotter(bokeh_src),
    pn.widgets.DataFrame(df[['ticker', 't', 'vwap', 'action']], name='Alerts')
)

# Reason: To make the Panel layout servable, allowing it to be viewed as a web application.
viz.servable()
