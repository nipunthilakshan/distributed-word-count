# Distributed Word Count

The main objective of this project is to use Hadoop Streaming using Python.Hadoop Streaming is a feature that comes 
with Hadoop and allows users or developers to use various different languages for writing MapReduce programs like Python, C++, Ruby, etc.
So let's see how to write a Hadoop MapReduce program in Python.

## Prequalities

* Running Hadoop on Linux
* Mapper & Reducer programs
* Sample text files which contains data for testing

## Steps

* mapper.py - Implements the mapper logic. It will read the data from STDIN and will split the lines into words, and 
will generate an output of each word with its individual count.
* Run the following command to check the mapper functionality in normal environment.

```bash
$ echo "foo foo quux labs foo bar quux" | python mapper.py
foo     1
foo     1
quux    1
labs    1
foo     1
bar     1
quux    1
```
* Run the following command to check the reducer functionality with mapper in normal environment.
```bash
$ echo "foo foo quux labs foo bar quux" | python mapper.py | sort -k1,1 | python reducer.py
bar     1
foo     3
labs    1
quux    2
```

```bash
$ cat pg20417.txt | python mapper.py | sort -k1,1 | python reducer.py
hanging 3
hangs   1
happen  3
happened        7
happening       2
happens 4
happens,        1
happens.        2
happens?        1
happily 1
---more
```

Now lets's check how we can do this using Hadoop in a efficient way.
* Upload the input and jobs files to EMR master node(SFTP/WinScp/FileZilla can be used).
* Make a directory in HDFS and add the test data there.
```bash
$ hdfs dfs -mkdir /user/nipun/mapReduce/input
$ hdfs dfs -put 4300-0.txt 5000-8.txt pg20417.txt /user/nipun/mapReduce/input
$ hdfs dfs -ls /user/nipun/mapReduce/input
-rw-r--r--   1 hadoop hdfsadmingroup    1586336 2022-02-04 15:32 /user/nipun/mapReduce/input/4300-0.txt
-rw-r--r--   1 hadoop hdfsadmingroup    1428843 2022-02-04 15:32 /user/nipun/mapReduce/input/5000-8.txt
-rw-r--r--   1 hadoop hdfsadmingroup     674570 2022-02-04 15:13 /user/nipun/mapReduce/input/pg20417.txt
```

* Change the file permissions for jobs files.
```bash
$ chmod 777 mapper.py reducer.py 
```

* Locate the required jar file for streaming.
```bash
$ find /usr/lib/ -name *hadoop*streaming*.jar

/usr/lib/hadoop/hadoop-streaming-3.2.1-amzn-5.jar
/usr/lib/hadoop/hadoop-streaming.jar
/usr/lib/hadoop-mapreduce/hadoop-streaming-3.2.1-amzn-5.jar
/usr/lib/hadoop-mapreduce/hadoop-streaming.jar
```

* The one we???re looking for is /usr/lib/hadoop/hadoop-streaming.jar.
```bash
$ hadoop jar /usr/lib/hadoop/hadoop-streaming.jar -file /home/hadoop/mapReduce/mapper.py 
/home/hadoop/mapReduce/reducer.py -mapper "python mapper.py" -reducer "python reducer.py"  -input /user/nipun/mapReduce/input -output /user/nipun/mapReduce/output
```

* The input and output directories should be located in HDFS and the relevant path should be given.The mapper, 
reducer and streaming jars are available on master node and give the relevant paths accordingly.

![plot](./images/response.PNG)

![plot](./images/response1.PNG)

* The result that we got is available inside the output directory and go can check how the aggregation and 
distribution happened.

## References
1. https://www.geeksforgeeks.org/hadoop-streaming-using-python-word-count-problem
2. https://hugues-talbot.github.io/files/BigData/Big_Data_Tutorial_1.pdf
3. https://www.dcs.bbk.ac.uk/~dell/teaching/cc/lab/cosmin_emr_aws_v5.pdf
