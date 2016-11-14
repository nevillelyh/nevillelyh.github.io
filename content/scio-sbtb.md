Title: Scio at Scala by the Bay
Date: 2016-11-14 1:04PM
Category: code
Tags: data, scala, scio

It's been 7 months since we first announced [Scio](https://github.com/spotify/scio) at [GCPNEXT16](https://cloudplatformonline.com/NEXT2016.html). There're now dozens of internal teams and a couple of other companies using Scio to run hundreds of pipelines on a daily basis. Within [Spotify](https://www.spotify.com/), Scio is now the prefered framework for building new data pipelines on [Google Cloud Platform](http://cloud.google.com/). We've also made 19 released and added tons of features and improvements. Below is a list of some notable ones.

- Interactive REPL
- Type safe BigQuery macro improvements and [Scio-IDEA-plugin](https://github.com/spotify/scio-idea-plugin)
- BigQuery [standard SQL 2011 syntax](https://cloud.google.com/bigquery/docs/reference/standard-sql/) support
- HDFS source and sink
- Avro file compression support
- Bigtable multi-table sink and utility for cluster scaling
- Protobuf file support and usability improvements
- Accumulator usability improvements
- End-to-end testing utilities and matchers improvements
- Join performance improvements and skewed join
- Metrics interface and enhancements

I talked about Scio at [Scala by the Bay](http://scala.bythebay.io/) last week and here are the slides.

<iframe src="//www.slideshare.net/slideshow/embed_code/key/13tC6anQaZpNE8" width="800" height="490" frameborder="0" marginwidth="0" marginheight="0" scrolling="no" style="border:1px solid #CCC; border-width:1px; margin-bottom:5px; max-width: 100%;" allowfullscreen> </iframe> <div style="margin-bottom:5px"> <strong> <a href="//www.slideshare.net/sinisalyh/scio-a-scala-api-for-google-cloud-dataflow-apache-beam" title="Scio - A Scala API for Google Cloud Dataflow &amp; Apache Beam" target="_blank">Scio - A Scala API for Google Cloud Dataflow &amp; Apache Beam</a> </strong> from <strong><a target="_blank" href="//www.slideshare.net/sinisalyh">Neville Li</a></strong> </div>
