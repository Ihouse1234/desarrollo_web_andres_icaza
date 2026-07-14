package com.dcc.comunired.service;

import com.dcc.comunired.entity.Log;
import com.dcc.comunired.repository.LogRepository;
import org.springframework.stereotype.Service;

import java.util.List;

// Lógica de negocio de los mensajes de log.
@Service
public class LogService {

    private final LogRepository logRepository;

    public LogService(LogRepository logRepository) {
        this.logRepository = logRepository;
    }

    // Devuelve todos los logs de la fecha más reciente a la más antigua.
    public List<Log> listarTodos() {
        return logRepository.findAllByOrderByFechaDesc();
    }
}