Title: Fun with macros and parquet-avro
Date: 2015-01-08 02:01PM
Category: code
Tags: avro, macro, parquet, scala

I recently had some fun building [parquet-avro-extra](https://github.com/nevillelyh/parquet-avro-extra), an add-on module for [parquet-avro](https://github.com/Parquet/parquet-mr/tree/master/parquet-avro) using [Scala macros](http://scalamacros.org/). I did it mainly to learn Scala macros but also to make it easier to use [Parquet](http://parquet.incubator.apache.org/) with [Avro](http://avro.apache.org/) in a data pipeline.

## Parquet and Avro

Parquet is a columnar storage system designed for HDFS. It offers some nice improvements over row-major systems including better compression and less I/O with column projection and predicate pushdown. Avro is a data serialization system that enables type-safe access to structured data with complex schema. The `parquet-avro` module makes it possible to store data in Parquet format on disk and process them as Avro objects inside a JVM data pipeline like [Scalding](https://github.com/twitter/scalding) or [Spark](http://spark.apache.org/).

## Projection

Parquet allows reading only a subset of columns via projection. Here's an Scalding [example](https://github.com/epishkin/scalding/tree/parquet_avro/scalding-parquet) from [Tapad](http://www.tapad.com/).

```scala
Projection[Signal]("field1", "field2.field2a")
```
Note that fields specifications are strings even though the API has access to Avro type `Signal` which has strongly typed getter methods.

This is slightly counter-intuitive since most Scala developers are used to transformations like `pipe.map(_.getField)`. It's however can be easily solved with macro since the syntax tree of is accessible. A modified version has signature of `def apply[T](getters: (T => Any)*): Schema` and can be used like this:

```scala
Projection[Signal](_.getField1, _.getField2.getField2a)
```

The macro version looks more natural plus you get auto-complete support from the IDE and avoid typos.

## Predicate

Predicate is an even better use case for macros. The Parquet predicate API supports a fixed set of column types and operators, and the user must use the correct factory methods to construct an expression tree. A simple lambda like `i: Item => i.price < 100 && i.getReviews >= 10` becomes this:

```java
import parquet.filter2.predicate.FilterApi;
import parquet.filter2.predicate.FilterPredicate;

FilterPredicate p = FilterApi(
  FilterApi.lt(FilterApi.floatColumn("price"), 100f),
  FilterApi.gteq(FilterApi.intColumn("reviews"), 10));
```

Obviously this very cumbersome and even worse than the projection case. But with macros it feels almost like writing a regular Scala predicate lambda:

```scala
Predicate[Item](i => i.getPrice < 100 && i.getReviews >= 10)
```

## Lessons learned

I have some experience with C++ templates and Clojure macros, but Scala macros is still pretty challenging to get started. A couple of notes:

- Since one can write pretty complex code inside a macro, I had to remind myself that they don't compute data at runtime, but merely transform the syntax tree.
- Pattern matching and deconstruction are handy for extracting tree elements.
- Quasiquotes can be chained and returned in recursion for complex transformations, just be aware of the different types first.
- It's great exercise for your recursion skills.
