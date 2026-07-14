package com.dcc.comunired.controller;

import com.dcc.comunired.dto.FotoDTO;
import com.dcc.comunired.entity.Foto;
import com.dcc.comunired.service.FotoService;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

@Controller
public class AdminFotosController {

    private final FotoService fotoService;

    // Formatea la fecha del miembro a algo legible
    private static final DateTimeFormatter FMT =
        DateTimeFormatter.ofPattern("dd/MM/yyyy HH:mm");

    public AdminFotosController(FotoService fotoService) {
        this.fotoService = fotoService;
    }

    /**
     * GET /admin-fotos
     * Muestra la galería con las fotos ordenadas de más reciente a más antigua.
     * Model es el equivalente a pasar variables en render_template() de Flask.
     */
    @GetMapping("/admin-fotos")
    public String adminFotos(Model model) {
        List<Foto> fotos = fotoService.listarParaAdmin();

        // Convertir cada entidad a DTO (aplanando los datos de las relaciones)
        List<FotoDTO> dtos = new ArrayList<>();
        for (Foto f : fotos) {
            dtos.add(new FotoDTO(
                f.getId(),
                f.getNombreArchivo(),
                f.getActividad().getMiembro().getFechaRegistro().format(FMT),
                f.getActividad().getMiembro().getComuna().getNombre(),
                f.getActividad().getMiembro().getEmail(),
                f.getEliminada()
            ));
        }

        model.addAttribute("fotos", dtos);
        return "admin-fotos";   // renderiza templates/admin-fotos.html
    }

    /**
     * Recibe el motivo en el cuerpo JSON: { "motivo": "texto..." }
     * Marca la foto como eliminada y registra la acción en el log.
     */
    @PostMapping("/api/fotos/{id}/eliminar")
    @ResponseBody
    public ResponseEntity<?> eliminarFoto(@PathVariable("id") Integer fotoId,
                                          @RequestBody Map<String, String> body) {
        try {
            String motivo = body.get("motivo");
            // El service valida el motivo y hace la operación transaccional
            fotoService.eliminarFoto(fotoId, motivo);
            return ResponseEntity.ok(Map.of("ok", true));
        } catch (IllegalArgumentException e) {
            return ResponseEntity.badRequest().body(Map.of(
                "ok", false,
                "error", e.getMessage()
            ));
        }
    }
}