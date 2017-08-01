Title: Lambda serialization
Date: 2017-08-01 01:51PM
Category: code
Tags: scala, scio, data

Lambda serialization is one of the more confusion issues in distributed data processing in Scala. No matter which framework you choose, whether it's Scalding, Spark, Flink or Scio, sooner or later you'll be hit by the dreaded `NotSerializableException`. In this post we'll take a closer look at the common causes and solutions to this problem.

## Setup

To demonstrate the problem, first we need a minimal setup that minics the behavior of a distributed data processing system. We start with a utility method that roundtrips an object throguh Java serialization. Anonymous functions, or lambdas, in such systems are serialized so that they can be distributed to workers for parallel processing.

```scala
import java.io.{ByteArrayInputStream, ByteArrayOutputStream, ObjectInputStream, ObjectOutputStream}

object SerDeUtil {
  def serDe[T](obj: T): T = {
    val buffer = new ByteArrayOutputStream()
    val out = new ObjectOutputStream(buffer)
    out.writeObject(obj)
    out.close()

    val in = new ObjectInputStream(new ByteArrayInputStream(buffer.toByteArray))
    in.readObject().asInstanceOf[T]
  }
}
```

Next we create a bare minimal `Collection[T]` type that mimics an abstract distributed data set, akin to `TypedPipe`, `RDD`, or `SCollection` in Scalding, Spark or Scio respectively. Our implementation is backed by a local in-memory `Seq[T]` but does pass the function `f` through serialization like a distributed system.

```scala
class Collection[T](private val xs: Seq[T]) {
  def map[U](f: T => U): Collection[U] = {
    val g = SerDeUtil.serDe(f)
    new Collection[U](xs.map(g))
  }
  override def toString: String = xs.toString()
}

object Collection {
  def apply[T](xs: T*): Collection[T] = new Collection[T](xs)
}
```

## Problems

The base case works perfectly fine. The anonymous function `_ + 1` gets translated to a `Function1[Int, Int]` instance. Since Scala functions extend `Serializable` and it doesn't refer to any closure, the instance is serializable by default.

```scala
object FnSerDe {
  def main(args: Array[String]): Unit = {
    /*
    _ + 1 =>
    new Function1[Int, Int] {
      override def apply(x: Int): Int = x + 1
    }
    */
    Collection(1, 2, 3).map(_ + 1)
  }
}
```

The next case also works fine. `plus` is a static method in `object FnSerDe` so it doesn't go through serialization. Instead the Scala compiler generates a `Function1[Int, Int]` instance to wrap it.

```scala
object FnSerDe {
  def plus(x: Int): Int = x + 1
  def main(args: Array[String]): Unit = {
    /*
    new Function1[Int, Int] {
      override def apply(x: Int): Int = FnSerDe.plus(x)
    }
    */
    Collection(1, 2, 3).map(plus)
  }
}
```

The next example is where the problem begins. By passing `new A().plus` into `map`, the `new A()` instance got pulled into the closure of the automatically generated `Function1` and needs to be serializable.

```scala
object FnSerDe {
  def main(args: Array[String]): Unit = {
    /*
    val a = new A()
    new Function1[Int, Int] {
      override def apply(x: Int): Int = a.plus(x) // a from closure
    }
    */
    Collection(1, 2, 3).map(new A().plus) // A is not serializable
  }
}

class A {
  def plus(x: Int): Int = x + 1
}
```

This can be easily fixed by making `A` extend `Serializable`.

```scala
class A extends Serializable {
  def plus(x: Int): Int = x + 1
}
```

Things get more complicated as our code grows. In the next example, even though `A` extends `Serializable` and its member `val b` is never used, it fails serialization since `B` doesn't extend `Serializable`.

```scala
class A extends Serializable {
  val b = new B
  def plus(x: Int): Int = x + 1
}

class B
```

We can apply the same trick we just learned by making `B` extend `Serializable` as well.

```scala
class B extends Serializable
```

However this gets tedious if the code base is large, and doesn't work with third-party code we have no control of. Since `b` is never used, we can mark it as `@transient` so that Java serializer ignores it.

```scala
class A extends Serializable {
  @transient val b = new B // becomes null after ser/de
  def plus(x: Int): Int = x + 1
}
```

This won't work if we do need to access `b` in the function though, since transient members become `null` after serialization, and we get an NullPointerException instead.

```scala
class A extends Serializable {
  @transient val b = new B // becomes null after ser/de
  def plus(x: Int): Int = x + b.one  // b.one throws NullPointerException
}

class B {
  val one = 1
}
```

Not all is lost though, we can still fix this by making `b` a `@transient lazy val`, so that `b` gets re-initialized with `new B` when it's first accessed after going through ser/de cycle.

```scala
class A extends Serializable {
  @transient lazy val b = new B // new B called again after ser/de
  def plus(x: Int): Int = x + b.one
}
```

We can also use this trick to make sure a non-serializable object survives ser/de, by making it `@transient lazy` while also keeping a serializable representation of it.

```scala
class A extends Serializable {
  @transient lazy val b = new B(arg) // B is not serializable
  val arg = 1 // but arg: Int is and can be used to re-initialize b
  def plus(x: Int): Int = x + b.one
}

// non-serializable third-party code, but requires a serializable Int to initialize
class B(arg: Int) {
  val one = arg
}
```

## Summary

This post only covered a tiny fraction of the broad topic of lambda serialization. Some systems like Spark and Scio uses closure cleaner to either remove non-serializable fields, or convert them to `Serializable` before serializing a lambda. The issue is made more complex by Scala 2.12 and Java 8 lambdas, since they're now dynamically generated and doesn't work with traditionally byte code manipulation used in these cleaners. Check out the following links for more about closure serialization.

- [Externalizer](https://github.com/twitter/chill/blob/develop/chill-scala/src/main/scala/com/twitter/chill/Externalizer.scala) - in Twitter chill, which wraps a non-serializable object and uses Kryo to handle serialization
- <https://github.com/scala/bug/issues/10232> - Invalid bytecode generated for deserialization when many lambdas are declared
- <https://github.com/scala/bug/issues/10233> - NotSerializableException on object methods due to lambda closure
- <https://issues.apache.org/jira/browse/SPARK-14540> - Support Scala 2.12 closures and Java 8 lambdas in ClosureCleaner
- <https://github.com/twitter/chill/pull/292> - Clean closures transitively
