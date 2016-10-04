Title: On being a polyglot
Date: 2014-08-21 9:26PM
Category: code
Tags: c, cpp, python, javascript, scala, java, clojure, haskell

I'm kind of known as a polyglot among coworkers. We would often argue that instead of hiring great Java/Python/C++ developers, we should rather strive to hire great engineers with strong CS fundamentals who can pick up any language easily. I came from scientific computing background, doing mostly C/C++/Python many years ago. Over the course of the last three years at my current job I coded seven languages professionally, some out of interest and some necessity. I enjoyed the experience learning all these different things and want to share my experience here, what I learned from each one of them and how it helps me becoming a better engineer.

## C

The first language I used seriously, apart from LOGO & BASIC when I was a kid of course. It's probably the closest thing one can get to the operating system and bare metal without dropping down to assembly (while you still can in C). It's a simple language whose syntax served as the basis of many successors like C++ & Java. It doesn't offer any fancy features like OOP or namespaces, but rather depends on the developer's skill for organizing large code base (think Linux kernel or git).

Memory management is probably the biggest thing one get from learning the language, and to this day I'm still glad that I learned data structures in C. There are also other low level stuff like interrupts, system calls, and multi-threading which are often abstracted away in higher level languages. For these reasons I would argue that any professional developer should know some C.

I still remember programming my 9-pin dot-matrix printer with bit operators and ports; my first pre-Windows GUI with interrupts and VGA memory access; first e-mail client with UNIX sockets; first shell with all those Unix system calls; and learning two-phase commit by implementing it for [SQLite](http://www.sqlite.org/). While I rarely use C nowadays, many concepts pop up in day to day work and are essential in understanding much more complex systems.

## C++

A natural next step after C, C++ adds OOP and many more features like streams, operator overloading, and templates. Several books were instrumental to understanding the language better, including Scott Meyers' [Effective C++](http://www.amazon.com/Effective-Specific-Improve-Programs-Designs/dp/0321334876) series, and Stanley Lippman's [Inside the C++ Object Model](http://www.amazon.com/Inside-Object-Model-Stanley-Lippman/dp/0201834545). The former is regarded as a must read for all C++ programmers, while the latter dig into the language implementation of some mysterious features like object construction, virtual methods, and multiple inheritance. I actually read Effective C++ before studying the language. The first pass was not 100% clear but combined with practise and real world experience, the second read made a lot more sense and really made me comfortable with the language.

I started using it mostly in school for scientific computing, as "C with classes", where one rarely relies on auto memory management & threading. Memory were allocated in big chunks, or managed with STL collections, and often read-only once loaded. And processing large amount of data is often embarrassingly parallel, i.e. crunching through input files in threads.

Fast forward to my current job, C++ is mostly used in the desktop application, heavily threaded with many small objects encapsulating asynchronous backend requests and JavaScript bridge with [CEF](https://code.google.com/p/chromiumembedded/). Race conditions, memory leaks and null pointer crashes are common problems and I started to appreciate mutexes & [boost smart pointers](http://www.boost.org/doc/libs/1_56_0/libs/smart_ptr/smart_ptr.htm). Features like [template specialization](http://www.cprogramming.com/tutorial/template_specialization.html) also helps in creating generic & performant code while paving the way for understanding type classes in Scala & Haskell.

## Python

Probably the most popular of the bunch, Python is favored by many data scientists for its wide range of data processing libraries and I originally picked it up for information retrieval. It's easy to learn, concise, and perfect for ad-hoc analysis or as a utility language. A colleague once said that any competent programmer should know one static and one dynamic language well, and in that case Python would be many people's choice for the dynamic one.

When it comes to implementing complex algorithms quickly, list comprehension got me hooked first. Then it was lambda, map, reduce, filter, zip and that was when I discovered functional programming. After that came things like [itertools](https://docs.python.org/2/library/itertools.html) and [functools](https://docs.python.org/2/library/functools.html). To me Python was the gateway language to functional programming.

I also did a lot of backend work in Python, and learn to hate [GIL](https://wiki.python.org/moin/GlobalInterpreterLock) and love [gevent](http://www.gevent.org/). Performance was still an issue and significant amount of time was spent profiling and optimizing code. And through the process I got a much better understanding of the non-blocking event-driven concurrency model.

## JavaScript

JavaScript is a language that I write out of necessity, mostly when working with [Spotify Apps](https://developer.spotify.com/technologies/apps/) and my [audio visualization](http://labs.spotify.com/2013/11/14/announcing-spotify-visualization-api-beta/) hack project. It's one of those languages that I never learned properly. While the language isn't drastically different from the previous ones, I did have to wrap my head around various (ab)uses of closure and the whole async requests and callbacks concept, and you learn to organize the code around that to make it more maintainable.

## Scala

I introduced Scala back to my current job and use it on a daily basis. There are a lot of controversy around the language, mostly due to its steep learn curve and complexity. Learning curve was not so much of a problem for someone who already knows Python and C++, although there are still concepts harder to digest, like variances, bounds and type classes. Complexity, IMHO, was partly due to the limitation of the JVM, e.g. erasure and boxed primitives. Despite these problems, Scala seems to have found a sweet spot in the domain of big data, where it allows both development agility and performance, plus interoperability with other JVM system (Hadoop, Storm, Cassandra, etc.). Apart from powerful generics and operator overloading, Scala took a step further from C++ with implicits, making it easier to extend existing libraries or design new DSLs. [Scalding](https://github.com/twitter/scalding), [Spark](http://spark.apache.org/), and [Kafka](http://kafka.apache.org/) are probably the most well known Scala projects, while newcomers like [BIDMach](https://github.com/BIDData/BIDMach) are showing a lot of potential.

When it comes to learning the language, Twitter's [Scala School](https://twitter.github.io/scala_school/) and Horstmann's [Scala for the Impatient](http://www.horstmann.com/scala/) are both excellent resources and I enjoyed Joshua Suereth's [Scala in Depth](http://www.manning.com/suereth/) for advanced topics. The biggest reward, often absent from books & tutorials however, is abstract algebra and category theory. Sooner or later terms like monoid, semigroup, monad will pop up and you'll recognize such patterns in map/reduce, storm, and even Java libraries like [Guava](https://code.google.com/p/guava-libraries/). To me, that's the most important thing I learned from using Scala.

## Java

Another language I use out of necessity. It's often contempted in the start up world for verbosity and enterprise heritage. Most colleges teach Java in programming 101 and that was my only previous encounter with it (although I skipped most classes in school). The language has a very conservative set of features and probably not a challenge for any seasoned C++ developers. People often associate Java with design patterns, for better or worse, and IMHO a lot of them, like builder, factory, delegate, were really created to overcome the limitation of the language.

One area that Java excels in, however, is its ecosystem of libraries, tools, IDEs. Before Java I did almost all coding in Vim, using Xcode or Eclipse occasionally for debugging C++ code. After using [IntelliJ IDEA](http://www.jetbrains.com/idea/) for a few weeks, I'd say that it's probably the biggest attraction for writing Java. Verbosity becomes less of a problem once you get used to the IDE's features for code navigation, completion, and refactoring. Dependency management is also easier without various platform specific packages. And coming from doing backend in a Python world, the quality and maturity of libraries in the JVM world is so much better. We ended up spending a lot less time struggling with memcached, Cassandra or HTTP clients.

## Clojure

The latest language I used at work. We use it mainly for defining monitoring rules in [Riemann](http://riemann.io/) and I also hacked together a few [Storm](http://storm-project.net/) topologies in Clojure. With some Scala experience by the time I picked it up, most concepts are no stranger to me. Syntax is surprisingly simple and consistent. I often joke that it's my language of choice on a plane or boat with no internet, since the core language [cheat sheet](http://clojure.org/cheatsheet) fits on a single page. And Its inherently lazy sequence library maps naturally to stream processing and is also fun for solving [Project Euler](http://projecteuler.net/) problems.

Some coworkers were appalled by the excessive use of parentheses and existence of plugins like [rainbow_parentheses.vim](https://github.com/kien/rainbow_parentheses.vim). Yes we talk smack about it, joking that 40 columns is enough and one should hook up an elliptical machine to `(` and `)`. But I also think of it as a restraint of complexity and break my code down to smaller, reuseable functions.

Clojure is also the first time I was exposed to macros (not the `#define` kind in C/C++), [software transactional memory](http://en.wikipedia.org/wiki/Software_transactional_memory), and [homoiconic](http://en.wikipedia.org/wiki/Homoiconicity) programming languages. Concepts that broadened my understanding of programming language design.

## (Bonus) Haskell

I always regretted not learning Haskell ever since switching to [XMonad](http://xmonad.org/) as my window manager. If Python was my gateway drug to functional programming, then Scala, and more specifically [scalaz](https://github.com/scalaz/scalaz), are my gateway drug to Haskell, the pure functional programming language with strong academic background.

I recently picked up the language again, going through the excellent free book [Learn You a Haskell for Great Good!](http://learnyouahaskell.com/) side by side with [learning scalaz](http://eed3si9n.com/learning-scalaz/index.html). It's easy to see the parallel between the two, how some concepts built into the Haskell language are implemented with generics and implicits in scala(z). It's also not hard to see why Haskell attracts interest, with its powerful type inferences, type classes, lazy evaluation and many other features.

I probably won't use Haskell for real any time soon. I probably won't even use those features in scalaz or [shapeless](https://github.com/milessabin/shapeless) in production. Nevertheless I really enjoyed learning these concepts and see how they solve problems with elegance.

## Final words

You might also say that I'm a jack of all trades and master of none. This is very true and I never became a master of any of these languages and created a framework or library. On the other hand this also allows me to pick up any task or role within the team and quickly become productive. And I often found myself applying techniques from one language to another. All in all I believe it's much more beneficial to be a polyglot than sticking to one language and platform.
