#!/usr/bin/python3
import numpy as np
import networkx as nx
import plotly.graph_objs as go


def reconstruct_grid(environment,
                     obs,
                     action,
                     new_layout={},
                     new_label_pos={},
                     replace_dic=False,
                     size=None,
                     title='test grid'):

    # Some definitions.
    # ----------------
    # action_scpae  => space of the actions of the current environment.
    # grid          => grid information given the current environment.
    # n_bars        => total numbers of bars.
    # action        => current action applied to the grid. (This action does not-
    #                                                      change the grid topology).
    # custom_layout => Node's location on the grid.
    grid = []
    action_space = environment.action_space
    grid = environment.game.grid
    n_bars = len(action_space.substations_ids)

    if len(new_layout) != len(new_label_pos):
        raise ValueError('The lists pos and labels must have the same len')

    layout = {'1': (-280, -81),
              '2': (-100, -270),
              '3': (366, -270),
              '4': (350, -70),
              '5': (-80, -54),
              '6': (-64, 54),
              '7': (380, 0),
              '8': (438, 0),
              '9': (326, 70),
              '10': (200, 108),
              '11': (79, 162),
              '12': (-152, 270),
              '13': (-40, 270),
              '14': (222, 270)}

    if replace_dic:
        layout = new_layout
    else:
        for key, value in new_layout.items():
            if key in layout:
                layout[key] = value
            else:
                layout[key] = value
    # layout.update(new_layout)

    label_pos = {'1': 'top center',
                 '2': 'top left',
                 '3': 'middle right',
                 '4': 'bottom left',
                 '5': 'bottom right',
                 '6': 'middle left',
                 '7': 'top center',
                 '8': 'bottom center',
                 '9': 'bottom left',
                 '10': 'top center',
                 '11': 'bottom center',
                 '12': 'middle left',
                 '13': 'bottom right',
                 '14': 'middle right'}

    if replace_dic:
        label_pos = new_label_pos
    else:
        for key, value in new_label_pos.items():
            if key in layout:
                label_pos[key] = value
            else:
                layout[key] = value
    # label_pos.update(new_label_pos)

    # ---------------------------------------------------
    # The following code allows to get just the nodes ids
    # where there are elements connected. It also considerer
    # the split node action.
    all_sub_conf = []
    for sub_id in action_space.substations_ids:
        sub_conf, _ = action_space.get_substation_switches_in_action(action, sub_id)
        all_sub_conf.append(sub_conf)

    nodes_ids = np.arange(1, n_bars + 1)
    for i in range(len(all_sub_conf)):
        # Check if all elements in sub (i)
        # are connected to busbar B1.
        if (np.equal(all_sub_conf[i], np.ones(len(all_sub_conf[i])))).all():
            # Remove the existing node.
            nodes_ids = np.delete(nodes_ids, i)
            # And create a new node.
            nodes_ids = np.append(nodes_ids, int(str(666) + str(i + 1)))
        # Check if one or more elements
        # are connected to busbar B1.
        elif np.sum(all_sub_conf[i]) > 0:
            nodes_ids = np.append(nodes_ids, int(str(666) + str(i + 1)))

    # ------------------------------------------------------
    # Given the nodes where exist a connection if the busbar,
    # the nodes for prods and loads are reconstructed.

    # Retrieve id where loads and prods are connected.
    prods_ids = grid.mpc['gen'][:, 0]
    loads_ids = [int(x[0]) for x in grid.mpc['bus'] if x[2] > 0]

    # Boolean array where prods and loads are connected.
    are_prods = np.asarray([node_id in prods_ids for node_id in nodes_ids])
    are_loads = np.asarray([node_id in loads_ids for node_id in nodes_ids])

    # Lines ids of current grid.
    idx_or = np.asarray(list(map(int, grid.mpc['branch'][:, 0])))
    idx_ex = np.asarray(list(map(int, grid.mpc['branch'][:, 1])))

    edges_graph = list(zip(idx_or, idx_ex))
    nodes_graph = list(nodes_ids)

    # ----------------------------------------------------
    # # Compute observation values with an action do nothing.
    # obs, *_ = environment.step(action_space.get_do_nothing_action())
    #
    # print ('SE ids: \n{}'.format(obs.substations_ids))
    # print ('loads SE ids: \n{}'.format(obs.loads_substations_ids))
    # print ('Prods SE ids: \n{}'.format(obs.productions_substations_ids))
    # print ('Lines Or ids: \n{}'.format(obs.lines_or_substations_ids))
    # print ('Lines Ex ids: \n{}'.format(obs.lines_ex_substations_ids))
    # print ()
    # print ('Loads ids: \n{}'.format(obs.loads_nodes))
    # print ('Active loads: \n{}'.format(obs.active_loads))
    # print ('Reactive loads: \n{}'.format(obs.reactive_loads))
    # print ()
    # print ('Prods ids: \n{}'.format(obs.productions_nodes))
    # print ('Active Prods: \n{}'.format(obs.active_productions))
    # print ('Reactive Prods: \n{}'.format(obs.reactive_productions))
    # print ()
    # print ('Lines Or nodes: \n{}'.format(obs.lines_or_nodes))
    # print ('Lines Ex nodes: \n{}'.format(obs.lines_ex_nodes))
    # print ('Lines status: \n{}'.format(obs.lines_status))
    # print ('Active flows Or lines: \n{}'.format(obs.active_flows_origin))
    # print ('Reactive flows Or lines: \n{}'.format(obs.reactive_flows_origin))
    # print ('Active flows Ex lines: \n{}'.format(obs.active_flows_extremity))
    # print ('Reactive flows Ex lines: \n{}'.format(obs.reactive_flows_extremity))

    # print (grid.mpc)

    # ----------------------------------------
    # Creating label information for each node.

    labels = ['Results:'] * len(nodes_ids)

    def num_formatter(x): return '%.1f' % x

    # Fill prods. values in labels.
    for prod_id in prods_ids:
        # # Need to write at pos idx in labels the val of first load.
        # idx_prod_mpc = np.where(grid.mpc.gen[:, 0] == prod_id)[0][0]
        # prod_val_mpc = num_formatter(grid.mpc.gen[idx_prod_mpc, 2])
        # # Find the id in nodes_ids.
        # idx_in_nodes_ids = np.where(nodes_ids == prod_id)[0][0]
        # labels[idx_in_nodes_ids] += str('<br>' + 'Prod: ' + str(prod_val_mpc) + ' MW')
        #
        # Need to write at pos idx in labels the val of first load.
        idx_prod_mpc = np.where(grid.mpc['gen'][:, 0] == prod_id)[0][0]
        prod_val_obs = num_formatter(obs.active_productions[idx_prod_mpc])
        # Find the id in nodes_ids.
        idx_in_nodes_ids = np.where(nodes_ids == prod_id)[0][0]
        labels[idx_in_nodes_ids] += str('<br>' + 'Prod: ' + str(prod_val_obs) + ' MW')

    # Fill loads values in labels.
    for load_id in loads_ids:
        # Need to write at pos idx in labels the val of first load.
        idx_load_mpc = np.where(grid.mpc['bus'][:, 0] == load_id)[0][0]
        load_val_mpc = num_formatter(grid.mpc['bus'][idx_load_mpc, 2])
        # Find the id in nodes_ids.
        idx_in_nodes_ids = np.where(nodes_ids == load_id)[0][0]
        labels[idx_in_nodes_ids] += str('<br>' + 'Load: ' + str(load_val_mpc) + ' MW')

    # Fill origin values in labels.
    for node_or in np.unique(idx_or):
        #
        # For Origin transmission lines.
        # Retrieve node id indexes which belong to idx_or.
        idx_nodeid_idxor = np.where(idx_or == node_or)
        # Node id that pairs with idx_ex list.
        pair_nodeid_idxor = idx_ex[idx_nodeid_idxor]
        # Index in nodes_ids to allow to write in labels.
        idx_nodeid = np.where(nodes_ids == node_or)[0][0]
        for i in range(len(pair_nodeid_idxor)):
            # Write label for origin lines.
            labels[idx_nodeid] += str('<br>' + 'TLor{' + str(idx_or[idx_nodeid_idxor][i]) + '-' + str(pair_nodeid_idxor[i]) + '}' + ' ' + str(num_formatter(obs.active_flows_origin[idx_nodeid_idxor][i])) + ' MW')

    # Fill origin values in labels.
    for node_ex in np.unique(idx_ex):
        #
        # For Extrimity transmission lines.
        # Retrieve node id indexes which belong to idx_ex.
        idx_nodeid_idxex = np.where(idx_ex == node_ex)[0]
        # Node id that pairs with idx_or list.
        pair_nodeid_idxex = idx_or[idx_nodeid_idxex]
        # Index in nodes_ids to allow to write in labels.
        idx_nodeid = np.where(nodes_ids == node_ex)[0][0]
        for i in range(len(pair_nodeid_idxex)):
            # Write label for origin lines.
            labels[idx_nodeid] += str('<br>' + 'TLex{' + str(idx_ex[idx_nodeid_idxex][i]) + '-' + str(pair_nodeid_idxex[i]) + '}' + ' ' + str(num_formatter(obs.active_flows_extremity[idx_nodeid_idxex][i])) + ' MW')

    # --------------
    # Styling nodes
    # -------------
    default_size = 32
    size_nodes = np.ones(len(nodes_ids)) * default_size
    # Make productions nodes a bit bigger.
    size_nodes[np.where(are_prods == True)] = 47
    # Changing color nodes.
    default_color_nodes = 'rgb(31,120,180)'
    color_nodes = np.array([default_color_nodes] * len(nodes_ids))
    color_nodes[np.where(are_prods == True)] = 'rgb(227,26,28)'

    #
    # -------------------
    # Graph recontruction.
    G = nx.Graph()
    pos = {key: value for (key, value) in zip(nodes_graph, list(layout.values()))}

    # Edge trace for graph.
    edge_trace = go.Scatter(
        x=[],
        y=[],
        line=dict(width=1.4, color='#888'),
        hoverinfo='text',
        mode='lines')

    for edge in edges_graph:
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace['x'] += tuple([x0, x1, None])
        edge_trace['y'] += tuple([y0, y1, None])

# Edge nodes for graph.
    node_trace = go.Scatter(
        x=[],
        y=[],
        text=labels,
        # text=list(nodes_ids),
        mode='markers+text',
        hoverinfo='text',
        textposition=list(label_pos.values()),
        textfont=dict(size=9,
                      color='rgb(50,50,50)'),
        marker=dict(
            color=color_nodes,
            size=size_nodes,
            # colorbar=dict(thickness=15, title='Node Connections', xanchor='left', titleside='right'),
            line=dict(color='rgb(100,100,100)', width=2)))

    # Fill node trace.
    for node in nodes_graph:
        x, y = pos[node]
        node_trace['x'] += tuple([x])
        node_trace['y'] += tuple([y])

    # Function to make annotation like node name, etc.
    def make_annotations(pos, anno_text, font_size=10, font_color='rgb(255,255,255)'):
        L = len(pos)
        if len(anno_text) != L:
            raise ValueError('The lists pos and text must have the same len')
        annotations = []
        for k in range(L):
            annotations.append(dict(text=str(anno_text[k]),
                                    x=pos[k][0],
                                    y=pos[k][1],
                                    xref='x1', yref='y1',
                                    font=dict(color=font_color, size=font_size),
                                    showarrow=False))
        return annotations

    layout = layout = go.Layout(
        showlegend=False,
        margin=dict(b=10, l=5, r=5, t=10),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))

    # Modify grid size
    if size is None:
        pass
    else:
        layout.xaxis['range'] = [-size[0], size[0]]
        layout.yaxis['range'] = [-size[1], size[1]]

    # Make the graph with plotly.
    fig = go.Figure(data=[edge_trace, node_trace], layout=layout)
    # Labels
    fig['layout'].update(annotations=make_annotations(list(pos.values()), nodes_ids))

    # -------------
    # Coloring edges
    # -------------
    # P**2 = (sqrt(3)VI)**2 - Q**2
    vi = (np.sqrt(3) * obs.voltage_flows_origin * 100 * obs.thermal_limits / 1000)
    q = obs.reactive_flows_origin
    P_thermal_limits = np.sqrt(vi**2 - q**2)
    idx_lines = np.where(np.abs(obs.active_flows_origin) > P_thermal_limits)
    xx = []
    yy = []

    for k in idx_lines[0]:
        xx.extend([fig['data'][0]['x'][3 * k], fig['data'][0]['x'][3 * k + 1], None])
        yy.extend([fig['data'][0]['y'][3 * k], fig['data'][0]['y'][3 * k + 1], None])

    colored_edges = dict(type='scatter',
                         mode='line',
                         line=dict(width=6, color='red'),
                         x=xx,
                         y=yy)

    data1 = [colored_edges] + fig['data']
    fig1 = dict(data=data1, layout=fig['layout'])

    return fig1
