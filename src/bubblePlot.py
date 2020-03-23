import plotly.express as px
import pandas as pd

# Create a pandas dataframe from the csv:
df = pd.read_csv(input("Path to the CSV Data File: "))

# Index: K, N, L, ABUpdates, EUpdates, SyncAB, SyncAE, UpdatesABmin, UpdatesABmax, SyncAESuccess, SampleSize
fig = px.scatter_3d(df, x='K', y='N', z='L', size='ABUpdates', color='SyncAESuccess', hover_name='SampleSize')
# fig = px.scatter_3d(df, x='K', y='N', z='L', size='SyncAESuccess', color='SyncAESuccess')

fig.show()

# Allow to store the generated HTML in a file for use in a presentation
# import plotly as pl
# pl.offline.plot(fig, filename="output.html")
