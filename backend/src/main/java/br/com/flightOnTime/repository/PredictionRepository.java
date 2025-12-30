package br.com.flightOnTime.repository;

import br.com.flightOnTime.entity.PredictionEntity;
import org.springframework.data.jpa.repository.JpaRepository;

public interface PredictionRepository extends JpaRepository<PredictionEntity,Long> {
}
