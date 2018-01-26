package stock;


import org.apache.hadoop.mapreduce.Reducer;

import java.io.IOException;

public class TradeDetailReduce extends Reducer{

    @Override
    protected void reduce(Object key, Iterable values, Context context) throws IOException, InterruptedException {
        super.reduce(key, values, context);
    }

}
