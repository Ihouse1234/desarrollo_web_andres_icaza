package com.dcc.comunired.controller;

import com.dcc.comunired.service.NotaService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/api")
public class NotaController {

    private final NotaService notaService;

    public NotaController(NotaService notaService) {
        this.notaService = notaService;
    }

    @PostMapping("/actividades/{id}/notas")
    public ResponseEntity<?> agregarNota(@PathVariable("id") Integer actividadId,
                                         @RequestBody Map<String, Integer> body) {
        try {
            Integer valorNota = body.get("nota");
            // El service valida que la nota esta entre 1 y 7, recalcula el promedio.
            Double nuevoPromedio = notaService.agregarNota(actividadId, valorNota);

            // Respuesta exitosa con el promedio con 1 decimal.
            return ResponseEntity.ok(Map.of(
                "ok", true,
                "promedio", String.format("%.1f", nuevoPromedio)
            ));
        } catch (IllegalArgumentException e) {
            // Si la validación falla, responde error
            return ResponseEntity.badRequest().body(Map.of(
                "ok", false,
                "error", e.getMessage()
            ));
        }
    }
}