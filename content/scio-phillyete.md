Title: Scio at Philly ETE
Date: 2017-04-20 11:12AM
Category: code
Tags: data, scala, scio

It's been another 6 months since my talk about [Scio](https://github.com/spotify/scio) at [Scala by the Bay](http://scala.bythebay.io). We've seen huge adoption and improvements since then. The number of production Scio pipelines has grown from ~70 to 400+ within [Spotify](https://www.spotify.com/). A lot of other companies are using and contributing to it as well. In the most recent edition of the Spotify data university, an internal week long big data training camp for non-data engineers, we revamped the curriculum to cover Scio, BigQuery and other [Google Cloud Big Data](https://cloud.google.com/solutions/big-data/) products instead of Hadoop, Scalding and Hive.

<blockquote class="twitter-tweet" data-lang="en"><p lang="en" dir="ltr">Spotify data university round 3 &amp; 1st time covering Scio, <a href="https://twitter.com/ApacheBeam">@ApacheBeam</a> &amp; <a href="https://twitter.com/GCPBigData">@GCPBigData</a> 👋 Hadoop, HDFS, M/R, YARN 🍾 batch + streaming <a href="https://t.co/1gWIEbN0mW">pic.twitter.com/1gWIEbN0mW</a></p>&mdash; Neville Li (@sinisa_lyh) <a href="https://twitter.com/sinisa_lyh/status/846549633367265281">March 28, 2017</a></blockquote>
<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>

And here's a list of some notable improvements in Scio.

- Master branch is now based on [Apache Beam](https://beam.apache.org/)
- Graduate type safe BigQuery API form experimental to stable
- [Sparkey](https://github.com/spotify/sparkey-java) side input support
- [TensorFlow](https://www.tensorflow.org/) TFRecord file IO
- [Cloud Pub/Sub](https://cloud.google.com/pubsub/) attributes support
- Named transformations for streaming update
- Safe-guard against malformed tests and better error messages
- Flexible custom IO wiring
- KryoRegistrar for custom Kryo serialization
- Table description for type-safe BigQuery
- Lots of performance improvements and bug fixes

I talked about Scio at [Philly ETE](http://2017.phillyemergingtech.com/) last week and here are the slides.

<iframe src="//www.slideshare.net/slideshow/embed_code/key/15xefjkymEWvVV" width="800" height="490" frameborder="0" marginwidth="0" marginheight="0" scrolling="no" style="border:1px solid #CCC; border-width:1px; margin-bottom:5px; max-width: 100%;" allowfullscreen> </iframe> <div style="margin-bottom:5px"> <strong> <a href="//www.slideshare.net/sinisalyh/scio-moving-to-google-cloud-a-spotify-story" title=" Scio - Moving to Google Cloud, A Spotify Story" target="_blank"> Scio - Moving to Google Cloud, A Spotify Story</a> </strong> from <strong><a target="_blank" href="https://www.slideshare.net/sinisalyh">Neville Li</a></strong> </div>
