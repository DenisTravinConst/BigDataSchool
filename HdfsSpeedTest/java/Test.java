import java.io.IOException;
import java.util.HashMap;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

/**
 * Speed test java class
 */
public class Test {

    /**
     * Main java class
     */
    public static void main(String [] args) throws Exception
    {
        Configuration conf = new Configuration();
        Job job = Job.getInstance(conf, "SpeedTest");
        job.setJarByClass(Test.class);
        job.setMapperClass(Map.class);
        job.setCombinerClass(Reduce.class);
        job.setReducerClass(Reduce.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(IntWritable.class);
        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));
        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }

    /**
     * Set category to dictionary method
     * @param dictionary Categories dictionary
     * @param category Category to set
     * @return Input dictionary with new category added
     */
    public static HashMap<String, Integer> setCategory(HashMap<String, Integer> dictionary, String category){
        if (dictionary.keySet().contains(category)){
            dictionary.put(category, dictionary.get(category) + 1);
        } else {
            dictionary.put(category, 1);
        }
        return dictionary;
    }

    /**
     * Mapper class
     */
    public static class Map extends Mapper<Object, Text, Text, IntWritable>{
        public void map(Object key, Text value, Context con) throws IOException, InterruptedException
        {
            HashMap<String, Integer> dictionary = new HashMap<String, Integer>();
            String[] lines = value.toString().split("\n");
            try {
                for (String line : lines) {
                    String[] lineArray = line.trim().split("\t");
                    String statusCode = lineArray[5].trim();
                    if (!"response".equals(statusCode)) {
                        if (statusCode.toCharArray()[0] == '2' || statusCode.toCharArray()[0] == '3') {
                            String[] urlRootArray = line.trim().split("\t")[4].trim().split("/");
                            String urlRoot = String.format("%s/%s", urlRootArray[0], urlRootArray[1]);
                            dictionary = setCategory(dictionary, urlRoot);
                        } else {
                            dictionary = setCategory(dictionary, String.format("error-%sXX", statusCode.toCharArray()[0]));
                        }
                    }
                }
            } catch (Exception e){
                dictionary = setCategory(dictionary, "error");
            }


            for(String category : dictionary.keySet()){
                Text outputKey = new Text(category.toUpperCase().trim());
                IntWritable outputValue = new IntWritable(dictionary.get(category));
                con.write(outputKey, outputValue);
            }
        }
    }

    /**
     * Reducer class
     */
    public static class Reduce extends Reducer<Text, IntWritable, Text, IntWritable>
    {
        public void reduce(Text word, Iterable<IntWritable> values, Context con) throws IOException, InterruptedException
        {
            int sum = 0;
            for(IntWritable value : values)
            {
                sum += value.get();
            }
            con.write(word, new IntWritable(sum));
        }
    }
}