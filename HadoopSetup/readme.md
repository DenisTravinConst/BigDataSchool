CentOS7:

  #!/bin/bash
  sudo yum -y install wget
  sudo yum -y install java-1.8.0-openjdk
  wget http://apache-mirror.rbc.ru/pub/apache/hadoop/common/hadoop-2.9.0/hadoop-2.9.0.tar.gz
  tar xvfz hadoop-2.9.0.tar.gz
  echo 'export JAVA_HOME=/usr/lib/jvm/jre-1.8.0-openjdk' >> ~/.bashrc
  echo 'export HADOOP_HOME=~/hadoop-2.9.0' >> ~/.bashrc
  source ~/.bashrc
  echo 'export JAVA_HOME=/usr/lib/jvm/jre-1.8.0-openjdk' >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh
  PATH=$PATH:~/hadoop-2.9.0/bin
  echo '<configuration><property><name>fs.defaultFS</name><value>hdfs://localhost:9000</value></property></configuration>' > $HADOOP_HOME/etc/hadoop/core-site.xml
  echo '<configuration><property><name>dfs.replication</name><value>1</value></property></configuration>' > $HADOOP_HOME/etc/hadoop/hdfs-site.xml
  ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa
  cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
  chmod 0600 ~/.ssh/authorized_keys
  hdfs namenode -format
  #press yes here if it is necessary
  $HADOOP_HOME/sbin/start-dfs.sh
  hdfs dfs -mkdir /test
  hdfs dfs -ls /
