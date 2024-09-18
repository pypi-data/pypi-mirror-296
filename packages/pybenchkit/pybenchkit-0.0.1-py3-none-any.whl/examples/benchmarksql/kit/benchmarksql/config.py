# Copyright (C) 2023 Huawei Technologies Co., Ltd. All rights reserved.
# SPDX-License-Identifier: MIT
"""
Benchmarksql benchmark configuration.
"""

from typing import List

from benchkit.platforms import get_current_platform


def get_mariadb_config(
    user: str,
    password: str,
    db_name: str,
    restart_sut_thread_probability: str = "0.0",
) -> List[str]:
    """
    Get benchmarksql config for mariadb/mysql.

    Documentation for parameters is available here:
    https://github.com/pgsql-io/benchmarksql/blob/master/docs/PROPERTIES.md
    """

    # TODO rollbackPercent as input parameter?

    p = get_current_platform()
    nb_cpus = p.nb_cpus()

    warehouses = 2
    load_workers = nb_cpus
    sut_threads = nb_cpus

    max_delivery_bg_threads = (3 * sut_threads) // 4

    max_delivery_bg_per_warehouse = nb_cpus

    rampup_mins = 0
    rampup_sut_mins = 0
    rampup_terminal_mins = 0
    run_mins = 5
    report_interval_secs = 10
    keying_time_multiplier = "0.1"
    think_time_multiplier = "0.1"

    return [
        "# General Driver and connection parameters",
        "#",
        "# db={ postgres | oracle | firebird | mariadb | transact-sql }",
        "# driver=<JDBC_DRIVER_CLASS>",
        "# application={ Generic | PostgreSQLStoredProc | OracleStoredProc }",
        "# conn=<JDBC_URI>",
        "# user=<USERNAME>",
        "# password=<PASSWORD>",
        "db=mariadb",
        "driver=org.mariadb.jdbc.Driver",
        "application=Generic",
        f"conn=jdbc:mariadb://localhost:3306/{db_name}",
        f"user={user}",
        f"password={password}",
        "",
        "# Scaling and timing configuration",
        f"warehouses={warehouses}",
        f"loadWorkers={load_workers}",
        "monkeys=64",  # previously: 2
        f"sutThreads={sut_threads}",
        f"maxDeliveryBGThreads={max_delivery_bg_threads}",
        f"maxDeliveryBGPerWarehouse={max_delivery_bg_per_warehouse}",
        f"rampupMins={rampup_mins}",
        f"rampupSUTMins={rampup_sut_mins}",
        f"rampupTerminalMins={rampup_terminal_mins}",
        f"runMins={run_mins}",
        f"reportIntervalSecs={report_interval_secs}",
        f"restartSUTThreadProbability={restart_sut_thread_probability}",
        f"keyingTimeMultiplier={keying_time_multiplier}",
        f"thinkTimeMultiplier={think_time_multiplier}",
        "traceTerminalIO=false",
        "",
        '# Below are the definitions for the "attempted" transaction mix.',
        "# The TPC-C specification requires minimum percentages for all but",
        "# the NEW_ORDER transaction. If a test run happens to have any of",
        "# those four types fall below those minimums, the entire test is",
        "# invalid. We don't want that to happen, so we specify values just",
        "# a tiny bit above the required minimum.",
        "# The newOrderWeight is calculated as 100.0 - sum(all_other_types).",
        "paymentWeight=43.2",
        "orderStatusWeight=4.2",
        "deliveryWeight=4.2",
        "stockLevelWeight=4.2",
        "",
        "# The TPC-C require a minimum of 1% of the NEW_ORDER transactions",
        "# to roll back due to a user entry error (non existing item",
        "# number. Doing it with a strict 1/100th probability can lead to",
        "# undershooting this target, so we default to 1.01% to be sure.",
        "rollbackPercent=1.01",
        "",
        "# Directory name to create for collecting detailed result data.",
        "# Comment this out to suppress. Note that the Flask UI will define",
        "# this by itself, so don't specify it if you run through the UI.",
        "resultDirectory=my_result_%tY-%tm-%td_%tH%tM%tS",
        "",
        "# BenchmarkSQL includes three OS metric collector scripts implemented",
        "# in Python3. Two require to have collectd installed on the server",
        "# systems, you want to include in the performance report. The data",
        "# will be saved in resultDirectory/data/os-metric.json. The third",
        "# is based on Prometheus and node_exporter.",
        "",
        "# mcCollectdMqtt.py is a metric collector that expects the collectd",
        "# instances on the servers to send the metric data to an MQTT broker.",
        "",
        "#osCollectorScript=./mcCollectdMqtt.py \\",
        "#    -h mymqttbroker.localdomain \\",
        "#    -t collectd/mydbserver.localdomain/# \\",
        "#    -t collectd/mybackrest.localdomain/#",
        "",
        "# mcCollectdGraphite.py is a metric collector that expects the",
        "# collectd instances on the servers to send the metric data to",
        "# a graphite/whisper database and be available through the /render",
        "# API.",
        "",
        "#osCollectorScript=./mcCollectdGraphite.py \\",
        "#    -u http://mygraphite.localdomain/render/ \\",
        "#    -t collectd.mydbserver_localdomain.*.* \\",
        "#    -t collectd.mydbserver_localdomain.*.*.* \\",
        "#    -t collectd.mybackrest_localdomain.*.* \\",
        "#    -t collectd.mybackrest_localdomain.*.*.*",
        "",
        "# mcPrometheus.py retrieves the metric data from a Prometheus",
        "# server through the API. It converts the output into the same",
        "# format as the former two produce. The instances listed are",
        '# the same names given in the "instance" label of the metric',
        "# data scraped by Prometheus. The port number will be removed",
        "# in the os-metric.json output.",
        "",
        "#osCollectorScript=./mcPrometheus.py \\",
        "#    -u http://myprometheus.localdomain:9090/api/v1/query_range \\",
        "#    -i mydbserver.localdomain:9100 \\",
        "#    -i mybackrest.localdomain:9100",
        "",
        "# The report script is what generates the detailed HTML report for",
        "# the benchmark run. It is a Jinja2 template based reporting system",
        "# that includes graphs of various metrics, captured during the benchmark.",
        "",
        "reportScript=./generateReport.py -t report_simple.html",
        "",
        "#reportScript=./generateReport.py \\",
        "#    -t report_extended.html \\",
        "#    -c 'mydbserver.localdomain:DB server' \\",
        "#    -d 'mydbserver.localdomain:DB server:hda2' \\",
        "#    -i 'mydbserver.localdomain:DB server:eth0' \\",
        "#    -c 'mybackrest.localdomain:pgbackrest server' \\",
        "#    -d 'mybackrest.localdomain:pgbackrest server:hda2' \\",
        "#    -i 'mybackrest.localdomain:pgbackrest server:eth0'",
    ]
