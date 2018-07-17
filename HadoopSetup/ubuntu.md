#!/bin/bash
sudo apt-get update
sudo apt-get -y install default-jre
wget http://apache-mirror.rbc.ru/pub/apache/hadoop/common/hadoop-2.9.0/hadoop-2.9.0.tar.gz
tar xvfz hadoop-2.9.0.tar.gz
echo 'export JAVA_HOME=$(dirname $(dirname $(readlink -f $(which java))))' >> ~/.bashrc
echo 'export HADOOP_HOME=~/hadoop-2.9.0' >> ~/.bashrc
echo PATH=$PATH:~/hadoop-2.9.0/bin >> ~/.bashrc
source ~/.bashrc
echo 'export JAVA_HOME=$(dirname $(dirname $(readlink -f $(which java))))' >> ~/hadoop-2.9.0/etc/hadoop/hadoop-env.sh
echo '<configuration><property><name>fs.defaultFS</name><value>hdfs://localhost:9000</value></property></configuration>' > ~/hadoop-2.9.0/etc/hadoop/core-site.xml
echo '<configuration><property><name>dfs.replication</name><value>1</value></property></configuration>' > ~/hadoop-2.9.0/etc/hadoop/hdfs-site.xml
ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
chmod 0600 ~/.ssh/authorized_keys
ssh-keyscan -H 0.0.0.0 >> ~/.ssh/known_hosts
ssh-keyscan -H 127.0.0.1 >> ~/.ssh/known_hosts
ssh-keyscan -H ::1 >> ~/.ssh/known_hosts
ssh-keyscan -H localhost >> ~/.ssh/known_hosts
~/hadoop-2.9.0/bin/hdfs namenode -format
~/hadoop-2.9.0/sbin/start-dfs.sh
exec bash
