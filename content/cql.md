Title: Using CQL with legacy column families
Date: 2014-09-13 08:47PM
Category: code
Tags: cassandra, cql

We use [Cassandra](http://cassandra.apache.org/) extensively [at work](http://www.slideshare.net/JimmyMrdell/playlists-at-spotify-cassandra-summit-london-2013?related=1), and up till recently we've been using mostly Cassandra 1.2 with [Astyanax](https://github.com/Netflix/astyanax) and [Thrift](https://thrift.apache.org/) protocol in Java applications. Very recently we started adopting Cassandra 2.0 with CQL, [DataStax Java Driver](https://github.com/datastax/java-driver) and binary protocol.

While one should move to CQL schema to take full advantage of the new protocol and storage engine, it's still possible to use CQL and the new driver on existing clusters. Say we have a legacy column family with `UTF8Type` for row/column keys and `BytesType` for values, it would look like this in `cassandra-cli`:

```sql
create column family data
  with column_type = 'Standard'
  and comparator = 'UTF8Type'
  and default_validation_class = 'BytesType'
  and key_validation_class = 'UTF8Type';
```

And this in `cqlsh` after setting `start_native_transport: true` in `cassandra.yaml`:

```sql
CREATE TABLE data (
  key text,
  column1 text,
  value blob,
  PRIMARY KEY (key, column1)
) WITH COMPACT STORAGE;
```

In this table, `key` and `column1` corresponds to row and column keys in the legacy column family and `value` corresponds to column value.

Queries to look up a column value, an entire row, and selected columns in a row would look like this:

```sql
SELECT value FROM mykeyspace.data WHERE key = 'rowkey' AND column1 = 'colkey';
SELECT column1, value FROM mykeyspace.data WHERE key = 'rowkey';
SELECT column1, value FROM mykeyspace.data WHERE key = 'rowkey' AND column1 IN ('colkey1', 'colkey2');
```

And I found [these slides](http://www.slideshare.net/DataStax/understanding-how-cql3-maps-to-cassandras-internal-data-structure) that explain the mapping bewteen CQL and Cassandra's storage model.
