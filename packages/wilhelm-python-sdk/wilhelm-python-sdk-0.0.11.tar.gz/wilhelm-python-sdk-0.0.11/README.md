Wilhelm Python SDK
==================

![Python Version][Python Version Badge]
[![Read the Docs][Read the Docs badge]][Read the Docs URL]
[![PyPI][PyPI project badge]][PyPI project url]
[![GitHub Workflow Status][GitHub Workflow Status badge]][GitHub Workflow Status URL]
[![Apache License badge]][Apache License URL]

Wilhelm Graph Database Python SDK offers a programmatic approach that uploads language vocabulary into Graph Database,
where [Wilhelm](https://wilhelm.qubitpi.org/) pulls the vocabularies and display them online

To install the SDK, simply run

```console
pip install wilhelm-python-sdk
```

Example Usage:

1. Make ready a Neo4J database instance. A free one can be obtained at https://console.neo4j.io
2. Set the following environment variables

   - `NEO4J_URI`: the connection URL of the database, such as "neo4j://localhost", "neo4j+s://xxx.databases.neo4j.io"
   - `NEO4J_USERNAME`: the username for connecting the database
   - `NEO4J_PASSWORD`: the user's password for the connection

   where all of them are available

3. Have a vocabulary file of the following YAML format ready at __german.yaml__ (in this example, we are loading a
   German vocabulary):

   ```yaml
   vocabulary:
     - term: "null"
       definition: 0
     - term: Guten Tag
       definition: Good day
     - term: Hallo
       definition: Hello
     - term: Ich heiße ...
       definition: I am called ...
     - term: Mein Name ist ...
       definition: My name is ...
     - term: bitte
       definition: please
   ```

4. Load vocabulary into Neo4J database:

   ```python
   from wilhelm_graphdb_python.neo4j_loader import load_into_database

   load_into_database("german.yaml", "German")
   ```

License
-------

The use and distribution terms for [Wilhelm Graph Database Python SDK]() are covered by the [Apache License, Version 2.0].

<div align="center">
    <a href="https://opensource.org/licenses">
        <img align="center" width="50%" alt="License Illustration" src="https://github.com/QubitPi/QubitPi/blob/master/img/apache-2.png?raw=true">
    </a>
</div>

[Apache License badge]: https://img.shields.io/badge/Apache%202.0-F25910.svg?style=for-the-badge&logo=Apache&logoColor=white
[Apache License URL]: https://www.apache.org/licenses/LICENSE-2.0
[Apache License, Version 2.0]: http://www.apache.org/licenses/LICENSE-2.0.html

[GitHub Workflow Status badge]: https://img.shields.io/github/actions/workflow/status/QubitPi/wilhelm-python-sdk/ci-cd.yml?logo=github&style=for-the-badge
[GitHub Workflow Status URL]: https://github.com/QubitPi/wilhelm-python-sdk/actions/workflows/ci-cd.yml

[Python Version Badge]: https://img.shields.io/badge/Python-3.10-brightgreen?style=for-the-badge&logo=python&logoColor=white
[PyPI project badge]: https://img.shields.io/pypi/v/wilhelm-python-sdk?logo=pypi&logoColor=white&style=for-the-badge
[PyPI project url]: https://pypi.org/project/wilhelm-python-sdk/

[Read the Docs badge]: https://img.shields.io/readthedocs/wilhelm-python-sdk?style=for-the-badge&logo=readthedocs&logoColor=white&label=Read%20the%20Docs&labelColor=8CA1AF
[Read the Docs URL]: https://wilhelm-python-sdk.qubitpi.org
