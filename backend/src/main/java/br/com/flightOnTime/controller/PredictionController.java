package br.com.flightOnTime.controller;

import br.com.flightOnTime.dto.PredictionRequestDTO;
import br.com.flightOnTime.dto.PredictionResponseDTO;
import br.com.flightOnTime.dto.StatusResponseDTO;
import br.com.flightOnTime.service.PredictionService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@CrossOrigin(origins = "*")
public class PredictionController {
    private final PredictionService predictionService;
    public PredictionController(PredictionService predictionService) {
        this.predictionService = predictionService;
    }

    @PostMapping("/predict")
    @ResponseStatus(HttpStatus.OK)
    @Operation(summary = "endpoint responsável pela previsão de vôo, histórico de atrasos e cadastro das consultas.")
    @ApiResponse(responseCode = "200", description = " success", content = {
            @Content(mediaType = "application.json", schema = @Schema(implementation = ResponseEntity.class))
    })
    public ResponseEntity<PredictionResponseDTO> predict(@Valid @RequestBody PredictionRequestDTO request) {
        PredictionResponseDTO response = predictionService.getPrediction(request);

        return ResponseEntity.ok(response);

    }
    @GetMapping("/stats")
    public StatusResponseDTO showStatus() {
        return predictionService.getStatus();
    }

}

