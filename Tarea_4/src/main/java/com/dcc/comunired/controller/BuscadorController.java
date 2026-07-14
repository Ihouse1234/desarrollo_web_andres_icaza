package com.dcc.comunired.controller;

import com.dcc.comunired.dto.ActividadDTO;
import com.dcc.comunired.entity.Actividad;
import com.dcc.comunired.service.BusquedaService;
import com.dcc.comunired.service.NotaService;
import org.springframework.web.bind.annotation.*;

import java.util.ArrayList;
import java.util.List;

@RestController
@RequestMapping("/api")   // todas las rutas de esta clase empiezan con /api
public class BuscadorController {

    private final BusquedaService busquedaService;
    private final NotaService notaService;

    public BuscadorController(BusquedaService busquedaService, NotaService notaService) {
        this.busquedaService = busquedaService;
        this.notaService = notaService;
    }

    @GetMapping("/buscar")
    public List<ActividadDTO> buscar(@RequestParam("q") String q) {
        List<Actividad> actividades = busquedaService.buscar(q);

        // Convertir cada entidad a su DTO.
        List<ActividadDTO> resultado = new ArrayList<>();
        for (Actividad a : actividades) {
            // Calcular el promedio; si es null, mostrar "-"
            Double promedio = notaService.obtenerPromedio(a.getId());
            String notaStr = (promedio == null) ? "-" : String.format("%.1f", promedio);

            resultado.add(new ActividadDTO(
                a.getId(),
                a.getMiembro().getNombre(),
                a.getDia(),
                a.getTipo(),
                a.getMiembro().getComuna().getNombre(),
                a.getNombre(),
                a.getDescripcion(),
                notaStr
            ));
        }
        return resultado;
    }
}