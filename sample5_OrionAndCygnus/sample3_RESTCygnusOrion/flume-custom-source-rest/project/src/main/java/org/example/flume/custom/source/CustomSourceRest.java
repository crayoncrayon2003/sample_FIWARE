package org.example.flume.custom.source;

import org.apache.flume.*;
import org.apache.flume.conf.Configurable;
import org.apache.flume.event.SimpleEvent;
import org.apache.flume.source.AbstractSource;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.util.EntityUtils;

import org.slf4j.LoggerFactory;
import org.slf4j.Logger;

import org.json.JSONObject;
import java.io.IOException;

public class CustomSourceRest extends AbstractSource implements Configurable, PollableSource {
    private static final Logger LOGGER = LoggerFactory.getLogger(CustomSourceRest.class);
    private String URL;

    @Override
    public void configure(Context context) {
        // Load configuration
        LOGGER.debug("[CustomSourceRest][configure] start");
        URL = context.getString("url", "http://localhost:8080");
        LOGGER.debug("[CustomSourceRest][configure] end");
    }

    @Override
    public void start() {
        LOGGER.debug("[CustomSourceRest][start] start");
        super.start();
        LOGGER.debug("[CustomSourceRest][start] end");
    }

    @Override
    public void stop() {
        LOGGER.debug("[CustomSourceRest][stop] start");
        super.stop();
        LOGGER.debug("[CustomSourceRest][stop] end");
    }

    @Override
    public long getBackOffSleepIncrement() {
        return 2000L;
    }

    @Override
    public long getMaxBackOffSleepInterval() {
        return 10000L;
    }

    @Override
    public Status process() throws EventDeliveryException {
        LOGGER.debug("[CustomSourceRest][process] start");
        Status status = null;

        try {
            // get data for Webserver
            String response = getWebServerData();
            // Parse the response
            JSONObject jsonResponse = new JSONObject(response);
            int temperature = jsonResponse.getInt("temperature");
            int humidity = jsonResponse.getInt("humidity");

            // create event data
            JSONObject jsonName = new JSONObject();
            jsonName.put("type", "Text");
            jsonName.put("value", "This is CustomSourceRest");
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
            Event event = new SimpleEvent();
            event.setBody(json.toString().getBytes());

            // send event
            getChannelProcessor().processEvent(event);

            Thread.sleep(5000L);

            status = Status.READY;
        } catch (ChannelFullException e) {
            LOGGER.error("[CustomSourceRest][process] end. Channel is full, backing off", e);
            status = Status.BACKOFF;
        } catch (Throwable t) {
            LOGGER.error("[CustomSourceRest][process] end. Error processing event", t);
            status = Status.BACKOFF;
        }
        LOGGER.debug("[CustomSourceRest][process] end");
        return status;
    }

    private String getWebServerData() throws IOException {
        try (CloseableHttpClient httpClient = HttpClients.createDefault()) {
            HttpGet request = new HttpGet(URL);
            try (CloseableHttpResponse response = httpClient.execute(request)) {
                int statusCode = response.getStatusLine().getStatusCode();
                if (statusCode == 200) { // Success
                    return EntityUtils.toString(response.getEntity());
                } else {
                    throw new IOException("Failed to fetch data from API, Response code: " + statusCode);
                }
            }
        }
    }

}
