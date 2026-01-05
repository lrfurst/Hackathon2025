package br.com.flightOnTime.config;

import lombok.extern.slf4j.Slf4j;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.health.contributor.Health;
import org.springframework.boot.health.contributor.HealthIndicator;

import org.springframework.stereotype.Component;
import java.net.HttpURLConnection;

import java.net.URL;

import java.time.LocalDateTime;


@Slf4j
@Component("pythonApiHealth")
public class PythonApiHealthIndicator implements HealthIndicator {

  //  private static final String FLASK_URL = "http://localhost:5000";
  @Value("${API_PYTHON_URL:http://app-python:5000}")
  private String flaskUrl;



    @Override
    public Health health() {
        log.debug("Testando Flask em: {}", flaskUrl);

        try {
            URL url = new URL(flaskUrl);
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("GET");
            conn.setConnectTimeout(2000);
            conn.setReadTimeout(2000);

            int code = conn.getResponseCode();
            conn.disconnect();

            log.debug("Flask respondeu com HTTP {}", code);

            // QUALQUER resposta HTTP (inclusive 404) = Flask ONLINE
            return Health.up()
                    .withDetail("status", "Flask ONLINE")
                    .withDetail("url", flaskUrl)
                    .withDetail("httpCode", code)
                    .withDetail("timestamp", LocalDateTime.now())
                    .withDetail("note", code == 404 ?
                            "Endpoint raiz não existe - normal" :
                            "Respondendo normalmente")
                    .build();

        } catch (java.net.ConnectException e) {
            // Conexão recusada = Flask OFFLINE
            log.warn("Flask OFFLINE: Conexão recusada");
            return Health.down()
                    .withDetail("status", "Flask OFFLINE")
                    .withDetail("url", flaskUrl)
                    .withDetail("error", "Conexão recusada - Flask não está rodando")
                    .withDetail("timestamp", LocalDateTime.now())
                    .build();

        } catch (java.net.SocketTimeoutException e) {
            // Timeout = Flask OFFLINE
            log.warn("Flask OFFLINE: Timeout");
            return Health.down()
                    .withDetail("status", "Flask OFFLINE")
                    .withDetail("url", flaskUrl)
                    .withDetail("error", "Timeout - Flask não respondeu em 2 segundos")
                    .withDetail("timestamp", LocalDateTime.now())
                    .build();

        } catch (Exception e) {
            // Outros erros
            return Health.down()
                    .withDetail("status", "Flask OFFLINE")
                    .withDetail("url", flaskUrl)
                    .withDetail("error", e.getMessage())
                    .withDetail("timestamp", LocalDateTime.now())
                    .build();
        }
    }

}