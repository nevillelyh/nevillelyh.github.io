Title: Automatic type-class derivation with Shapeless
Date: 2017-08-21 09:30AM
Category: code
Tags: scala, fp

We had a knowledge sharing session at work recently on [Shapeless](https://github.com/milessabin/shapeless/) for automatic type class derivation. Here is a little write-up for the topic.

## Scala List

First let's review how `List` works in Scala. A `List` is a linked list with `head` and `tail`, plus `Nil` for empty list. It can be represented with the following abstract data type:

```scala
sealed trait List[+A] {
  def ::[B >: A](head: B): List[B] = Cons(head, this)
}
case object Nil extends List[Nothing] // Nothing is a sub-type of every other type
case class Cons[+A](head: A, tail: List[A]) extends List[A]
```

Notice that `::`, the list concatenation operation, is just a method on trait `List[+A]`. Since Scala operators that end with `:` are right-associative, we can conveniently create lists by chaining multiple `::`s. Therefore the following expressions are equivalent:

```scala
1 :: 2 :: Nil
1 :: (2 :: Nil)
Nil.::(2).::(1)
Cons(1, Cons(2, Nil))
```

It's important to point out here that Scala `List` is homogeneous, i.e. it has a single type parameter `A` and thus can only store elements of `A` and its sub-types. On the other hand, it can have varying numbers of elements at runtime.

## Shapeless HList

Since `List` is homogeneous, the most common way to represent lists of different types in Scala is tuples. However, since tuples of different arities are different types (`Tuple2[A, B]`, `Tuple3[A, B, C]`, ...) and limited to 22 elements, it's hard to write generic code that operates on tuples of varying arities.

Heterogenous list, or `HList`, is the core type in Shapeless and can represent lists of varying lengths with different element types.

```scala
sealed trait HList

// HNil is both a type (trait) and an object
sealed trait HNil extends HList {
  def ::[H](head: H): H :: HNil = new ::(head, this)
}
case object HNil extends HNil
case class ::[+H, +T <: HList](head: H, tail: T) extends HList
  
implicit class HListOps[T <: HList](val self: T) extends AnyVal {
  def ::[H](head: H): H :: T = new ::(head, self)
}
```

And the following expressions are equivalent:

```scala
1 :: 3.14 :: "foo" :: true :: HNil
1 :: (3.14 :: ("foo" :: (true :: HNil)))
HNil.::(true).::("foo").::(3.14).::(1)
::(1, ::(3.14, ::("foo", ::(true, HNil))))
```

Note that there are two `::(head: H)` implementations with different return types `H :: HNil` and `H :: T`. This way types of all elements are retained and not erased to `HList` if `::` was only defined in `trait HList`.

Also note that in Scala, generic types with 2 type paramemters can be used in an infix position, i.e. `::[H, T]` == `H :: T`, and those that end with `:` are right-associative, we can conveniently create unique `HList` types in a syntax similar to `List` creation.

```scala
// ::[Int, ::[Double, HNil]]
type L1 = Int :: Double :: HNil

// ::(1, ::(3.14, HNil))
val l1: L1 = 1 :: 3.14 :: HNil

// ::[Int, ::[Double, ::[String, HNil]]]
type L2 = Int :: Double :: String :: HNil

// ::(1, ::(3.14, ::("foo", HNil)))
val l2: L2 = 1 :: 3.14 :: "foo" :: HNil

// ::[Int, ::[Double, ::[String, ::[Boolean, HNil]]]]
type L3 = Int :: Double :: String :: Boolean :: HNil

// ::(1, ::(3.14, ::("foo", ::(true, HNil))))
val l3: L3 = 1 :: 3.14 :: "foo" :: true :: HNil
```

We can see that each `HList` instance, i.e. `L1`, `L2`, `L3`, is a unique type with fixed but varying number of element types determined at compile time. But since all of them are instances of `HList` and recursively `H :: T`, we can operate them in a generic way with implicits.

## Implicit type-class derivation

Now let's look at how we can operate `HList` by recursively process `head` and `tail`. Say we have a `Flip[T]` type class that flips the value of type `T`, and implicit instances for `Int`, `Double`, `Boolean` and `String`.

```scala
trait Flip[T] {
  def apply(x: T): T
}

object Flip {
  def apply[T](f: T => T): Flip[T] = new Flip[T] {
    override def apply(x: T): T = f(x)
  }
}

implicit val intFlip = Flip[Int](-_)
implicit val doubleFlip = Flip[Double](-_)
implicit val booleanFlip = Flip[Boolean](!_)
implicit val stringFlip = Flip[String](_.reverse)
```

And we want to apply `Flip[T]` to an `Hlist` of arbitrary length and types. For an `HList` of `A :: B :: C :: D :: HNil`, we want to recursively summon implicit instances of `Flip[T]` for the heads, i.e. `A`, `B`, `C`, `D`, and the tails, i.e. `B :: C :: D :: HNil`, `C :: D :: HNil`, `D :: HNil`, `HNil`. As any recursive approach it's easy to start with the terminal case `HNil`.

```scala
import shapeless._

implicit val hnilFlip = Flip[HNil](_ => HNil)

implicit def hconsFlip[H, T <: HList]
(implicit hf: Flip[H], tf: Flip[T]) // summon implicit instances, tf is computed recursively
: Flip[H :: T] = new Flip[H :: T] {
  override def apply(x: H :: T): H :: T = hf(x.head) :: tf(x.tail)
}
```

Now we can summon an implicit `Flip[T]` with any `HList` instances.

```scala
def flip[T](x: T)(implicit f: Flip[T]) = f(x)

flip(1 :: 3.14 :: "foo" :: true :: HNil)
// Int :: Double :: String :: Boolean :: HNil = -1 :: -3.14 :: "oof" :: false :: HNil
```

The above code is expanded at compile time to:

```scala
val f = hconsFlip(intFlip,
  hconsFlip(doubleFlip,
    hconsFlip(stringFlip,
      hconsFlip(booleanFlip, hnilFlip))))
f.apply(1 :: 3.14 :: "foo" :: true :: HNil)
```

## Generic and LabelledGeneric

Now that we know how to operate `HList`s in a generic way, Shapeless also offers `Generic` and `LabelledGeneric` for operating tuples and case classes in the same manner. `Generic` is a type-class for conversion between Scala types and `HList`s.

```scala
// (Int, Double, String, Boolean) <=> Int :: Double :: String :: Boolean :: HNil
val gen = Generic[(Int, Double, String, Boolean)]

val l = gen.to((1, 3.14, "foo", true)) // 1 :: 3.14 :: "foo" :: true :: HNil
val t = gen.from(l) // (1, 3.14, "foo", true)
```

We can now extend `flip` to any tuples.

```scala
def flip[T, L <: HList](x: T)
                       (implicit gen: Generic.Aux[T, L], f: Flip[L]): T =
  gen.from(f(gen.to(x)))

// T = (Int, Double, String, Boolean)
// L = Int :: Double :: String :: Boolean :: HNil
// gen = Generic[(Int, Double, String, Boolean)]
// f = implicitly[Flip[Int :: Double :: String :: Boolean :: HNil]]
flip((1, 3.14, "foo", true))
// (Int, Double, String, Boolean) = (-1, -3.14, "oof", false)
```

`Generic` also works with case classes, so our `flip` method works automatically supports them as well.

```scala
case class Record(i: Int, d: Double, s: String, b: Boolean)
// Record <=> Int :: Double :: String :: Boolean :: HNil
val gen = Generic[Record]
val l = gen.to(Record(1, 3.14, "foo", true)) // 1 :: 3.14 :: "foo" :: true :: HNil
val g = gen.from(l) // Record(1, 3.14, "foo", true)

flip(Record(1, 3.14, "foo", true)) // Record(-1, -3.14, "oof", false)
```

You might have noticed that so far we've only operated on the types and values of individual fields, but not field names in a case class. `LabelledGeneric` is designed just for that by giving us access field names via the type system.

```scala
val gen = LabelledGeneric[Record]
// Int with shapeless.labelled.KeyTag[Symbol with shapeless.tag.Tagged[String("i")], Int]
// :: Double with shapeless.labelled.KeyTag[Symbol with shapeless.tag.Tagged[String("d")], Double]
// :: String with shapeless.labelled.KeyTag[Symbol with shapeless.tag.Tagged[String("s")], String]
// :: Boolean with shapeless.labelled.KeyTag[Symbol with shapeless.tag.Tagged[String("b")], Boolean]
// :: shapeless.HNil
```

Each field type e.g. `Int`, `Double` is extended with `KeyTag[K, V]` where `K` is a macro generated singleton type that uniquely represents the string value. Without diving too deep into the topic, we can retrieve the field name with the `Witness` type class.

```scala
import shapeless.labelled.FieldType

def name[K <: Symbol, V](f: FieldType[K, V])
                        (implicit wit: Witness.Aux[K]): String = wit.value.name

// l.head: Int with shapeless.labelled.KeyTag[Symbol with shapeless.tag.Tagged[String("i")], Int]
name(l.head) // "i"
```

We can now derive type classes that also depends on field names, for example `ToMap[T]` that converts `T` to `Map[String, Any]`.

```scala
import shapeless._
import shapeless.labelled.FieldType

trait ToMap[T] {
  def apply(x: T): Map[String, Any]
}

implicit val hnilToMap = new ToMap[HNil] {
  override def apply(x: HNil) = Map.empty
}

implicit def hconsToMap[K <: Symbol, H, T <: HList]
(implicit wit: Witness.Aux[K], ttm: ToMap[T])
: ToMap[FieldType[K, H] :: T] = new ToMap[FieldType[K, H] :: T] {
  override def apply(x: FieldType[K, H] :: T): Map[String, Any] =
    ttm(x.tail) + (wit.value.name -> x.head)
}

def toMap[T, L <: HList](x: T)
                       (implicit
                        gen: LabelledGeneric.Aux[T, L],
                        tm: ToMap[L]): Map[String, Any] =
  tm(gen.to(x))

case class Record(i: Int, d: Double, s: String, b: Boolean)
toMap(Record(1, 3.14, "foo", true)) // Map("b" -> true, "s" -> "foo", d -> 3.14, i -> 1)
```

## Type class companions

Now we know how to write generic code that works with tuples and case classes, but the above examples are still pretty verbose. Luckily there're are some helpers in shapeless to reduce boilerplate for these problems, namely `ProductTypeClassCompanion` and `LabelledProductTypeClassCompanion`.

The `ProductTypeClassCompanion` skeleton for `Flip[T]` looks like this:

```scala
import shapeless._

object FlipDerivedOrphans extends ProductTypeClassCompanion[Flip] {
  override val typeClass = new ProductTypeClass[Flip] {
    override def product[H, T <: HList](ch: Flip[H], ct: Flip[T]): Flip[H :: T] = ???
    override def emptyProduct: Flip[HNil] = ???
    override def project[F, G](instance: => Flip[G], to: F => G, from: G => F): Flip[F] = ???
  }
}
```

It's easy to fill in the blanks.

```scala
object FlipDerivedOrphans extends ProductTypeClassCompanion[Flip] {
  override val typeClass = new ProductTypeClass[Flip] {
    override def product[H, T <: HList](ch: Flip[H], ct: Flip[T]): Flip[H :: T] =
      Flip[H :: T](x => ch(x.head) :: ct(x.tail))
    override def emptyProduct: Flip[HNil] = Flip[HNil](_ => HNil)
    override def project[F, G](instance: => Flip[G], to: F => G, from: G => F): Flip[F] =
      Flip[F](f => from(instance(to(f))))
  }
}

implicit def deriveFlip[T]
(implicit orphan: Orphan[Flip, FlipDerivedOrphans.type, T])
: Flip[T] = orphan.instance

case class Record(i: Int, d: Double, s: String, b: Boolean)
val f = implicitly[Flip[Record]]
f(Record(1, 3.14, "foo", true))
```

Likewise we can use `LabelledProductTypeClassCompanion` for `ToMap[T]`.

```scala
object ToMapDerivedOrphans extends LabelledProductTypeClassCompanion[ToMap] {
  override val typeClass = new LabelledProductTypeClass[ToMap] {
    override def product[H, T <: HList](name: String, ch: ToMap[H], ct: ToMap[T]): ToMap[H :: T] =
      new ToMap[H :: T] {
        override def apply(x: H :: T): Map[String, Any] = ct(x.tail) + (name -> x.head)
      }
    override def emptyProduct: ToMap[HNil] =
      new ToMap[HNil] {
        override def apply(x: HNil): Map[String, Any] = Map.empty
      }
    override def project[F, G](instance: => ToMap[G], to: F => G, from: G => F): ToMap[F] =
      new ToMap[F] {
        override def apply(x: F): Map[String, Any] = instance(to(x))
      }
  }
}

implicit def deriveToMap[T]
(implicit orphan: Orphan[ToMap, ToMapDerivedOrphans.type, T])
: ToMap[T] = orphan.instance

case class Record(i: Int, d: Double, s: String, b: Boolean)
val f = implicitly[ToMap[Record]]
f(Record(1, 3.14, "foo", true))
```

However this doesn't work right away. The compiler complains about `could not find implicit value for parameter e: ToMap[Record]`. Upon closer inspection, we can see that even though the `ch: ToMap[H]` argument in `def product` is unused, it's still summoning implicits for `Int`, `Double`, `String` and `Boolean`. This can be worked around by introducing dummy instances like below. Since `dummyToMap` is in the companion `object ToMap` which has lower priority than `deriveToMap` in the current scope, it's only used for `ch: TopMap[H]` and not `implicitly[ToMap[Record]]`. This is obviously not the most elegant solution and only used here to demonstrate common problems when designing and deriving type classes. A better solution might be using an ADT as `ToMap#apply` return type instead of `Map[String, Any]`, and use pattern matching to handle head (single field) vs. tail (`Map`) cases.

```scala
object ToMap {
  implicit def dummyToMap[T] = new ToMap[T] {
    override def apply(x: T) = ???
  }
}
```

This concludes the write-up. However there're still some topics not covered, like `Coproduct` and more complex scenarios for implicit lookup.

## References

- [Shapeless feature overview](https://github.com/milessabin/shapeless/wiki/Feature-overview:-shapeless-2.0.0)
- [Shows](https://github.com/milessabin/shapeless/blob/master/examples/src/main/scala/shapeless/examples/shows.scala) and [Monoid](https://github.com/milessabin/shapeless/blob/master/examples/src/main/scala/shapeless/examples/monoids.scala) examples in Shapeless
- [StackOverflow question on Coproduct](https://stackoverflow.com/questions/25517069/what-is-the-purpose-of-the-emptycoproduct-and-coproduct-methods-of-the-typeclass)
- [The Type Astronaut's Guide to Shapeless](http://underscore.io/books/shapeless-guide/)
- [Implicit parameter precedence again](http://eed3si9n.com/implicit-parameter-precedence-again)
