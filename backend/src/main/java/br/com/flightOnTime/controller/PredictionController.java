package br.com.flightOnTime.controller;

import br.com.flightOnTime.dto.PredictionRequestDTO;
import br.com.flightOnTime.dto.PredictionResponseDTO;
import br.com.flightOnTime.service.PredictionService;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/predict") //Caminho base do controller
public class PredictionController {

    //Declarar uma dependência  do service
    private final PredictionService predictionService;

    //Injeção de dependência por construtor
    public PredictionController(PredictionService predictionService) {
        this.predictionService = predictionService;
    }

    @PostMapping
    public ResponseEntity<PredictionResponseDTO> predict(@Valid @RequestBody PredictionRequestDTO request) {
        // Solicita ao service a previsão do status do voo com base nos dados informados
        PredictionResponseDTO response = predictionService.getPrediction(request);

        // Retorna a resposta com o status HTTP 200 (OK)
        return ResponseEntity.ok(response);

    }
}

