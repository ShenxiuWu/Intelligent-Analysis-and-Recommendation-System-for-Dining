#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import folium
import networkx as nx
import osmnx as ox


def showMarkers(data):
    """
    :type data:     dataFrame
    """   
    lats = list(data['latitude'])
    lngs = list(data['longitude'])
    centralY, centralX = 0, 0
    for i in range(len(lats)):
        centralY += lats[i]
        centralX += lngs[i]
    centralLoc = [centralY, centralX]
    m = folium.Map(location = centralLoc) # folium.Map(location=[longitude[0], latitude[0]])
    marker_cluster = folium.MarkerCluster().add_to(m)
    for name, row in data[:1000].iterrows():
        folium.Marker([row["latitude"], row["longitude"]], popup=row["name"]).add_to(marker_cluster)
    m.save('stops.html')
    return m

def shortestPathNavigation(userLoc, destinLoc):
    """
    :type userLoc:     List[float] of size 2
    :type destinLoc:   List[float] of size 2
    """
    G = ox.graph_from_point(userLoc, distance = 2000, distance_type = 'network', network_type = 'walk')
    Gnodes = G.nodes()
    
    # Get the nearest node in the system of the given location
    origin_node = ox.get_nearest_node(G, userLoc)
    destin_node = ox.get_nearest_node(G, destinLoc)
    
    # Get the lat&lng of the approximated location
    origin_point, destin_point = [[Gnodes[i]['y'],Gnodes[i]['x']] for i in [origin_node, destin_node]]
    
    # Get the shortest route's nodes' indices
    route = nx.shortest_path(G, origin_node,destin_node, weight = 'length')
    fig,ax = ox.plot_graph_route(G,route,origin_point = origin_point, destination_point = destin_point)
    
    # Get the shortest route's lat&lng
    the_route = [[G.nodes()[i]['y'],G.nodes()[i]['x']] for i in route]
    
    # Create map and add markers of origin&destin to the map
    m = folium.Map(location = userLoc, zoom_start = 13)
    marker_cluster = folium.MarkerCluster().add_to(m)
    folium.Marker(origin_point, popup = 'Origin').add_to(marker_cluster)
    folium.Marker(destin_point, popup = 'Dest').add_to(marker_cluster)
    
    # Add the shortest path to the map
    shortest_path = folium.PolyLine(the_route).add_to(m) # More parameters: #weight=15,#color='#8EE9FF'
    
    # Show the map
    return m