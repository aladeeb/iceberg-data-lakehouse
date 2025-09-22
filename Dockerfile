FROM python:3.12.9-bullseye AS spark-base

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      sudo \
      curl \
      vim \
      unzip \
      rsync \
      openjdk-11-jdk \
      build-essential \
      software-properties-common \
      ssh && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

## Download spark and hadoop dependencies and install

# ENV variables
ENV SPARK_VERSION=3.5.6

ENV SPARK_HOME=${SPARK_HOME:-"/opt/spark"}
ENV HADOOP_HOME=${HADOOP_HOME:-"/opt/hadoop"}

ENV SPARK_MASTER_PORT=7077
ENV SPARK_MASTER_HOST=spark-master
ENV SPARK_MASTER="spark://$SPARK_MASTER_HOST:$SPARK_MASTER_PORT"

ENV PYTHONPATH=$SPARK_HOME/python/:$PYTHONPATH
ENV PYSPARK_PYTHON=python3

# Add iceberg spark runtime jar to IJava classpath
ENV IJAVA_CLASSPATH=/opt/spark/jars/*

RUN mkdir -p ${HADOOP_HOME} && mkdir -p ${SPARK_HOME}
WORKDIR ${SPARK_HOME}

RUN mkdir -p ${SPARK_HOME} \
    && curl https://dlcdn.apache.org/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop3.tgz -o spark-${SPARK_VERSION}-bin-hadoop3.tgz \
    && tar xvzf spark-${SPARK_VERSION}-bin-hadoop3.tgz --directory ${SPARK_HOME} --strip-components 1 \
    && rm -rf spark-${SPARK_VERSION}-bin-hadoop3.tgz

# Add spark binaries to shell and enable execution
RUN chmod u+x /opt/spark/sbin/* && \
    chmod u+x /opt/spark/bin/*
ENV PATH="$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin"

# Add a spark config for all nodes
COPY conf/spark-defaults.conf "$SPARK_HOME/conf/"


FROM spark-base AS pyspark

# Install python deps
COPY requirements.txt .
RUN pip3 install -r requirements.txt


FROM pyspark AS pyspark-runner

# # Download iceberg spark runtime
# TBD

# Download hadoop-aws and aws-java-sdk-bundle jars
RUN curl https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.4/hadoop-aws-3.3.4.jar -Lo /opt/spark/jars/hadoop-aws-3.3.4.jar
RUN curl https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.12.517/aws-java-sdk-bundle-1.12.517.jar -Lo /opt/spark/jars/aws-java-sdk-bundle-1.12.517.jar


COPY entrypoint.sh .
RUN chmod u+x /opt/spark/entrypoint.sh

# # Optionally install Jupyter
# FROM pyspark-runner AS pyspark-jupyter

# RUN pip3 install notebook

# ENV JUPYTER_PORT=8889

# ENV PYSPARK_DRIVER_PYTHON=jupyter
# ENV PYSPARK_DRIVER_PYTHON_OPTS="notebook --no-browser --allow-root --ip=0.0.0.0 --port=${JUPYTER_PORT}"
# # --ip=0.0.0.0 - listen all interfaces
# # --port=${JUPYTER_PORT} - listen ip on port 8889
# # --allow-root - to run Jupyter in this container by root user. It is adviced to change the user to non-root.


ENTRYPOINT ["./entrypoint.sh"]
CMD [ "bash" ]

# Now go to interactive shell mode
# -$ docker exec -it spark-master /bin/bash 
# then execute
# -$ pyspark

# If Jupyter is installed, you will see an URL: `http://127.0.0.1:8889/?token=...`
# This will open Jupyter web UI in your host machine browser.
# Then go to /warehouse/ and test the installation.