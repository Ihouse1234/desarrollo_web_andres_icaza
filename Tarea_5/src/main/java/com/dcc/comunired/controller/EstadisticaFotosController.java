package com.dcc.comunired.controller;

import com.dcc.comunired.service.FotoService;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ResponseBody;

import java.util.Map;

@Controller
public class EstadisticaFotosController {

    private final FotoService fotoService;

    public EstadisticaFotosController(FotoService fotoService) {
        this.fotoService = fotoService;
    }

    // Muestra la pagina con el gráfico.
    @GetMapping("/estadistica-fotos")
    public String estadisticaFotos() {
        return "estadistica-fotos";   // renderiza templates/estadistica-fotos.html
    }

    /**
     * Devuelve los conteos en JSON para alimentar el gráfico:
     *   { "vigentes": 12, "eliminadas": 3 }
     */
    @GetMapping("/api/estadistica-fotos")
    @ResponseBody
    public Map<String, Long> datosEstadistica() {
        return Map.of(
            "vigentes",   fotoService.contarVigentes(),
            "eliminadas", fotoService.contarEliminadas()
        );
    }
}