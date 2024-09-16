import matplotlib.pyplot as plt
import pydot
import matplotlib.animation as animation
from PIL import Image
import io
import torch
import networkx as nx
from torch_geometric.utils import subgraph, to_networkx
from src.algorithm.individual_new import IndividualNew
import numpy as np


def generate_image_grid(images, cls_true, cls_pred=None, title=None, label_names=None):
    fig, axes = plt.subplots(3, 3, figsize=(10, 10))
    if title:
        fig.suptitle(title, size=20)

    for i, ax in enumerate(axes.flat):
        ax.imshow(images[i, :, :, :], interpolation='spline16')
        cls_true_name = label_names[int(cls_true[i])]
        xlabel = f"{cls_true_name} ({int(cls_true[i])})"
        if cls_pred is not None:
            cls_pred_name = label_names[int(cls_pred[i])]
            xlabel += f"\nPred: {cls_pred_name}"
        ax.set_xlabel(xlabel)
        ax.set_xticks([])
        ax.set_yticks([])

    fig.canvas.draw()
    image = Image.frombytes('RGBA', fig.canvas.get_width_height(), fig.canvas.buffer_rgba())

    plt.close(fig)

    return image


def generate_graph(individual, rankdir='TB', return_image=False):
    if isinstance(individual, IndividualNew):
        return _generate_graph_new(individual, rankdir, return_image)
    graph = pydot.Dot(graph_type='digraph', rankdir=rankdir)
    nodes = {}

    for i in range(individual.net_info.input_num):
        node = pydot.Node(f'input-{i}', label=f'Input {i}', shape='ellipse')
        nodes[i] = node
        graph.add_node(node)

    for idx in range(individual.net_info.node_num + individual.net_info.out_num):
        if individual.is_active[idx]:
            gene_info = individual.gene[idx]
            func_type = individual.net_info.func_type[gene_info[0]] if idx < individual.net_info.node_num else f'Output {idx - individual.net_info.node_num}'
            label = f"{func_type} (Node {idx})"
            node = pydot.Node(f'node-{idx}', label=label, shape='box')
            nodes[idx + individual.net_info.input_num] = node
            graph.add_node(node)

    for idx in range(individual.net_info.node_num + individual.net_info.out_num):
        if individual.is_active[idx]:
            for j in range(1, individual.net_info.max_in_num + 1):
                input_idx = individual.gene[idx][j]
                if input_idx >= 0:
                    edge = pydot.Edge(nodes[input_idx], nodes[idx + individual.net_info.input_num])
                    graph.add_edge(edge)

    if return_image:
        png_str = graph.create(prog='dot', format='png')
        image = Image.open(io.BytesIO(png_str))
        return image

    return graph


def generate_cartesian_graph(individual, return_image=False):
    if isinstance(individual, IndividualNew):
        return _generate_cartesian_graph_new(individual, return_image)
    graph = pydot.Dot(graph_type='digraph')
    nodes = {}

    for i in range(individual.net_info.input_num):
        node = pydot.Node(f'input-{i}', shape='ellipse')
        node.set('pos', f'-1,{i:.2f}!')
        nodes[i] = node
        graph.add_node(node)

    for idx in range(individual.net_info.node_num):
        x = (idx // individual.net_info.rows)
        y = idx % individual.net_info.rows

        node_style = "filled" if individual.is_active[idx] else "filled"
        node_color = '#ff00cc' if individual.is_active[idx] else '#cccccc'
        node = pydot.Node(f'{idx}', label=f'{idx}', style=node_style, shape="circle", fillcolor=node_color)
        node.set('pos', f'{x},{y}!')
        node.set('fontsize', 10)
        nodes[idx + individual.net_info.input_num] = node
        graph.add_node(node)

    for idx in range(individual.net_info.out_num):
        out_idx = individual.net_info.node_num + idx
        node = pydot.Node(f'output-{idx}', label=f'output-{idx}', style="filled", shape="ellipse", fillcolor='#ccaadd')
        node.set('pos', f'{(individual.net_info.cols + 1)},{idx:.2f}!')
        nodes[out_idx + individual.net_info.input_num] = node
        graph.add_node(node)

        for con in range(individual.net_info.max_in_num):
            input_idx = individual.gene[out_idx][con + 1]
            if input_idx in nodes:
                graph.add_edge(pydot.Edge(nodes[input_idx], nodes[out_idx + individual.net_info.input_num]))

    for idx in range(individual.net_info.node_num):
        if individual.is_active[idx]:
            for con in range(individual.net_info.max_in_num):
                input_idx = individual.gene[idx][con + 1]
                if input_idx in nodes:
                    graph.add_edge(pydot.Edge(nodes[input_idx], nodes[idx + individual.net_info.input_num]))

    if return_image:
        png_str = graph.create(prog='neato', format='png')
        image = Image.open(io.BytesIO(png_str))
        return image

    return graph


def generate_subgraph(data, num_nodes=10):
    subset = torch.arange(num_nodes)
    edge_index, _ = subgraph(subset, data.edge_index, relabel_nodes=True, num_nodes=data.num_nodes)

    sub_data = data.clone()
    sub_data.edge_index = edge_index
    sub_data.x = data.x[subset]
    sub_data.y = data.y[subset]

    G = to_networkx(sub_data, to_undirected=True)

    plt.figure(figsize=(10, 10))
    node_color = [sub_data.y[i].item() for i in range(num_nodes)]
    pos = nx.circular_layout(G)
    labels = {i: f"{i}\nClass {sub_data.y[i].item()}" for i in range(num_nodes)}
    nx.draw(G, pos, labels=labels, node_size=500, cmap=plt.get_cmap('Set3'), node_color=node_color, with_labels=True, font_weight='bold')

    fig = plt.gcf()
    fig.canvas.draw()

    image = Image.frombytes('RGBA', fig.canvas.get_width_height(), fig.canvas.buffer_rgba())

    plt.close(fig)

    return image


class ImageAnimation:
    def __init__(self, image_list, figsize=(8, 8), interval=1000):
        self.image_list = image_list
        self.iterations = len(image_list)
        self.fig, self.ax = plt.subplots(figsize=figsize)
        self.im = self.ax.imshow(self.image_list[0], animated=True)
        self.counter_text = self.ax.text(0.05, 0.95, '', transform=self.ax.transAxes, color='black', fontsize=30, ha='left', va='top', fontweight='bold')
        self.ax.axis('off')

        self.anim = animation.FuncAnimation(
            self.fig, self._draw_frame, frames=self.iterations,
            init_func=self._init, interval=interval, blit=True)

    def _init(self):
        self.im.set_data(self.image_list[0])
        self.counter_text.set_text(f"Image 1/{self.iterations}")
        return self.im, self.counter_text

    def _draw_frame(self, framedata):
        self.im.set_data(self.image_list[framedata])
        self.counter_text.set_text(f"Image {framedata + 1}/{self.iterations}")
        return self.im, self.counter_text

    def save(self, filename, dpi=100):
        self.anim.save(filename, writer='pillow', dpi=dpi)


def render_dot_to_image(dot_file, prog='dot'):
    (graph,) = pydot.graph_from_dot_file(dot_file)
    png_str = graph.create(prog=prog, format='png')
    image = Image.open(io.BytesIO(png_str))

    return image


def generate_combined_image(first_image, second_image, figsize):
    fig, axs = plt.subplots(2, 1, figsize=figsize)

    axs[0].imshow(first_image)
    axs[0].axis('off')

    axs[1].imshow(second_image)
    axs[1].axis('off')
    plt.tight_layout()

    fig.canvas.draw()
    combined_image = Image.frombytes('RGBA', fig.canvas.get_width_height(), fig.canvas.buffer_rgba())

    plt.close(fig)

    return combined_image


def _generate_graph_new(individual, rankdir='TB', return_image=False):
    graph = pydot.Dot(graph_type='graph', rankdir=rankdir)
    active_nodes = np.where(individual.is_active)[0]

    nodes = {}
    for i in range(individual.net_info.input_num):
        node = pydot.Node('input-%d' % i)
        nodes[i] = node
        graph.add_node(node)

    out_idx = 0
    for idx in active_nodes:
        gene = individual.gene[idx]
        if not gene['is_output']:
            fnc = individual.net_info.func_type[gene['fnc_idx']]
            label = fnc.__name__ if hasattr(fnc, '__name__') else str(fnc)
            name = label + '_id_%d' % idx
        else:
            name = 'output-%d' % out_idx
            label = name
            out_idx += 1
        nodes[idx + individual.net_info.input_num] = pydot.Node(name, label=label)
        graph.add_node(nodes[idx + individual.net_info.input_num])

    for idx in active_nodes:
        node = nodes[idx + individual.net_info.input_num]
        for con in range(individual.gene[idx]['num_inputs']):
            con_node = nodes[individual.gene[idx]['inputs'][con]]
            graph.add_edge(pydot.Edge(con_node, node))

    if return_image:
        png_str = graph.create(prog='dot', format='png')
        image = Image.open(io.BytesIO(png_str))
        return image

    return graph


def _generate_cartesian_graph_new(individual, return_image=False):
    graph = pydot.Dot(graph_type='digraph')
    nodes = []

    for i in range(individual.net_info.input_num):
        node = pydot.Node('input-%d' % i)
        node.set('pos', '-1,%2f!' % i)
        nodes.append(node)
        graph.add_node(node)

    for idx in range(individual.net_info.node_num):
        x = min(idx // individual.net_info.rows, individual.net_info.cols)
        y = idx % individual.net_info.rows

        node = pydot.Node(idx, style="filled", shape="circle")
        node.set('pos', '%f,%f!' % (x / 1.5, y / 1.5))
        node.set('fontsize', 10)

        if individual.is_active[idx]:
            node.set('fillcolor', '#ff00cc')

        nodes.append(node)
        graph.add_node(node)

    for idx in range(individual.net_info.out_num):
        node = pydot.Node('output %d' % idx, style="filled", fillcolor='#ccaadd')
        node.set('pos', '%2f,%2f!' % ((individual.net_info.cols + 1) / 1.5, idx))
        nodes.append(node)
        graph.add_node(node)

    last = None

    for idx in range(individual.net_info.node_num):
        if not individual.is_active[idx]:
            continue

        for con in range(individual.gene[idx]['num_inputs']):
            input_idx = individual.gene[idx]['inputs'][con]
            last = idx + individual.net_info.input_num
            graph.add_edge(pydot.Edge(nodes[input_idx], nodes[idx + individual.net_info.input_num]))

    graph.add_edge(pydot.Edge(nodes[last], nodes[-1]))

    if return_image:
        png_str = graph.create(prog='neato', format='png')
        image = Image.open(io.BytesIO(png_str))
        return image

    return graph
