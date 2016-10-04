Title: How many copies
Date: 2014-08-02 8:48PM
Category: code
Tags: data, performance, scala

One topic that came up a lot when optimizing Scala data applications is the performance of standard collections, or the hidden cost of temporary copies. The collections API is easy to learn and maps well to many Python concepts where a lot of data engineers are familiar with. But the performance penalty can be pretty big when it's repeated over millions of records in a JVM with limited heap.

## Mapping values

Let's take a look at one most naive example first, mapping the values of a `Map`.

```scala
val m = Map("A" -> 1, "B" -> 2, "C" -> 3)
m.toList.map(t => (t._1, t._2 + 1)).toMap
```

Looks simple enough but obviously not optimal. Two temporary `List[(String, Int)]` were created, one from `toList` and one from `map`. `map` also creates 3 copies of `(String, Int)`.

There are a few commonly seen variations. These don't create temporary collections but still key-value tuples.

```scala
for ((k, v) <- m) yield k -> (v + 1)
m.map { case (k, v) => k -> (v + 1) }
```

If one reads the [ScalaDoc](http://www.scala-lang.org/api/2.10.4/index.html#scala.collection.immutable.Map) closely, there's a `mapValues` method already and it probably is the shortest and most performant.

```scala
m.mapValues(_ + 1)
```

## Java conversion

Similar problem exists when converting between Scala and Java collections. We store data on HDFS in [Avro](http://avro.apache.org/) and one most commonly used data structure is high dimensional vector, represented as `java.util.List[java.lang.Float]` in Avro and `Array[Float]` in Scala and [breeze](https://github.com/scalanlp/breeze).

Since there's no direct conversion between Java `List` and Scala `Array`, the naive solution requires a temporary copy and looks like this:

```scala
import java.util.{ List => JList }
import java.lang.{ Float => JFloat }
import scala.collection.JavaConverters._

def javaToArray(v: JList[JFloat]): Array[Float] = v.asScala.asInstanceOf[List[Float]].toArray
def arrayToJava(v: Array[Float]): JList[JFloat] = v.toList.asInstanceOf[List[JFloat]].asJava
```

The conversion is almost 10 times faster by doing the conversion manually in a loop.

```scala
def javaToArray(v: JList[JFloat]): Array[Float] = {
  val r = new Array[Float](v.size)
  var i = 0
  val j = v.iterator
  while (i < v.size) {
    r(i) = j.next
    i += 1
  }
  r
}

def arrayToJava(v: Array[Float]): JList[JFloat] = {
  val r = new JArrayList[JFloat](v.size)
  var i = 0
  while (i < v.size) {
    r.add(v(i))
    i += 1
  }
  r
}
```

## Merging maps

Same goes for merging 2 `Map[String, Double]` by summing up values of duplicate keys. Both solutions below require 2 copies of key sets, one union/intersect set,

```scala
val m1 = Map("A" -> 1.0, "B" -> 2.0, "C" -> 3.0)
val m2 = Map("A" -> 1.5, "B" -> 2.5, "D" -> 3.5)

// solution 1
val i = m1.keySet intersect m2.keySet
val m = i.map { k => k -> (m1(k) + m2(k)) }
(m1 -- i) ++ (m2 -- i) ++ m  // -- i unnecessary
m1  ++ m2 ++ m               // slightly better

// solution 2
(m1.keySet ++ m2.keySet) map { k =>
  k -> (m1.getOrElse(k, 0.0) + m2.getOrElse(k, 0.0))
}
```

The best solution for this case also happens to be the shortest. It leverages the fact that pairs from the right-hand size of `++` overwrite those on the left-hand size. One could even compare size of the maps and put the smaller on the right-hand size to further reduce copies.

```scala
m1 ++ m2.map { case (k, v) => k -> (v + m1.getOrElse(k, 0.0)) }
```

## Cheating by mutation

All of these optimizations are nice but sometimes they are just not enough. Imagine if the map merge operation is used in a `foldLeft` on the reducer size, over millions of users with one `Map` each, we'll be basically creating that many temporary copies and sometimes GC just can't keep up. Good thing is that in some cases we know for sure a temporary object won't be reused ever again, and can mutate it in place and pass it along to further reduce copying. In the example below LHS is mutated in place and returned in the binary operation.

```scala
import scala.collection.mutable. { Map => MMap }

def mergeMaps(m1: MMap[String, Double], m2: MMap[String, Double]) = {
  m2.foreach { case (k, v) => m1(k) = v + m1.getOrElse(k, 0.0) }
  m1
}
```

And in this `foldLeft` operation, LHS is always the same object as initial value `z` and mutated throughout the group.

```scala
val group: Grouped[String, MMap[String, Double]] // = ...
group.foldLeft(MMap[String, Double]())(mergeMaps)
```

Some numeric libraries, like [JBLAS](http://mikiobraun.github.io/jblas/) offer operators in both immutable (by copying) and mutable (by mutating in place) fashions. It's probably best to start with the immutable ones to ensure correctness, and drop down to mutating in place when running into performance problems.
