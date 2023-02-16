# Homerun

Temporal Example Project. (unfinished)

TODO
- Signal
- Query

A pitcher throws a ball (starts a task).

The batter has to swing at it (send a signal) at the right moment to register a hit!

Pre-requisites:
- A temporal server (use their [Docker Compose files](https://github.com/temporalio/docker-compose))
- Python >= 3.7
- [Poetry](https://python-poetry.org)
- [Local Temporal server running](https://docs.temporal.io/application-development/foundations#run-a-development-cluster)

To run the example:
1. `poetry install`
1. poetry run python homerun/homerun_activity.py