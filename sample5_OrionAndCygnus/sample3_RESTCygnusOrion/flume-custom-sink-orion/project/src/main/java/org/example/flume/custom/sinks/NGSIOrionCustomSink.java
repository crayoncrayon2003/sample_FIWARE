package org.example.flume.custom.sinks;

import org.apache.flume.Context;
import org.apache.flume.Event;
import org.apache.flume.EventDeliveryException;
import org.apache.flume.conf.Configurable;
import org.apache.flume.sink.AbstractSink;
import org.apache.flume.Transaction;
import org.apache.flume.Channel;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import org.json.JSONObject;
import java.io.IOException;

public class NGSIOrionCustomSink extends AbstractSink implements Configurable {
    private static final Logger LOGGER = LoggerFactory.getLogger(NGSIOrionCustomSink.class);
    private String orionHost;
    private String orionPort;
    private String orionFiware;
    private String orionFiwarePath;
    private String orionId;
    private String orionType;
    private String orionBackend;

    @Override
    public void configure(Context context) {
        // load config
        LOGGER.debug("[NGSIOrionCustomSink][configure] start");
        orionHost = context.getString("orion_host", "");
        orionPort = context.getString("orion_port", "1026");
        orionFiware = context.getString("orion_fiware", "");
        orionFiwarePath = context.getString("orion_fiware_path", "/");
        orionId = context.getString("orion_id", "");
        orionType = context.getString("orion_type", "");
        LOGGER.debug("[NGSIOrionCustomSink][configure] end");
    }

    @Override
    public void start() {
        LOGGER.debug("[NGSIOrionCustomSink][start] start");
        try {
            orionBackend = String.format("http://%s:%s", orionHost, orionPort);
            LOGGER.debug("[" + this.getName() + "] Orion persistence backend created");
        } catch (Exception e) {
            LOGGER.error("Error while creating the Orion persistence backend. Details=" + e.getLocalizedMessage());
        }

        super.start();
        LOGGER.debug("[NGSIOrionCustomSink][start] end");
    }

    @Override
    public void stop() {
        LOGGER.debug("[NGSIOrionCustomSink][stop] start");
        super.stop();
        LOGGER.debug("[NGSIOrionCustomSink][stop] end");
    }

    @Override
    public Status process() throws EventDeliveryException {
        LOGGER.debug("[NGSIOrionCustomSink][process] start");

        Channel ch = getChannel();
        Transaction txn = ch.getTransaction();
        txn.begin();

        try{
            // receive event
            Event event = getChannel().take();

            if (event == null) {
                txn.commit();
                LOGGER.error("[NGSIOrionCustomSink][process] event == null");
                return Status.BACKOFF;
            }

            // get data
            String msg = new String(event.getBody());
            LOGGER.debug("get msg: {}", msg);

            try (CloseableHttpClient httpClient = HttpClients.createDefault()) {
                LOGGER.debug("[NGSIOrionCustomSink][process] create HttpClient");

                // Create the NGSI update request
                JSONObject updateRequest = new JSONObject();
                updateRequest.put("actionType", "append");

                JSONObject entity = new JSONObject();
                entity.put("id", orionId);
                entity.put("type", orionType);

                JSONObject attributes = new JSONObject(msg);
                for (String key : attributes.keySet()) {
                    entity.put(key, attributes.getJSONObject(key));
                }
                updateRequest.put("entities", new org.json.JSONArray().put(entity));

                // update request of NGSI v2
                HttpPost request = new HttpPost(orionBackend + "/v2/op/update");
                request.setHeader("Content-Type", "application/json");
                request.setHeader("Fiware-Service", orionFiware);
                request.setHeader("Fiware-ServicePath", orionFiwarePath);
                request.setEntity(new StringEntity(updateRequest.toString()));

                try (CloseableHttpResponse response = httpClient.execute(request)) {
                    int statusCode = response.getStatusLine().getStatusCode();
                    if (statusCode == 200 || statusCode == 201 || statusCode == 204) {
                        LOGGER.info("Successfully sent event to API. Status code: {}", statusCode);
                        txn.commit();
                        return Status.READY;
                    } else {
                        LOGGER.error("Failed to send event to API. Status code: {}", statusCode);
                        txn.rollback();
                        return Status.BACKOFF;
                    }
                }
            } catch (IOException e) {
                LOGGER.error("[NGSIOrionCustomSink][process] error IOException", e);
                txn.rollback();
                return Status.BACKOFF;
            }

        } catch (Throwable t) {
            txn.rollback();
            throw new EventDeliveryException("[NGSIOrionCustomSink][process] error Throwable", t);
        }finally{
            txn.close();
        }
    }
}
