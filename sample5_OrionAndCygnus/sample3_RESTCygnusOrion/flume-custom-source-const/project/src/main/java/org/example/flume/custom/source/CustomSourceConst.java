package org.example.flume.custom.source;

import org.apache.flume.*;
import org.apache.flume.conf.Configurable;
import org.apache.flume.event.SimpleEvent;
import org.apache.flume.source.AbstractSource;
import org.slf4j.LoggerFactory;
import org.slf4j.Logger;
import org.json.JSONObject;
import java.util.Random;

public class CustomSourceConst extends AbstractSource implements Configurable, PollableSource {
    private static final Logger LOGGER = LoggerFactory.getLogger(CustomSourceConst.class);
    private Random random;

    @Override
    public void configure(Context context) {
        // load config
        LOGGER.debug("[CustomSourceConst][configure] start");
        this.random = new Random();
        LOGGER.debug("[CustomSourceConst][configure] end");
    }

    @Override
    public void start() {
        LOGGER.debug("[CustomSourceConst][start] start");
        super.start();
        LOGGER.debug("[CustomSourceConst][start] end");
    }

    @Override
    public void stop() {
        LOGGER.debug("[CustomSourceConst][stop] start");
        super.stop();
        LOGGER.debug("[CustomSourceConst][stop] end");
    }


    // first failure, the wait time is  2 seconds.(0+2)
    // next  failure, the wait time is  4 seconds.(2+2)
    // next  failure, the wait time is  6 seconds.(4+2)
    // next  failure, the wait time is  8 seconds.(6+2)
    // next  failure, the wait time is 10 seconds.(8+2)
    // next  failure, the wait time is 10 seconds.(maximum) ...
    // next  failure, the wait time is 10 seconds.(maximum) ...
    @Override public long getBackOffSleepIncrement() {
        // This method determines the amount of time (milliseconds)
        // to increase the wait time between each retry.
        // In this example, it is set to 2,000 milliseconds (2 seconds).
        return 2000L;
    }
    @Override public long getMaxBackOffSleepInterval() {
        // This method sets the maximum amount of time (in milliseconds) to wait between retries.
        // In this example, it is set to 10,000 milliseconds (10 seconds).
        return 10000L;
    }

    @Override
    public Status process() throws EventDeliveryException {
        LOGGER.debug("[CustomSourceConst][process] start");
        Status status = null;

        try {
            Event event = new SimpleEvent();

            // create event data
            // ex.
            // {
            //     "name": {
            //         "type": "Text",
            //         "value": "This is CustomSourceConst",
            //         "metadata": {}
            //     },
            //     "temperature": {
            //         "type": "Integer",
            //         "value": 42,  // example value
            //         "metadata": {}
            //     },
            //     "humidity": {
            //         "type": "Integer",
            //         "value": 73,  // example value
            //         "metadata": {}
            //     }
            // }

            int temperature = this.random.nextInt(101);
            int humidity    = this.random.nextInt(101);

            JSONObject jsonName = new JSONObject();
            jsonName.put("type", "Text");
            jsonName.put("value", "This is CustomSourceConst");
            jsonName.put("metadata", new JSONObject());

            JSONObject jsonTemperature = new JSONObject();
            jsonTemperature.put("type", "Integer");
            jsonTemperature.put("value", temperature);
            jsonTemperature.put("metadata", new JSONObject());

            JSONObject jsonHumidity = new JSONObject();
            jsonHumidity.put("type", "Integer");
            jsonHumidity.put("value", humidity);
            jsonHumidity.put("metadata", new JSONObject());

            JSONObject json = new JSONObject();
            json.put("name",        jsonName);
            json.put("temperature", jsonTemperature);
            json.put("humidity",    jsonHumidity);

            // set data to event
            event.setBody(json.toString().getBytes());

            // send event
            getChannelProcessor().processEvent(event);

            status = Status.READY;
        } catch (ChannelFullException e) {
            LOGGER.error("[CustomSourceConst][process] end. Channel is full, backing off", e);
            status = Status.BACKOFF;
        } catch (Throwable t) {
            LOGGER.error("[CustomSourceConst][process] end. Error processing event", t);
            status = Status.BACKOFF;
        }
        LOGGER.debug("[CustomSourceConst][process] end");
        return status;
    }
}
