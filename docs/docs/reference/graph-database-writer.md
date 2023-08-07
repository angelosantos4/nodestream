# Graph Database Writer

The graph database writer is a writer that writes the output of a ingestion pipeline to a graph database. Currently, only Neo4j is supported.

## Database Independent Options

### `database`
The name of the database technology to use. Currently only `neo4j` is supported.

### `batch_size`
The number of ingests to write to the database in a single batch. Defaults to 10000.

## Database Specific Options

### `neo4j`

#### `uri`
The URI of the Neo4j database to connect to.

#### `username`
The username to use when connecting to the Neo4j database.

#### `password`
The password to use when connecting to the Neo4j database.

#### `database_name`
The name of the logical database to use. If not specified, the default database (neo4j) will be used.

#### `use_enterprise_features`

If set to `true`, the Neo4j Enterprise features will be used. Defaults to `false`.
