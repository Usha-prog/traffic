#from tkinter import font
import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import networkx.algorithms.community as nx_comm
#from community import community_louvain

st.title(' Optimal traffic routes prediction for Shuttle Services ')
st.markdown('Karate Club Graph')

uploaded_file = st.file_uploader(" ", type=['xlsx']) #Only accepts excel file format

if uploaded_file is not None:     
    data = pd.read_excel(uploaded_file)
    data
    graph = nx.karate_club_graph()
    graph = nx.from_pandas_edgelist(data,source='query_origin',target='query_destination',edge_attr=['distance(meters)','duration(minutes)']) #Use the Graph API to create an empty       network graph object

    partition = nx_comm.louvain_communities(graph)

    if st.button("Click here for Partition: "):
        st.write(partition, len(partition))

    color_map = []
    # color the nodes according to their partition
    for node in graph:
        if node in partition[0]:
            color_map.append('red')
        elif node in partition[1]:
            color_map.append('green')
        elif node in partition[2]:
            color_map.append('blue')
        else:
            color_map.append('yellow')

    
    fig, ax = plt.subplots(figsize = (30,15))
    pos = nx.spring_layout(graph)


    nx.draw_networkx(graph, pos, partition, 
                    with_labels=True, 
                    node_size = 250, 
                    node_shape = "s", 
                    edge_color = "k", 
                    style = "--", 
                    node_color = color_map,
                    font_size = 15)
    plt.title('Louvain_communities algorithm', fontdict={'fontsize': 40})
    st.pyplot(fig)
   
    #########################################
    st.info("louvain_community Partition Graph")

    com = nx_comm.louvain_communities(graph)

    st.subheader("For louvain_communities")
    st.write("Modularity: ", nx_comm.modularity(graph, com))
    st.write("Partition Quality: ", nx_comm.partition_quality(graph, com))
    st.write("Coverage: ", nx_comm.coverage(graph, com)) 
    st.write("Performance: ", nx_comm.performance(graph, com))

    if st.button("Click to show edge betweeness centrality of graph"):
        edge_BC = nx.edge_betweenness_centrality(graph)
        st.info(sorted(edge_BC.items(), key=lambda edge_BC : (edge_BC[1], edge_BC[0]), reverse = True))
