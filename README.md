# README

## Description

This is the repository for the [webinar about cross-DAG dependencies in Apache Airflow](https://streamyard.com/watch/BUifcMp5zBsZ).

## Getting started

You can simply click the button below to start the exercise environment within Gitpod.

[![Open in Gitpod](
    https://gitpod.io/button/open-in-gitpod.svg
)](https://gitpod.io/#https://github.com/datamindedbe/academy_airflow)

### Airflow UI

This environment will set up an Airflow instance for you.
The Airflow UI will load in a new browser window once the startup is complete (if not, you can navigate to http://0.0.0.0:8080).
You can log in to the UI using "airflow" both as username and password.

### Mounted folders

The folder named *mount* contains three sub-folders: dags, logs and plugins.
These three folders reflect the internal state of Airflow for these points,
and can be used to upload DAGs or plugins into Airflow, or download log files. The examples handled during the webinar are already present in the *dags* folder.
