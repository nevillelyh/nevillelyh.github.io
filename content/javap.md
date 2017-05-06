Title: Decompiling Scala code
Date: 2017-05-06 5:14PM
Category: code
Tags: scala, fp

I was bored today and decided to decompile some Scala code for fun and profit. I'm using Scala 2.12.2 and Java 1.8.0_121.

## Scala object

```scala
package javap

object Test01 {
  def main(args: Array[String]): Unit = Unit
}
```

```java
public final class javap.Test01$ {
  public static javap.Test01$ MODULE$;
  public static {};
  public void main(java.lang.String[]);
  private javap.Test01$();
}

public final class javap.Test01 {
  public static void main(java.lang.String[]);
}

```

As we can see a Scala object is compiled to 2 Java classes, `Test01` with static methods for Java compatibility and a `Test01$` with a static instance of itself as `MODULE$`, so that `Test01` can be used as an instance value in Scala.

## Class constructors

```scala
package javap

class Test02(val x: Int, val y: Int, z: Int) {
  def this(x: Int, y: Int) = this(x, y, 0)
}
```

```java
public class javap.Test02 {
  private final int x;
  private final int y;
  public int x();
  public int y();
  public javap.Test02(int, int, int);
  public javap.Test02(int, int);
}

```

Looks like the default constructor `(val x: Int, val y: Int, z: Int)` and the overloaded one `(x: Int, y: Int)` each generated a Java constructor. However only `x` and `y` are `val`s and became public member methods of the class, while `z` is used as a constructor argument only.

## Traits

```scala
package javap

trait Test03 {
  val x: Int = ???
  def f(x: Int): Int = ???
}
```

```java
public interface javap.Test03 {
  public abstract void javap$Test03$_setter_$x_$eq(int);
  public abstract int x();
  public static int f$(javap.Test03, int);
  public int f(int);
  public static void $init$(javap.Test03);
}

```

So `trait`s are not too different from `object`s. However method `f` generated two versions, one static with the `Test03` itself as an additional argument and one member method. There's also a setter method, most likely to allow overriding `x` in sub-types.

## Member `val`s

```scala
package javap

class Test04 {
  val a: Int = ???
  lazy val b: Int = ???
  @transient lazy val c: Int = ???
  implicit val d: Int = ???
}
```

```java
public class javap.Test04 {
  private int b;
  private transient int c;
  private final int a;
  private final int d;
  private volatile byte bitmap$0;
  public int a();
  private int b$lzycompute();
  public int b();
  private int c$lzycompute();
  public int c();
  public int d();
  public javap.Test04();
}

```

Here we can see clearly that Scala `val`s are compiled as accessor methods and private field. `b` and `c` are lazy and generated two `lzycompute` methods. In addition `c` is transient and the underlying field is marked so as well. There's also a `bitmap$0` to keep track of the states of `lazy val`s. See this StackOverflow [thread](http://stackoverflow.com/questions/6877040/in-compiled-scala-what-is-the-bitmap0-field0).

## Primitives

```scala
package javap

class Test05 {
  def plus1(x: Int, y: Int): Int = ???
  def plus2[T](x: T, y: T): T = ???
  def plus3[@specialized(Int, Long, Float, Double) T](x: T, y: T): T = ???
}
```

```java
public class javap.Test05 {
  public int plus1(int, int);
  public <T> T plus2(T, T);
  public <T> T plus3(T, T);
  public double plus3$mDc$sp(double, double);
  public float plus3$mFc$sp(float, float);
  public int plus3$mIc$sp(int, int);
  public long plus3$mJc$sp(long, long);
  public javap.Test05();
}

```

Unlike Java, which has primitive (`int`, `long`, etc.) and boxed (`Integer`, `Long`, etc.) types, Scala has unified primitive types and will choose the appropriate type in generated code, like primitives in most cases and boxed types in generic classes. We can see here that `plus1` and `plus2` are identical to how one would write then in Java. However `plus3` generates one generic version and 4 specialized versions.

See these [slides](http://www.lyh.me/slides/primitives.html) for a more in depth discussion of Scala primitives.

## Functions

```scala
package javap

class Test06 {
  def map(xs: Array[Int], f: Int => Int): Array[Int] = xs.map(f)
  def f(x: Int): Int = ???
  val g = f _
  val h = (x: Int) => x + 1: Int
}
```

```java
public class javap.Test06 {
  private final scala.Function1<java.lang.Object, java.lang.Object> g;
  private final scala.Function1<java.lang.Object, java.lang.Object> h;
  public int[] map(int[], scala.Function1<java.lang.Object, java.lang.Object>);
  public int f(int);
  public scala.Function1<java.lang.Object, java.lang.Object> g();
  public scala.Function1<java.lang.Object, java.lang.Object> h();
  public static final int $anonfun$g$1(javap.Test06, int);
  public static final int $anonfun$h$1(int);
  public javap.Test06();
  private static java.lang.Object $deserializeLambda$(java.lang.invoke.SerializedLambda);
}

```

These Scala anonymous functions are realy just instances of the trait `Function1[T, R]`. Scala generates both static methods (`$anonfun$g$1`, `$anonfun$h$1`) and function instances (`g()`, `h()`) for `g` and `f` since they are declared as `val`s. `f` is declared as a method and has no instances. This will probably happen at the call site.

## Other features

```scala
package javap

class Test07 {
  def plus1(x: Int, y: Int, z: Int = 0): Int = ???
  def plus2(x: Int)(y: Int)(z: Int): Int = ???
  def plus3(x: Int)(implicit y: Int): Int = ???
  def plus4[T](x: T, y: T)(implicit num: Numeric[T]): T = ???
  def plus5[T: Numeric](x: T, y: T): T = ???
}
```

```java
public class javap.Test07 {
  public int plus1(int, int, int);
  public int plus1$default$3();
  public int plus2(int, int, int);
  public int plus3(int, int);
  public <T> T plus4(T, T, scala.math.Numeric<T>);
  public <T> T plus5(T, T, scala.math.Numeric<T>);
  public javap.Test07();
}

```

Here we can see that there's not much special in the generated methods. Method `plus1` with default argument generated a special case. While curried `plus2` and `plus3` with implicit argument don't look special at all. `plus4` and `plus5` look identical since an `implicit` type class argument is equivalent to a context bound `[T: Numeric]`.

## Conclusion

In my experience as a library builder, digging into generated byte code allows me to better understand the following topics

- Java inter-op, e.g. Scala features that translate well or badly when called in Java
- Performance considerations, e.g. primitive vs. boxed types, class method vs. function instances
- Serialization implications, e.g. pulling in non-serializable trait or object module, or initialization sequence of `@transient lazy val`s

The script that generated these can be found at <https://github.com/nevillelyh/scala-playground/blob/master/javap.sh>.
