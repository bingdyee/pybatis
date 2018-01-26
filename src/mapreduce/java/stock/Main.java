package stock;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

import java.io.IOException;
import stock.TradeDetailMapper;
import stock.TradeDetailReduce;

public class Main {

    public void runJob() throws IOException, ClassNotFoundException, InterruptedException {
        Configuration conf = new Configuration();

        conf.set("fs.defaultFS", "hdfs://localhost:9000/");
        conf.set("mapreduce.job.jar", "stock-share.jar");
        conf.set("mapreduce.framework.name", "yarn");
        conf.set("yarn.resourcemanager.hostname", "localhost");

        Job job = Job.getInstance(conf);

        job.setMapperClass(TradeDetailMapper.class);
        job.setReducerClass(TradeDetailReduce.class);

        FileInputFormat.setInputPaths(job, "/stock_input/");
        FileOutputFormat.setOutputPath(job, new Path("/stock_output/"));

        job.waitForCompletion(true);
    }

    public static void main(String [] args) throws IOException, ClassNotFoundException, InterruptedException {

        System.out.println("Hello StockShare...");

    }

}
