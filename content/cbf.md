Title: CanBuildFrom
Date: 2017-05-18 9:46AM
Category: code
Tags: scala, fp

We recently had an internal knowledge sharing on higher-kinded types and `CanBuildFrom` type classes in Scala. Here's a short summary.

## Basics

Let's start by implementing `map`.

```scala
def map(xs: Seq[Int], f: Int => Double): Seq[Double] = xs.map(f)
map(Seq(1, 2, 3), _ + 0.1)
```

This implementation is not very good since it only works with `Seq[Int]` and `Int => Double`. It's easy to parameterize `Int` and `Double`.

```scala
def map[A, B](xs: Seq[A], f: A => B): Seq[B] = xs.map(f)
```

However `map(Seq(1, 2, 3), _ + 0.1)` now fails to compile with a message `missing parameter type for expanded function ((x$1) => x$1.$plus(10))`

This is because inference of `A` in `f: A => B` depends on the type of `xs: Seq[A]`, and limitation of Scala type inference. A common workaround is to curry arguments.

```scala
def map[A, B](xs: Seq[A])(f: A => B): Seq[B] = xs.map(f)
map(Seq(1, 2, 3))(_ + 0.1)
```

Similar pattern is commonly seen in Scala, like `foldLeft(z: B)(op: (B, A) => B)`. Another benefit is we can now write `f` in a multi-line `{}` block more elegantly.

```scala
map(Seq(1, 2, 3)) { x =>
  val y = x + 0.1
  println(s"$x + 0.5 = $y")
  y
}
```

## Higher-kinded types

However this version still only works on `Seq[A]`. We could parameterize it as `M[_]`, also known as higher-kinded type.

```scala
import scala.language.higherKinds
def map[M[_], A, B](xs: M[A])(f: A => B): M[B] = xs.map(f)
```

But now we have a compiler error saying `value map is not a member of type parameter M[A]`. We can add a upper bound for `M[_]` but it still wouldn't work.

```scala
def map[M[_] <: Seq[A], A, B](xs: M[A])(f: A => B): M[B] = xs.map(f)
```

Despite the fact that `M[_]` is a sub-type of `Seq[A]`, and `Seq[A]` has a `map` method, we can't build a `M[B]` back from `Seq[A]#map[B](f: A => B)`, since `M[B]` is a more specific type than `Seq[B]`.

```
type mismatch;
[error]  found   : Seq[B]
[error]  required: M[B]
```

However if we look at the method signature of `Seq[A]#map(f: A => B)` it actually looks like this.

```scala
trait TraversableLike[+A, +Repr] {
  def map[B, That](f: A => B)(implicit bf: CanBuildFrom[Repr, B, That]): That
}
```

Note that it's a method on `trait TraversableLike`, which means any `TraversableLike` collection can share the same `map` implementation. Also worth noting is `Seq[+A]` has an inheritance hierarchy like this:

```scala
trait Seq[+A] extends SeqLike[A, Seq[A]] // ...
trait SeqLike[+A, +Repr] extends IterableLike[A, Repr] // ...
trait IterableLike[+A, +Repr] extends TraversableLike[A, Repr] // ...
```

We see that in `Seq[A] extends SeqLike[A, Seq[A]]`, type of the current trait `Seq[A]` is also used as a type parameter for the super-type, which is propagated all the way to `TraversableLike`. This is commonly known as F-bounded polymorphism, which is useful heere since methods on sub-types of `TraversableLike` can now return a more specific type, e.g. `Seq`, `List`, `Vector`, instead of the same broad super-type. For more information on F-bounded polymorphism, check out Marconi Lanna's [excellent presentation](https://github.com/marconilanna/NEScala2015) at NEScala 2015.

In the case of `Seq[Int]#map(f: Int => Double)`, we can expand the method like this:

```scala
def map[Int, That](f: Int => Double)(implicit bf: CanBuildFrom[Seq[Int], Double, That])
```

## CanBuildFrom

`CanBuildFrom` is a key type class in the Scala collections library and enables a lot code reuse.

```scala
trait CanBuildFrom[-From, -Elem, +To]
```

In its type signature, `From` is the original collection and `To` is the target collection. `Elem` is the element type of the target collection and in some determines the type of `To`. For example we can map over a `Map[K, V]` into `K -> V` (which is a syntactic sugar for `(K, V)`), and get another map. However mapping into `String` would result in a `List[String]` since one cannot build a `Map[K, V]` with a single type.

```scala
// From: Map[String, Int]
// (String, Int) => (String, Double)
// To: Map[String, Double]
// CanBuildFrom[Map[String, Int], (String, Double), Map[String, Double]]
Map("a" -> 1, "b" -> 2).map(kv => kv._1 -> kv._2 + 0.1)

// From: Map[String, Int]
// (String, Int) => String
// To: List[String]
// CanBuildFrom[Map[String, Int], String, List[String]]
Map("a" -> 1, "b" -> 2).map(kv => kv._1 + kv._2.toString)
```

We can use `CanBuildFrom` to rewrite our `map` function.

```scala
def map[M[_] <: Seq[A], A, B](xs: M[A])(f: A => B)
                             (implicit cbf: CanBuildFrom[M[A], B, M[B]]): M[B] = {
  val b = cbf() // new Builder[Elem, To]
  xs.foreach(x => b += f(x))
  b.result()
}
```

Our function can now support any `Seq` types without losing the type information.
