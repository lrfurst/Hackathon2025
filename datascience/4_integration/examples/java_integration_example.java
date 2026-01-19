// Minimal, compilable Java example for integrating with the Python Flight Prediction API
// Scope: client-side integration only (no business logic, no invented fields)

package com.example.flight.integration;

import org.springframework.http.*;
import org.springframework.web.client.*;
import org.springframework.http.client.SimpleClientHttpRequestFactory;

import java.util.Collections;

// -----------------------------------------------------------------------------
// DTOs — aligned strictly with API contract
// -----------------------------------------------------------------------------

class FlightData {
    public String companhia_aerea;
    public String aeroporto_origem;
    public String aeroporto_destino;
    public String data_hora_partida;
    public Double distancia_km;
}

class PredictionResponse {
    public boolean atraso;
    public double probabilidade;
}

// -----------------------------------------------------------------------------
// Minimal API Client
// -----------------------------------------------------------------------------

public class FlightPredictionClient {

    private final RestTemplate restTemplate;
    private final String apiUrl;

    public FlightPredictionClient(String apiUrl) {
        SimpleClientHttpRequestFactory factory = new SimpleClientHttpRequestFactory();
        factory.setConnectTimeout(3000);
        factory.setReadTimeout(3000);
        this.restTemplate = new RestTemplate(factory);
        this.apiUrl = apiUrl;
    }

    public PredictionResponse predict(FlightData flight) {
        String url = apiUrl + "/predict";

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        headers.setAccept(Collections.singletonList(MediaType.APPLICATION_JSON));

        HttpEntity<FlightData> request = new HttpEntity<>(flight, headers);

        try {
            ResponseEntity<PredictionResponse> response = restTemplate.exchange(
                url,
                HttpMethod.POST,
                request,
                PredictionResponse.class
            );

            if (response.getStatusCode() == HttpStatus.OK && response.getBody() != null) {
                return response.getBody();
            }

            throw new RuntimeException("Unexpected response from API: " + response.getStatusCode());

        } catch (HttpClientErrorException e) {
            // 4xx — payload or contract error (do not retry)
            throw new RuntimeException("Client error calling API: " + e.getStatusCode(), e);

        } catch (HttpServerErrorException e) {
            // 5xx — server error (retry or fallback allowed)
            throw new RuntimeException("Server error from API: " + e.getStatusCode(), e);

        } catch (ResourceAccessException e) {
            // timeout / connection refused
            throw new RuntimeException("API unavailable or timeout", e);
        }
    }

    // -------------------------------------------------------------------------
    // Quick manual test (no Spring context required)
    // -------------------------------------------------------------------------

    public static void main(String[] args) {
        FlightPredictionClient client = new FlightPredictionClient("http://localhost:8000");

        FlightData flight = new FlightData();
        flight.companhia_aerea = "AA";
        flight.aeroporto_origem = "JFK";
        flight.aeroporto_destino = "LAX";
        flight.data_hora_partida = "2024-01-15T14:30:00";
        flight.distancia_km = 3980.0;

        try {
            PredictionResponse result = client.predict(flight);
            System.out.println("Atraso: " + result.atraso);
            System.out.println("Probabilidade: " + result.probabilidade);
        } catch (Exception e) {
            System.err.println("Erro ao chamar API: " + e.getMessage());
        }
    }
}
