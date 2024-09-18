#   #!/usr/bin/env python
#   -*- coding: utf-8 -*-
#   ******************************************************************************
#     Copyright (c) 2024.
#     Developed by Yifei Lu
#     Last change on 8/22/24, 8:45 AM
#     Last change by yifei
#    *****************************************************************************
import pandas as pd
import numpy as np
from collections import OrderedDict
from pathlib import Path

from ..pipeline import Pipeline, Resistance, ShortPipe, LinearResistance
from ..node import Node
from ..network import Network
from ...utils.exception import *


def read_nodes(path_to_file: Path) -> dict:
    """

    :param path_to_file:
    :return:
    """
    nodes = dict()
    df_node = pd.read_csv(path_to_file, delimiter=';')
    df_node = df_node.replace({np.nan: None})

    _long = None
    _lat = None

    for row_index, row in df_node.iterrows():
        if row['gas_composition'] is not None:
            row['gas_composition'] = OrderedDict(eval(row['gas_composition']))
        if row['longitude'] is not None:
            _long = row['longitude']
        if row['latitude'] is not None:
            _lat = row['latitude']
        nodes[row['node_index']] = Node(node_index=row['node_index'],
                                        pressure_pa=row['pressure_pa'],
                                        volumetric_flow=row['flow_sm3_per_s'],
                                        energy_flow=row['flow_MW'],
                                        temperature=row['temperature_k'],
                                        altitude=row['altitude_m'],
                                        gas_composition=row['gas_composition'],
                                        node_type=row['node_type'],
                                        longitude=_long,
                                        latitude=_lat)
    return nodes


def read_pipelines(path_to_file: Path, network_nodes: dict, conversion_factor=1.) -> dict:
    """

    :param path_to_file:
    :param network_nodes:
    :return:
    """
    pipelines = dict()
    df_pipe = pd.read_csv(path_to_file, delimiter=';')
    df_pipe = df_pipe.replace({np.nan: None})

    for row_index, row in df_pipe.iterrows():
        pipelines[row['pipeline_index']] = Pipeline(inlet=network_nodes[row['inlet_index']],
                                                    outlet=network_nodes[row['outlet_index']],
                                                    diameter=row['diameter_m'],
                                                    length=row['length_m'],
                                                    friction_factor_method=row['friction_method'],
                                                    conversion_factor=conversion_factor)
    return pipelines


def read_compressors(path_to_file: Path) -> dict:
    """

    :param path_to_file:
    :return:
    """
    compressors = dict()
    return compressors


def read_resistances(path_to_file: Path, network_nodes: dict) -> dict:
    """

    :param path_to_file:
    :param network_nodes:
    :return:
    """
    resistances = dict()
    df_resistance = pd.read_csv(path_to_file, delimiter=';')
    df_resistance = df_resistance.replace({np.nan: None})

    for row_index, row in df_resistance.iterrows():
        resistances[row['resistance_index']] = Resistance(inlet=network_nodes[row['inlet_index']],
                                                          outlet=network_nodes[row['outlet_index']],
                                                          resistance=row['resistance'])
    return resistances


def read_linear_resistances(path_to_file: Path, network_nodes: dict) -> dict:
    """

    :param path_to_file:
    :param network_nodes:
    :return:
    """
    resistances = dict()
    df_linear_resistance = pd.read_csv(path_to_file, delimiter=';')
    df_linear_resistance = df_linear_resistance.replace({np.nan: None})

    for row_index, row in df_linear_resistance.iterrows():
        resistances[row['linear_resistance_index']] = LinearResistance(inlet=network_nodes[row['inlet_index']],
                                                                       outlet=network_nodes[row['outlet_index']],
                                                                       resistance=row['linear_resistance'])
    return resistances


def read_shortpipes(path_to_file: Path, network_nodes: dict) -> dict:
    """

    :param path_to_file:
    :param network_nodes:
    :return:
    """
    shortpipes = dict()
    df_shortpipes = pd.read_csv(path_to_file, delimiter=';')
    df_shortpipes = df_shortpipes.replace({np.nan: None})

    for row_index, row in df_shortpipes.iterrows():
        shortpipes[row['shortpipe_index']] = ShortPipe(inlet=network_nodes[row['inlet_index']],
                                                       outlet=network_nodes[row['outlet_index']])
    return shortpipes


def create_network_from_csv(path_to_folder: Path, conversion_factor=1.) -> Network:
    """

    :param path_to_folder:
    :return:
    """
    all_files = list(path_to_folder.glob('*.csv'))
    # nodes = read_nodes(Path('./' + '_'.join(all_files[0].stem.split('_')[:-1]) + '_nodes.csv'))
    nodes_file = next((file for file in all_files if 'node' in file.stem), None)

    nodes = read_nodes(nodes_file)

    network_components = {'node': nodes,  # the dataset should have at least node
                          'pipeline': None,
                          'compressor': None,
                          'resistance': None,
                          'shortpipe': None,
                          'linear_resistance': None}

    for file in all_files:
        file_name = file.stem
        if 'node' in file_name:
            pass
        elif 'pipeline' in file_name:
            pipelines = read_pipelines(file, nodes, conversion_factor)
            network_components['pipeline'] = pipelines
        elif 'compressor' in file_name:
            compressors = read_compressors(file)
            network_components['compressor'] = compressors
        elif 'resistance' in file_name:
            resistances = read_resistances(file, nodes)
            network_components['resistance'] = resistances
        elif 'linearR' in file_name:
            linear_resistances = read_linear_resistances(file, nodes)
            network_components['linear_resistance'] = linear_resistances
        elif 'shortpipe' in file_name:
            shortpipes = read_shortpipes(file, nodes)
            network_components['shortpipe'] = shortpipes
        else:
            raise FileNameError(f'Please check the file name {file_name}.csv')

    return Network(nodes=network_components['node'],
                   pipelines=network_components['pipeline'],
                   compressors=network_components['compressor'],
                   resistances=network_components['resistance'],
                   linear_resistances=network_components['linear_resistance'],
                   shortpipes=network_components['shortpipe'])
