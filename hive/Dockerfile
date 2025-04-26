FROM bde2020/hive:2.3.2-postgresql-metastore

USER root

# Fix source issue for Debian Jessie and install wget
RUN echo "deb http://archive.debian.org/debian jessie main" > /etc/apt/sources.list \
 && apt-get update -o Acquire::Check-Valid-Until=false \
 && apt-get install --allow-unauthenticated -y wget

# Add S3A + AWS dependencies (hadoop-aws, aws-sdk, jackson)
RUN wget https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/2.7.4/hadoop-aws-2.7.4.jar -P /opt/hadoop-2.7.4/share/hadoop/common/lib && \
    wget https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk/1.7.4/aws-java-sdk-1.7.4.jar -P /opt/hadoop-2.7.4/share/hadoop/common/lib && \
    wget https://repo1.maven.org/maven2/com/fasterxml/jackson/core/jackson-core/2.6.5/jackson-core-2.6.5.jar -P /opt/hadoop-2.7.4/share/hadoop/common/lib && \
    wget https://repo1.maven.org/maven2/com/fasterxml/jackson/core/jackson-annotations/2.6.5/jackson-annotations-2.6.5.jar -P /opt/hadoop-2.7.4/share/hadoop/common/lib && \
    wget https://repo1.maven.org/maven2/com/fasterxml/jackson/core/jackson-databind/2.6.5/jackson-databind-2.6.5.jar -P /opt/hadoop-2.7.4/share/hadoop/common/lib
