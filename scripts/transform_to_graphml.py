import networkx as nx
import pandas as pd

df_airports = pd.read_csv('data/airports.csv')
df_flights = pd.read_csv('data/anac.csv')
REGIOES = ['CENTRO-OESTE', 'NORDESTE', 'NORTE', 'SUDESTE','SUL']


# Create graph
G = nx.Graph()

df_airports = df_airports.query('country == "BRASIL"').copy()

# Add nodes
for index, row in df_airports.iterrows():
    G.add_node(row['code'],
               name=row['name'],
               country=row['country'],
               latitude=row['lat_geo_point'],
               longitude=row['lon_geo_point'],
               region=row['region']
               )

# Add edges

df_flights = df_flights.query('origin_airport_country == "BRASIL" and destination_airport_country == "BRASIL"').copy()
df_flights = df_flights.query('origin_airport_region == @REGIOES').copy() 
df_flights.dropna(subset=["origin_airport_region"],inplace=True)
df_flights.dropna(subset=['destination_airport_region'],inplace=True)


df_edges = df_flights[[
    'origin_airport_abbreviation',
    'destination_airport_abbreviation',
]].dropna()
df_edges = df_edges.groupby(df_edges.columns.tolist(), as_index=False).size()
for index, row in df_edges.iterrows():
    if row['origin_airport_abbreviation'] == row['destination_airport_abbreviation']:
        continue
    G.add_edge(row['origin_airport_abbreviation'], row['destination_airport_abbreviation'], flight_count=row['size'])

# Export to graphml
nx.write_graphml(G, 'air_traffic.graphml')
