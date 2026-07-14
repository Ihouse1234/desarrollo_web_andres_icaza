package com.dcc.comunired.repository;

import com.dcc.comunired.entity.Log;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;


public interface LogRepository extends JpaRepository<Log, Long> {
    // Trae todos los logs de la fecha más reciente a la más antigua
    List<Log> findAllByOrderByFechaDesc();
}