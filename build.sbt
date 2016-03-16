organization  := "weather-forecastr"

version       := "0.1"

scalaVersion  := "2.11.7"

scalacOptions := Seq("-unchecked", "-deprecation", "-encoding", "utf8")



resolvers ++= Seq(
Resolver.bintrayRepo("scalaz", "releases")
)


libraryDependencies ++= {
  val sparkVersion = "1.6.0"



  Seq(
    "org.apache.spark" %% "spark-core" % sparkVersion,
  "org.apache.spark" %% "spark-streaming" % sparkVersion
)
}

resolvers += "typesafe repo" at " http://repo.typesafe.com/typesafe/releases/"
