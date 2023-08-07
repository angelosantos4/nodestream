# Extractors

## `StreamExtractor`

The `StreamExtractor` provides a convenient abstraction for extracting records from different types of streams
by allowing customization of the underlying stream system and the record format. By implementing the `StreamConnector`
and `StreamRecordFormat` subclasses, one can easily adapt the extraction process to various stream sources and
record formats.

The documentation below contains information on the supported `StreamConnector` and `StreamRecordFormat` options and
how to configure them. See the [Customizing The Stream Extractor](../guides/customizing-the-stream-extractor.md) guide
to learn how to add your own implementations of these classes.

#### Top Level Arguments

```yaml
- implementation: nodestream.pipeline.extractors.streams:StreamExtractor
  arguments:
     # rest of the stream extractor format arguments
     timeout: 10 # default 60. Number of seconds to await records.
     max_records: 1 # default 100. Max number of records to get at one time.
```

### `StreamConnector`

The `StreamConnector` describes how to poll data from the underlying streaming mechanism.

#### `Kafka`

```yaml
- implementation: nodestream.pipeline.extractors.streams:StreamExtractor
  arguments:
     # rest of the stream extractor format arguments
     connector: kafka
     topic: my-topic-with-data
     group_id: my_group_id
     bootstrap_servers:
      - localhost:9092
      - localhost:9093
```

### `StreamRecordFormat`

The `StreamRecordFormat` parses the raw data from the `StreamConnector`.

#### `json`

The `json` format simply calls `json.loads` on the data provided from the `StreamConnector`. To use it, you can
set the `record_format` to be `json` in the `StreamExtractor` configuration. For example:

```yaml
- implementation: nodestream.pipeline.extractors.streams:StreamExtractor
  arguments:
     # rest of the stream extractor format
     record_format: json
```

## `AthenaExtractor`

The `AthenaExtractor` issues a query to Amazon Athena, and returns yields each row as a record to the pipeline. For
example, the following `AthenaExtractor` configuration:

```yaml
- implementation: nodestream.pipeline.extractors.stores.aws:AthenaExtractor
  arguments:
    query: SELECT name, version FROM python_package_versions;
    workgroup: MY_WORKGROUP_NAME
    database: package_registry_metadata;
    output_location: s3://my_bucket/some_path
```

produces records with the following shape:

```json
{"name": "nodestream", "version": "0.2.0"}
```

### Arguments

| Parameter Name          	| Type   	| Description                                                                                                                                                                               	|
|-------------------------	|--------	|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------	|
| query                   	| String 	| The actual query to run. The results yielded by the extractor will reflect the shape of the data returned from the query.                                                                 	|
| workgroup               	| String 	| The workgroup name to use to execute the query under. See the [AWS Docs](https://docs.aws.amazon.com/athena/latest/ug/user-created-workgroups.html) for more information.                 	|
| output_location         	| String 	| The output location string to store results for Athena. See the [AWS Docs](https://docs.aws.amazon.com/athena/latest/ug/querying.html) for more information.                              	|
| database                	| String 	| The name of the athena logical database to execute the query in. See the [AWS Docs](https://docs.aws.amazon.com/athena/latest/ug/user-created-workgroups.html) for more information.      	|
| assume_role_arn         	| String 	| The ARN of a role to assume before interacting with the bucket. Of course the appropriate configuration is needed on both the current credentials as well as the target role.             	|
| assume_role_external_id 	| String 	| The external id that is required to assume role. Only used when `assume_role_arn` is set and only needed when the role is configured to require an external id.                           	|
| **session_args          	| Any    	| Any other argument that you want sent to the [boto3.Session](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/session.html) that will be used to interact with AWS. 	|

## `S3Extractor`

The `S3Extractor` pulls files down from S3 and yields the records read from each file using the
[appropriate file format parser](./file-formats.md). A simple example would look like this:

```yaml
- implementation: nodestream.pipeline.extractors.stores.aws:S3Extractor
  arguments:
    bucket: my-awesome-bucket
```

### Additional Arguments
With the previous minimal configuration, it will use your currently active aws credentials to read all objects from
`my-awesome-bucket`. However, there are many options you can add to this:

| Parameter Name          	| Type   	| Description                                                                                                                                                                               	|
|-------------------------	|--------	|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------	|
| prefix                  	| String 	| Filter the objects pulled from S3 to only the ones that have this prefix in the name.                                                                                                     	|
| object_format           	| String 	| Regardless of the file's extension, use the format provided from the list of [file format](./file-formats.md) supported.                                                                  	|
| assume_role_arn         	| String 	| The ARN of a role to assume before interacting with the bucket. Of course the appropriate configuration is needed on both the current credentials as well as the target role.             	|
| assume_role_external_id 	| String 	| The external id that is required to assume role. Only used when `assume_role_arn` is set and only needed when the role is configured to require an external id.                           	|
| **session_args          	| Any    	| Any other argument that you want sent to the [boto3.Session](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/session.html) that will be used to interact with AWS. 	|


## `FileExtractor`

The `FileExtractor` class represents an extractor that reads records from files specified by glob patterns.
It takes a collection of file paths as input and yields the records read from each file using the
[appropriate file format parser](./file-formats.md).

```yaml
- implementation: nodestream.pipeline.extractors:FileExtractor
  arguments:
    globs:
      - people/*.json
      - other_people/*.json
```

## `TimeToLiveConfigurationExtractor`

"Extracts" time to live configurations from the file and yields them one at a time to the graph database writer.


One can configure a Node TTL like this:
```yaml
- implementation: nodestream.pipeline.extractors.ttl:TimeToLiveConfigurationExtractor
  arguments:
    graph_object_type: NODE
    configurations:
      - object_type: Person
        expiry_in_hours: 96
      - object_type: Occupation
        expiry_in_hours: 48
```

and one can configure a Relationship TTL like this:

```yaml
- implementation: nodestream.pipeline.extractors.ttl:TimeToLiveConfigurationExtractor
  arguments:
    graph_object_type: RELATIONSHIP
    configurations:
      - object_type: REPORTS_TO
        expiry_in_hours: 96
      - object_type: PERFORMS
        expiry_in_hours: 48
```


### Arguments

Each configuration can include the following arguments:

| Parameter Name          	| Type   	| Description                                                                                                                                                                               	|
|-------------------------	|--------	|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------	|
| object_type             	| String 	| The object type to apply the TTL to.                                                                                                                                                      	|
| expiry_in_hours         	| Integer 	| The number of hours after which the object should be deleted.                                                                                                                              	|
| enabled                 	| Boolean 	| Whether or not the TTL is enabled. Defaults to `True`.                                                                                                                                     	|
| batch_size              	| Integer 	| The number of objects to delete in a single batch. Defaults to `100`.                                                                                                                     	|
| custom_query            	| String 	| A custom query to use to delete the objects. If not provided, the default query will be used. The custom query is database implmentation specific.                                                                                             	|
