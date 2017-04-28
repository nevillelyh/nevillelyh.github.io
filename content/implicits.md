Title: Implicits
Date: 2017-04-21 8:48AM
Category: code
Tags: scala, fp

In this post we're going to take a closer look at Scala implicits and various use cases.

## Basics

Let's first look at the basics. There're 3 main basic uses of implicits, as an argument, as a conversion method, and enhancing an existing class, a.k.a. the "Pimp My Library" pattern.

### Implicit arguments

Suppose we have a basic function like this.

```scala
def plus(x: Int) = x + 1
plus(10) // => 11
```

We can add a second argument and make it a curried function.

```scala
def plus(x: Int)(y: Int) = x + y
plus(10)(1) // => 11
```

We can then make the second argument implicit and supply it via an `implicit val`.

```scala
def plus(x: Int)(implicit y: Int) = x + y

implicit val one = 1
plus(10) // => 11
```

Since `plus` needs an implicit argument of type `Int` and there happens to be one in the scope, `one` is applied automatically. However it won't work if there are multiple `implicit val`s.

```scala
implicit val one = 1
implicit val two = 2
plus(10) // => ambiguous implicit values
```

This example isn't very interesting and one can usually use argument with a default value instead. However implicit arguments are handy for decoupling behavior from business logic. Let's take a look at `Future[+T]` for example.

```scala
val f = Future {
  Thread.sleep(1000) // simulating slow computation
  42
}
// => Cannot find an implicit ExecutionContext.
```

A closer look at the API shows that `Future { code }` is actually an `apply` method on the companion object. The implicit argument `executor` determines the concurrency behavior, e.g. fixed, fork-join or other thread pools.

```scala
object Future {
  def apply[T](body: => T)(implicit executor: ExecutionContext): Future[T]
}
```

And we can import a default global one in this case.

```scala
import scala.concurrent.ExecutionContext.Implicits.global
val f = Future { /* lenghty computation */ }
```

And `global` is just a predefined `implicit val`.

```scala
object ExecutionContext {
  object Implicits {
    implicit lazy val global: ExecutionContextExecutor = // ...
  }
}
```

### Implicit conversions

Say we build a complex number data type and a plus method.

```scala
case class Complex(r: Double, i: Double)
def plus(x: Complex, y: Complex): Complex =
  Complex(x.r + y.r, x.i + y.i)
    
plus(Complex(1.0, -1.0), Complex(2.0, 0.0)) // Complex(3.0, -1.0)
```

Note that a complex number `2.0+0.0i` is also a real number, but we can't pass it to `plus` here.

```scala
plus(Complex(1.0, -1.0), 2.0) // type mismatch
```

We can however convert a `Double` to a `Complex`.

```scala
def double2complex(x: Double) = Complex(x, 0.0)
plus(Complex(1.0, -1.0), double2complex(2.0)) // Complex(3.0, -1.0)
```

And if we make `double2complex` implicit the compiler can apply automatic conversion for us.

```scala
implicit def double2complex(x: Double) = Complex(x, 0.0)
plus(Complex(1.0, -1.0), 2.0) // Complex(3.0, -1.0)
```

Implicit conversions are handy when building specific types from broader, more generic ones, but could lead to surprises if abused. Imagine what happens if we provide an implicit conversion from `String` to `Int`.

```scala
def plus(x: Int, y: Int) = x + y
implicit def s2i(s: String) = s.length

plus("a", "bcd") // => 4!
```

### Pimp My Library

Let's say we're using the `Complex` type from another library and would like to add a `scale` method to it. This is normally not possible without modifying the `Complex` class source code. However we could build a wrapper for the class with additional methods.

```scala
class RichComplex(self: Complex) {
  def scale(x: Double) = Complex(self.r * x, self.i * x)
}
```

We can also provide an implicit conversion method and use `Complex` as if it's also an `RichComplex`. Here the compiler realizes that there's no `scale(x: Double)` method on `Complex` but there exists an implicit conversion to `RichComplex` which does.

```scala
implicit def makeRichComplex(self: Complex) = new RichComplex(self)
Complex(1.0, -1.0).scale(10.0) // => Complex(10.0, 10.0)
```

If we own the `Complex` source code, a common pattern is to put enrichment methods (`makeRich*`) in a companion object and they can be resolved automatically. This is a common technique for library builders to split up complex classes into modules and provide specialization.

```scala
trait MyList[T] {
  // a lot of basic methods
}

class MyDoubleList(self: MyList[Double]) {
  // specific methods for Double
}

class MyKeyValueList[K, V](self: MyList[(K, V)]) {
  // specificmethods for key-value pairs
}

class MyTextList(self: MyList[String]) {
  // specific methods for String
  def saveAsTextFile(file: String) = // ...
}

object MyList {
  implicit def makeDoubleList(self: MyList[Double]) =
    new MyDoubleList(self)
  implicit def makeKeyValueList[K, V](self: MyList[(K, V)]) =
    new MyKeyValueList(self)
  implicit def makeTextList(self: MyList[String]) =
    new MyTextList(self)
}
```

You might have noticed that every time we call a method on an enhanced class, a new object is created. This can be sub-optimal, especially if there are large amount of base objects in a tight loop. The answer to this is [value classes](http://docs.scala-lang.org/overviews/core/value-classes.html). Basically an implicit class that extends `AnyVal`.

```scala
implicit class RichComplex(val self: Complex) extends AnyVal {
  def scale(x: Double) = Complex(self.r * x, self.i * x)
}
```

The plus side is that now we don't need the `implicit def` conversion method any more. The slight down side is that implicit classes cannot be declared at top level. A common practice is to put these classes in a package object so the library user can import it easily, e.g. `import com.mydomain.mydsl._` with the following example.

```scala
package com.mydomain

package object mydsl {
  implicit class RichComplex(val self: Complex) extends AnyVal {
    // ...
  }
}
```

## Type classes

Now that we covered the basic mechanics of implicits, let's talk about it's most common use case, type classes. We will start with summing numbers and then generalizing it to other types.

### Summing numbers

Let's start with a `sum` method that sums `Int`s.

```scala
def sum(xs: List[Int]) = xs.reduce(_ + _)
```

This is fairly straight-forward, but what if we want to sum `Long`, `Float` and `Double` as well? The follow code actually doesn't work because of type erasure.

```scala
def sum(xs: List[Int]) = xs.reduce(_ + _)
def sum(xs: List[Long]) = xs.reduce(_ + _)
def sum(xs: List[Float]) = xs.reduce(_ + _)
def sum(xs: List[Double]) = xs.reduce(_ + _)
```

But we noticed that all 4 cases require a `_ + _` operation. We can define a trait `Plus[T]` for it, which describes the plus behavior of type `T`, and 4 instances of it, one for each numeric type we want to generalize over. We call `Plus[T]` a type class for `T`. Note that the instances are implicits because we want the compiler to pass them for us.

```scala
trait Plus[T] {
  def plus(x: T, y: T): T
}
implicit val intPlus = new Plus[Int] {
  override def plus(x: Int, y: Int): Int = x + y
}
implicit val longPlus = new Plus[Long] {
  override def plus(x: Long, y: Long): Long = x + y
}
implicit val floatPlus = new Plus[Float] {
  override def plus(x: Float, y: Float): Float = x + y
}
implicit val doublePlus = new Plus[Double] {
  override def plus(x: Double, y: Double): Double = x + y
}
```

How we can rewrite our `sum` method in a more generic way.

```scala
def sum[T](xs: List[T])(implicit p: Plus[T]) = xs.reduce(p.plus)
sum(List(1, 2, 3)) // => 6
sum(List(0.1, 0.2, 0.3)) // => 0.6
```

This is nice but we still have to implement 4 `Plus[T]` instances. Lucky for us, there's already a predefined `Numeric[T]` type class in Scala, so we can simplify the above.

```scala
def sum[T](xs: List[T])(implicit num: Numeric[T]) = xs.reduce(num.plus)
```

This works for the numeric types in Scala but not necessarily other types that exhibit similar behavior, e.g. `Complex`, `Rational`. We can even further generalize the plus operation to non-numerical types, like the union of 2 sets.

### Semigroup

Now we start noticing a common pattern among these use cases, a type `T` and a binary operation `plus` of `(T, T) => T`. This is known as a [semigroup](https://en.wikipedia.org/wiki/Semigroup) in abstract algebra, and the plus operation is required to be associative, i.e. `(x + y) + z = x + (y + z)`. We can now support `Set[U]` by rewriting `sum` with `Semigroup[T]`.

```scala
trait Semigroup[T] {
  def plus(x: T, y: T): T
}
implicit def numSg(implicit num: Numeric[T]) = new Semigroup[T] {
  override def plus(x: T, y: T): T = num.plus(x, y)
}
implicit def setSg[U] = new Semigroup[Set[U]] {
  override def plus(x: Set[U], y: Set[U]): Set[U] = x ++ y
}
def sum[T](xs: List[T])(implicit sg: Semigroup[T]) = xs.reduce(sg.plus)
sum(List(Set("a", "b"), Set("a", "c"), Set("d"))) // => Set("a", "b", "c", "d")
```

The method signature for `sum` is a bit hard to read though, since we have a type parameter `[T]` before the argument list `(xs: List[T])`, and a implicit argument `sg: Semigroup[T]` after that describes the behavior of `T`. This can be rewritten as a context bound, `[T: Semigroup]`, to indicate that there exists a `Semigroup[T]` instance, but not explicitly given a name inside `sum`. The inside the function `implicitly[Semigroup[T]]` recovers the name.

```scala
def sum[T: Semigroup](xs: List[T]) = {
  val sg = implicitly[Semigroup[T]]
  xs.reduce(sg.plus)
}
```

And if we look at the source code of `implicitly`, it simply does what we did with `(implicit sg: Semigroup[T])` with a funny comment.

```scala
// for summoning implicit values from the nether world 
def implicitly[T](implicit e: T) = e
```

One common practice in Scala is to use tuples for lightweight data representation, e.g. rows from a data source. But how do we sum tuples? Say we have a list of `(Int, Double, Set[String])`, logically we want to sum the first, second and third field separately. Since we already have `Semigroup[T]` on `Int`, `Double` and `Set[U]`, we can compose them into a new semigroup. Note that this semigroup not only works for `(Int, Double, Set[String])` but any tuple 3 with arbitrary member types.

```scala
implicit def t3Sg[A: Semigroup, B: Semigroup, C: Semigroup] = new Semigroup[(A, B, C)] {
  val sgA = implicitly[Semigroup[A]]
  val sgB = implicitly[Semigroup[B]]
  val sgC = implicitly[Semigroup[C]]
  (sgA.plus(x._1, y._1), sgB.plus(x._2, y._2), sgC.plus(x._3, y._3))
}
  
sum(List(
  (1, 0.5, Set("a")),
  (2, 1.5, Set("b", "c")),
  (3, 2.5, Set("a", "b", "d"))))
// => (6, 4.5, Set("a", "b", "c", "d"))
```

Obviously we don't want to handcraft this for tuples from 2 to 22. Libraries like [Algebird](https://github.com/twitter/algebird) already include these common ones.

We can even generalize semigroup to maps. For two maps of `Map[K, V]` and a `Semigroup[V]`, we can sum the maps by summing values of the same key with the given semigroup.

```scala
implicit def mSg[K, V: Semigroup] = new Semigroup[Map[K, V]] {
  override def plus(x: Map[K, V], y: Map[K, V]): Map[K, V] =
    x ++ y.map { case (k, rv) =>
      val v = x.get(k) match {
        case Some(lv) => implicitly[Semigroup[V]].plus(lv, rv)
        case None => rv
      }
      (k, v)
    }
}
val m1 = Map(
  "a" -> (1, 0.5, Set("a")),
  "b" -> (2, 1.5, Set("b", "c")),
  "c" -> (3, 2.5, Set("a", "b", "c")))
val m2 = Map(
  "a" -> (10, 10.0, Set("a", "b")),
  "b" -> (20, 20.0, Set("c", "d", "e")),
  "d" -> (40, 100.0, Set("z")))
sum(List(m1, m2))
/*
=> Map(
  "a" -> (11, 10.5, Set("a", "b")),
  "b" -> (22, 21.5, Set("b", "c", "d", "e")),
  "c" -> (3, 2.5, Set("a", "b", "c")),
  "d" -> (40, 100.0, Set("z")))
*/
```

## Summary

That summarizes some main use cases of implicits. Here are some references.

- [Ordering](http://www.scala-lang.org/api/current/scala/math/Ordering.html) and [Numeric](http://www.scala-lang.org/api/current/scala/math/Numeric.html) type classes in Scala
- [Algebird](https://github.com/twitter/algebird) - Abstract Algebra for Scala
- My slides on [type classes](http://www.lyh.me/slides/type-classes.html) and [semigroups](http://www.lyh.me/slides/semigroups.html)
- Another excellent [blog post](http://www.lihaoyi.com/post/ImplicitDesignPatternsinScala.html) on implicit design patterns by Li Haoyi

We didn't discuss some more advanced topics like implicit resolution precedence and priority trick. Here are some more references.

- [Where does Scala look for implicits?](http://stackoverflow.com/questions/5598085/where-does-scala-look-for-implicits)
- [implicit parameter precedence again](http://eed3si9n.com/implicit-parameter-precedence-again)
- [Implicit prioritisation](https://gist.github.com/retronym/228673#file-low-priority-implicits-scala)
