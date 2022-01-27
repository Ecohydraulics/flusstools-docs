"""This module is inspired by Michael Diener - read more at
 https://github.com/mdiener21/python-geospatial-analysis-cookbook/tree/master/ch08

Example use: ``create_shortest_path(shp_file_name, start_node_id, end_node_id)``
"""

import networkx as nx
from .geotools import *
import json
from shapely.geometry import asLineString, asMultiPoint


def create_shortest_path(line_shp_name, start_node_id, end_node_id):
    """Calculates the shortest path from a network of lines.

    Args:
        line_shp_name (str): Input shapefile name
        start_node_id (int): Start node ID
        end_node_id (int): End node ID

    Returns:
        None: Creates a graph of nodes (coordinate pairs) connecting a start node with an end node in the defined ``line_shp_name``.
    """

    # load shapefile
    nx_load_shp = nx.read_shp(line_shp_name)

    # with not all graphs connected, take the largest connected subgraph by using the connected_component_subgraphs function.
    nx_list_subgraph = list(nx.connected_component_subgraphs(
        nx_load_shp.to_undirected()))[0]

    # get all the nodes in the network
    nx_nodes = np.array(nx_list_subgraph.nodes())

    # output the nodes to a GeoJSON file
    network_nodes = asMultiPoint(nx_nodes)
    write_geojson(line_shp_name.split(".shp")[0] + "_nodes.geojson",
                  network_nodes.__geo_interface__)

    # Compute the shortest path. Dijkstra's algorithm.
    nx_short_path = nx.shortest_path(nx_list_subgraph,
                                     source=tuple(nx_nodes[start_node_id]),
                                     target=tuple(nx_nodes[end_node_id]),
                                     weight='distance')

    # create numpy array of coordinates representing result path
    nx_array_path = get_full_path(nx_short_path, nx_list_subgraph)

    # convert numpy array to Shapely Linestring
    shortest_path = asLineString(nx_array_path)

    write_geojson(line_shp_name.split(".shp")[0] + "_Xpath.geojson",
                  shortest_path.__geo_interface__)


def get_path(n0, n1, nx_list_subgraph):
    """Get path between nodes ``n0`` and ``n1``.

    Args:
        n0 (int): Node 1
        n1 (int): Node 2
        nx_list_subgraph (list):(see create shortest path)

    Returns:
        ndarray: An array of point coordinates along the line linking these two nodes.
    """
    return np.array(json.loads(nx_list_subgraph[n0][n1]['Json'])['coordinates'])


def get_full_path(path, nx_list_subgraph):
    """Creates a numpy array of the line result.

    Args:
        path (str): Result of ``nx.shortest_path``
        nx_list_subgraph (list): See ``create_shortest path`` function

    Returns:
        ndarray: Coordinate pairs along a path.
    """
    p_list = []
    curp = None
    for i in range(len(path)-1):
        p = get_path(path[i], path[i+1], nx_list_subgraph)
        if curp is None:
            curp = p
        if np.sum((p[0]-curp)**2) > np.sum((p[-1]-curp)**2):
            p = p[::-1, :]
        p_list.append(p)
        curp = p[-1]
    return np.vstack(p_list)


def write_geojson(outfilename, indata):
    """Creates a new GeoJSON file

    Args>
        outfilename (str): Name for the output file
        indata (array): Array to write tyo the geojson file.

    Returns:
        Creates a new GeoJSON file.
    """
    with open(outfilename, "w") as file_out:
        file_out.write(json.dumps(indata))
