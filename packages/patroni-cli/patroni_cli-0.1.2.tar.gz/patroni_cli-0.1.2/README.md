# Patroni CLI

Patroni CLI is a command-line tool that allows you to manage a Patroni PostgreSQL cluster. You can use it to view cluster status, elect new leaders, and perform switchovers between nodes.

## Features

- **View Cluster Status**: List all cluster members and their roles.
- **Elect New Leader**: Trigger a failover and elect a new leader for the cluster.
- **Switchover**: Perform a switchover to a specified node or any healthy node.

## Installation

You can install the Patroni CLI via pip after packaging:

```bash
pip install patroni-cli
```

### Usage
Here are the available commands:

#### Check Cluster Status
```bash
patroni-cli --url http://localhost:8008 --username admin --password admin status
```

#### Elect a New Leader
```bash
patroni-cli --url http://localhost:8008 --username admin --password admin elect new_leader_name
```
#### Perform a Switchover
```bash
patroni-cli --url http://localhost:8008 --username admin --password admin switchover target_leader_name
```
If you want to perform a switchover without specifying a target leader, use:

```bash
patroni-cli --url http://localhost:8008 --username admin --password admin switchover
```