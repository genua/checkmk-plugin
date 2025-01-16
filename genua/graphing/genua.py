#!/usr/bin/env python3

from cmk.graphing.v1 import Title

from cmk.graphing.v1.metrics import (
    Metric,
    Unit,
    IECNotation,
    Color,
    DecimalNotation,
)

from cmk.graphing.v1.graphs import Graph


metric_genua_swap_max = Metric(
    name="genua_swap_max",
    title=Title("Available Swap"),
    unit=Unit(IECNotation("B")),
    color=Color.GREEN,
)
metric_genua_swap_used = Metric(
    name="genua_swap_used",
    title=Title("Used Swap"),
    unit=Unit(IECNotation("B")),
    color=Color.BLUE,
)

graph_genua_swap = Graph(
    name="genua_swap",
    title=Title("Swap"),
    compound_lines=[
        "genua_swap_max",
    ],
    simple_lines=[
        "genua_swap_used",
    ],
)


metric_genua_genubox_servicebox_sessions = Metric(
    name="genua_genubox_servicebox_sessions",
    title=Title("ServiceBox Sessions"),
    unit=Unit(DecimalNotation('')),
    color=Color.BLUE,
)


metric_genua_rendezvous_fbzs_all_connections = Metric(
    name="genua_rendezvous_fbzs_all_connections",
    title=Title("All Fbzs Connections"),
    unit=Unit(DecimalNotation("")),
    color=Color.RED,
)
metric_genua_rendezvous_fbzs_open_connections = Metric(
    name="genua_rendezvous_fbzs_open_connections",
    title=Title("Open Fbzs Connections"),
    unit=Unit(DecimalNotation("")),
    color=Color.GREEN,
)

graph_genua_rendezvous_fbzs_connections = Graph(
    name="genua_rendezvous_fbzs_connections",
    title=Title("Fbzs Connections"),
    simple_lines=[
        "genua_rendezvous_fbzs_all_connections",
        "genua_rendezvous_fbzs_open_connections",
    ]
)

metric_genua_rendezvous_sb_cpu = Metric(
    name="genua_rendezvous_sb_cpu",
    title=Title("CPU Utilization ServiceBox"),
    unit=Unit(DecimalNotation("%")),
    color=Color.GREEN,
)

metric_genua_rendezvous_sb_mem = Metric(
    name="genua_rendezvous_sb_mem",
    title=Title("Memory ServiceBox"),
    unit=Unit(DecimalNotation("%")),
    color=Color.GREEN,
)

metric_genua_servicebox_sessions = Metric(
    name="genua_servicebox_sessions",
    title=Title("ServiceBox Sessions"),
    unit=Unit(DecimalNotation("")),
    color=Color.GREEN,
)
