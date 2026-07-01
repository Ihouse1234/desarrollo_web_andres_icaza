package com.dcc.comunired.service;

import com.dcc.comunired.entity.Actividad;
import com.dcc.comunired.entity.Nota;
import com.dcc.comunired.repository.ActividadRepository;
import com.dcc.comunired.repository.NotaRepository;
import org.springframework.stereotype.Service;

import java.util.Optional;

@Service
public class NotaService {

    private final NotaRepository notaRepository;
    private final ActividadRepository actividadRepository;

    public NotaService(NotaRepository notaRepository,
                       ActividadRepository actividadRepository) {
        this.notaRepository = notaRepository;
        this.actividadRepository = actividadRepository;
    }

    public Double agregarNota(Integer actividadId, Integer valorNota) {
        // Validación 1: la nota debe estar entre 1 y 7 inclusive
        if (valorNota == null || valorNota < 1 || valorNota > 7) {
            throw new IllegalArgumentException("La nota debe ser un entero entre 1 y 7.");
        }

        // Validación 2: la actividad debe existir
        Optional<Actividad> actividadOpt = actividadRepository.findById(actividadId);
        if (actividadOpt.isEmpty()) {
            throw new IllegalArgumentException("La actividad no existe.");
        }

        Nota nota = new Nota();
        nota.setActividad(actividadOpt.get());
        nota.setNota(valorNota);
        notaRepository.save(nota);

        // Recalcular y devolver el promedio.
        return obtenerPromedio(actividadId);
    }

    
    // Devuelve el promedio de notas de una actividad, retorna null si la actividad aún no tiene notas.
    public Double obtenerPromedio(Integer actividadId) {
        return notaRepository.calcularPromedio(actividadId);
    }
}