# To configure hive on hadoop

-> wget http://www-us.apache.org/dist/hive/hive-2.1.0/apache-hive-2.1.0-bin.tar.gz

-> tar xvzf apache-hive-2.1.0-bin.tar.gz 

-> mv apache-hive-2.1.0-bin /hive

-> vi ~/.bashrc
add the following lines to this file:

export HIVE_HOME=/hive
export HIVE_CONF_DIR=/hive/conf
export PATH=$HIVE_HOME/bin:$PATH
export CLASSPATH=$CLASSPATH:/etc/hadoop/lib/*:.
export CLASSPATH=$CLASSPATH:/hive/lib/*:.

-> hdfs dfs -ls /
-> hdfs dfs -mkdir /user/hive/warehouse
-> hdfs dfs -chmod g+w /tmp
-> hdfs dfs -chmod g+w /user/hive/warehouse
-> hdfs dfs -ls /user

-> cd /hive/conf
-> cp hive-env.sh.template hive-env.sh
Edit the hive-env.sh file by appending the following line:
export HADOOP_HOME=/etc/hadoop

## Hive installation is completed successfully. Now we need an external database server to configure Metastore. We use Apache Derby database.

-> wget http://archive.apache.org/dist/db/derby/db-derby-10.13.1.1/db-derby-10.13.1.1-bin.tar.gz
-> tar xvzf db-derby-10.13.1.1-bin.tar.gz
-> mv db-derby-10.13.1.1-bin /derby

set up the Derby environment by appending the following lines to ~/.bashrc file:
-> vim ~/.bashrc
add the following line:

export DERBY_HOME=/derby
export PATH=$PATH:$DERBY_HOME/bin
export CLASSPATH=$CLASSPATH:$DERBY_HOME/lib/derby.jar:$DERBY_HOME/lib/derbytools.jar

**create a directory named data in $DERBY_HOME directory to store Metastore data**
-> mkdir $DERBY_HOME/data
-> exec bash
**Configuring Hive Metastore**

-> cd $HIVE_HOME/conf
-> cp hive-default.xml.template hive-site.xml

*create a file name jpox.properties in conf location*
-> vim jpox.properties

add the following lines:

javax.jdo.PersistenceManagerFactoryClass =

org.jpox.PersistenceManagerFactoryImpl

org.jpox.autoCreateSchema = false

org.jpox.validateTables = false

org.jpox.validateColumns = false

org.jpox.validateConstraints = false

org.jpox.storeManagerType = rdbms

org.jpox.autoCreateSchema = true

org.jpox.autoStartMechanismMode = checked

org.jpox.transactionIsolation = read_committed

javax.jdo.option.DetachAllOnCommit = true

javax.jdo.option.NontransactionalRead = true

javax.jdo.option.ConnectionDriverName = org.apache.derby.jdbc.EmbeddedDriver

javax.jdo.option.ConnectionURL = jdbc:derby://hadoop1:1527/metastore_db;create = true

javax.jdo.option.ConnectionUserName = APP

javax.jdo.option.ConnectionPassword = mine

-> chown -R hadoop /hive

**Metastore schema initialization**
-> schematool -dbType derby -initSchema

*if the following output is obtained it means success else troubleshoot:*

SLF4J: Class path contains multiple SLF4J bindings.

SLF4J: Found binding in [jar:file:/usr/local/apache-hive-2.1.0-bin/lib/log4j-slf4j-impl-2.4.1.jar!/org/slf4j/impl/StaticLoggerBinder.class]

SLF4J: Found binding in [jar:file:/usr/local/hadoop/share/hadoop/common/lib/slf4j-log4j12-1.7.5.jar!/org/slf4j/impl/StaticLoggerBinder.class]

SLF4J: See http://www.slf4j.org/codes.html#multiple_bindings for an explanation.

SLF4J: Actual binding is of type [org.apache.logging.slf4j.Log4jLoggerFactory]

Metastore connection URL:	 jdbc:derby:;databaseName=metastore_db;create=true

Metastore Connection Driver :	 org.apache.derby.jdbc.EmbeddedDriver

Metastore connection User:	 APP

Starting metastore schema initialization to 2.1.0

Initialization script hive-schema-2.1.0.derby.sql

Initialization script completed

schemaTool completed

# Now run hive to test

**if the following error are obtained do that:**

Error #1: 
Exception in thread "main" java.lang.RuntimeException: Couldn't create directory ${system:java.io.tmpdir}/${hive.session.id}_resources

-> edit hive-site.xml: 

go to this property and do the following:

<property>
    <name>hive.downloaded.resources.dir</name>
    <!--
    <value>${system:java.io.tmpdir}/${hive.session.id}_resources</value>
    -->
    <value>/home/hduser/hive/tmp/${hive.session.id}_resources</value>
    <description>Temporary local directory for added resources in the remote file system.</description>
</property>

Error #2: 

java.net.URISyntaxException: Relative path in absolute URI: ${system:java.io.tmpdir%7D/$%7Bsystem:user.name%7D
replace ${system:java.io.tmpdir}/${system:user.name} by /tmp/mydir in hive-site.xml as below:
<property>
    <name>hive.exec.local.scratchdir</name>
    <!--
    <value>${system:java.io.tmpdir}/${system:user.name}</value>
    -->
    <value>/tmp/mydir</value>
    <description>Local scratch space for Hive jobs</description>
</property>
 
**Now finally run the hive and execute queries**
