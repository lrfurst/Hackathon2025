package br.com.flightOnTime.controller;

import br.com.flightOnTime.dto.PredictionRequestDTO;
import br.com.flightOnTime.dto.PredictionResponseDTO;
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
@RequestMapping("/predict") //Caminho base do controller
@CrossOrigin(origins = "*")
public class PredictionController {
    //Declarar uma dependência  do service
    private final PredictionService predictionService;
    //Injeção de dependência por construtor
    public PredictionController(PredictionService predictionService) {
        this.predictionService = predictionService;
    }

    @PostMapping
    @ResponseStatus(HttpStatus.OK)
    @Operation(summary = "endpoint responsável pela previsão de vôo, histórico de atrasos e cadastro das consultas.")
    @ApiResponse(responseCode = "200", description = " success", content = {
            @Content(mediaType = "application.json", schema = @Schema(implementation = ResponseEntity.class))
    })
    public ResponseEntity<PredictionResponseDTO> predict(@Valid @RequestBody PredictionRequestDTO request) {
        // Solicita ao service a previsão do status do voo com base nos dados informados
        PredictionResponseDTO response = predictionService.getPrediction(request);

        // Retorna a resposta com o status HTTP 200 (OK)
        return ResponseEntity.ok(response);

    }
}

