package com.dcc.comunired.service;

import com.dcc.comunired.entity.Actividad;
import com.dcc.comunired.repository.ActividadRepository;
import org.springframework.stereotype.Service;

import java.util.List;

//Buscador actividades
@Service
public class BusquedaService {

    private final ActividadRepository actividadRepository;

    public BusquedaService(ActividadRepository actividadRepository) {
        this.actividadRepository = actividadRepository;
    }

    /**
     * Si el patrón tiene menos de 3 caracteres o no existe, devuelve lista vacía
     */
    public List<Actividad> buscar(String patron) {
        if (patron == null || patron.trim().length() < 3) {
            return List.of();   // lista vacía inmutable
        }
        return actividadRepository.buscar(patron.trim());
    }
}