student = LOAD 'hdfs://192.168.43.242:9001/pig_data' USING PigStorage(',') AS (id:int, name:chararray, city:chararray);
dump student;
