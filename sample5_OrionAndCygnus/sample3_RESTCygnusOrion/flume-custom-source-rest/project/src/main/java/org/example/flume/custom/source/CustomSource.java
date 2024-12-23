package org.example.flume.custom.source;

import org.apache.flume.*;
import org.apache.flume.Context;
import org.apache.flume.Event;
import org.apache.flume.event.EventBuilder;
import org.apache.flume.source.AbstractSource;
import org.apache.flume.conf.Configurable;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

public class CustomSource extends AbstractSource implements Configurable {
    private static final Logger LOG = LoggerFactory.getLogger(CustomSource.class);
    private String apiUrl;
    private long pollingInterval;
    private volatile boolean running;

    public static final String INPUT_HOST = "input.host";
    public static final String INPUT_PORT = "input.port";
    public static final String INPUT_INTERVAL = "input.interval";

    @Override
    public void configure(Context context) {
        LOG.debug("[CustomSource][configure] start");
        String HOST = context.getString(INPUT_HOST, "localhost");
        String PORT = context.getString(INPUT_PORT, "8080");
        apiUrl = String.format("http://%s:%s", HOST, PORT);
        pollingInterval = context.getLong(INPUT_INTERVAL, 10000L); // Default to 10 seconds
        LOG.debug("[CustomSource][configure] end");
    }

    @Override
    public synchronized void start() {
        LOG.debug("[CustomSource][start] start");
        running = true;
        LOG.debug("CustomSource started with API URL: {} and polling interval: {} ms", apiUrl, pollingInterval);
        new Thread(() -> {
            while (running) {
                try {
                    pollApi();
                    Thread.sleep(pollingInterval);
                } catch (InterruptedException e) {
                    LOG.error("Interrupted while sleeping", e);
                    running = false;
                } catch (IOException e) {
                    LOG.error("Error polling API", e);
                }
            }
        }).start();
        super.start();
        LOG.debug("[CustomSource][start] end");
    }

    @Override
    public synchronized void stop() {
        LOG.debug("[CustomSource][stop] start");
        running = false;
        LOG.debug("CustomSource stopped");
        super.stop();
        LOG.debug("[CustomSource][stop] end");
    }

    private void pollApi() throws IOException {
        LOG.debug("[CustomSource][pollApi] start");
        URL url = new URL(apiUrl);
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setRequestMethod("GET");
        int responseCode = conn.getResponseCode();

        if (responseCode == 200) {
            try (BufferedReader in = new BufferedReader(new InputStreamReader(conn.getInputStream()))) {
                String inputLine;
                StringBuilder content = new StringBuilder();
                while ((inputLine = in.readLine()) != null) {
                    content.append(inputLine);
                }
                // Log the retrieved data
                LOG.info("Data retrieved from API: {}", content.toString());
                // Create a Flume event with the data
                Event event = EventBuilder.withBody(content.toString().getBytes());
                getChannelProcessor().processEvent(event);
            }
        } else {
            LOG.error("Failed to poll API: HTTP response code {}", responseCode);
        }
        LOG.debug("[CustomSource][pollApi] end");
    }
}
