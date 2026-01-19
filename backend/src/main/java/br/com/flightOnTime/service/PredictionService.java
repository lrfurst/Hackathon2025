package br.com.flightOnTime.service;

import br.com.flightOnTime.dto.PredictionRequestDTO;
import br.com.flightOnTime.dto.PredictionResponseDTO;
import br.com.flightOnTime.infra.exception.PredictionNotFound;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpStatusCode;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;

@Service
public class PredictionService {

    private final WebClient webClient;

    @Value("${ml.api.base-url}")
    private String baseUrl;


    public PredictionService(WebClient.Builder builder) {
        this.webClient = builder.build();
    }


    public PredictionResponseDTO getPrediction(PredictionRequestDTO request) {

        return webClient.post()
                .uri(baseUrl)
                .bodyValue(request)
                .retrieve()
                .onStatus(
                        HttpStatusCode::isError,
                        response -> Mono.error(
                                new PredictionNotFound(
                                        "Erro ao chamar o serviço de previsão Python. Status: "
                                                + response.statusCode().value()
                                )
                        )
                )
                .bodyToMono(PredictionResponseDTO.class)
                .block(); // OK para MVP
    }
}
