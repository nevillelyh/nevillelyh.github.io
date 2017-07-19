Title: Lawfulness of aggregateByKey
Date: 2017-07-19 11:23AM
Category: code
Tags: scala, scio, data, fp

I spent a couple hours yesterday debugging what I thought was a Protobuf serialization issue, which turns out to be an unlawful Monoid-like use of `aggregateByKey` in [Scio](https://github.com/spotify/scio).

## The Problem

Both Scio and Spark have `aggregate` and `aggregateByKey` transformations that look like this:

```scala
// on SCollection[V]
def aggregate[U](zeroValue: U)(seqOp: (U, V) => U, combOp: (U, U) => U): SCollection[U]

// on SCollection[(K, V)]
def aggregateByKey[U](zeroValue: U)(seqOp: (U, V) => U, combOp: (U, U) => U): SCollection[(K, U)]
```

And we have some business logic that looks like this:

```scala
case class Count(id: String, count: Int)

val z = Count("", 0) // zeroValue
def seqOp(acc: Count, v: Count) = Count(v.id, acc.count + v.count)
def combOp(x: Count, y: Count) = Count(x.id, x.count + y.count)

sc.parallelize(Seq(Count("a", 10), Count("a", 100), Count("b", 5), Count("b", 50)))
  .groupBy(_.id)
  .aggregateByKey(z)(seqOp, combOp)
```

This code however, only works correctly locally with `DirectRunner` and always produces results with `id == ""` when running on Dataflow service with the `DataflowRunner`. Can you spot the bug?

## Monoid laws

You might notice that `zeroValue` and `combOp` together resemble a [Monoid](https://en.wikipedia.org/wiki/Monoid), which should satisfy the identity law:

```scala
combOp(zeroValue, x) == combOp(x, zeroValue) == x
```

Since elements in Scio, Spark, etc. are unordered, `combOp` should also be commutative to make computation deterministic.

```scala
combOp(x, y) == combOp(y, x)
```

## Under the hood

Here are 3 scenarios of what could happen to our code. Let's assume our data is split up into 2 partitions.

```scala
val xs1 = List(Count("a", 10), Count("a", 15))
val xs2 = List(Count("a", 100), Count("a", 150))
```

The first scenario is the most intuitive given the method signature of `aggregateByKey`. Elements in every partition are accumulated into `zeroValue` with `seqOp`, and the accumulated values are reduced with `combOp`. This produces the correct result.

```scala
val r1 = List(xs1.foldLeft(z)(seqOp), xs2.foldLeft(z)(seqOp)).reduce(combOp)
```

The next 2 scenarios are similar, except that `zeroValue` is appended or prepended to the list of accumulated results of `xs1` and `xs2` as input to `combOp`.

```scala
val r2 = List(z, xs1.foldLeft(z)(seqOp), xs2.foldLeft(z)(seqOp)).reduce(combOp) // incorrect
val r3 = List(xs1.foldLeft(z)(seqOp), xs2.foldLeft(z)(seqOp), z).reduce(combOp) // correct
```

We realize that only `r3` is correct but `r2` is not. This is because `combOp` breaks the identity law and since `List#reduce` starts from the left, `combOp(z, x)` will not populate `id` correctly while `combOp(x, z)` does. We made the wrong assumption in our code that `zeroValue` is only used in `seqOp` and never fed directly into `combOp`, and didn't implement it correctly. Any of these 3 scenarios could happen depending on the platform implementation. We need to fix `combOp` to satisfy the identity law:

```scala
def combOp(x: Count, y: Count): Count = Count(if (x.id.nonEmpty) x.id else y.id, x.count + y.count)
```

For more details see [spotify/scio#729](https://github.com/spotify/scio/issues/729) and [BEAM-2453](https://issues.apache.org/jira/browse/BEAM-2453).
