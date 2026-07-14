package com.dcc.comunired.service;

import com.dcc.comunired.entity.Foto;
import com.dcc.comunired.entity.Log;
import com.dcc.comunired.repository.FotoRepository;
import com.dcc.comunired.repository.LogRepository;
import jakarta.transaction.Transactional;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

// Lógica de negocio de las fotos.
@Service
public class FotoService {

    private final FotoRepository fotoRepository;
    private final LogRepository logRepository;

    public FotoService(FotoRepository fotoRepository, LogRepository logRepository) {
        this.fotoRepository = fotoRepository;
        this.logRepository = logRepository;
    }

    //Devuelve las fotos para la galería, de la más reciente a la más antigua.     
    public List<Foto> listarParaAdmin() {
        return fotoRepository.listarParaAdmin();
    }

    /**
     * Marca una foto como eliminada (borrado lógico) y registra la acción en el log.
     * Las dos operaciones deben ocurrir juntas. Si una falla, se revierte
     * todo y no queda la foto marcada sin su registro correspondiente.
     */
    @Transactional
    public void eliminarFoto(Integer fotoId, String motivo) {
        // ── Validación del motivo (obligatorio, entre 5 y 200 caracteres) ──
        if (motivo == null || motivo.trim().isEmpty()) {
            throw new IllegalArgumentException("El motivo es obligatorio.");
        }
        String motivoLimpio = motivo.trim();
        if (motivoLimpio.length() < 5 || motivoLimpio.length() > 200) {
            throw new IllegalArgumentException(
                "El motivo debe tener entre 5 y 200 caracteres.");
        }

        // Verificar que la foto existe ──
        Optional<Foto> fotoOpt = fotoRepository.findById(fotoId);
        if (fotoOpt.isEmpty()) {
            throw new IllegalArgumentException("La foto no existe.");
        }

        Foto foto = fotoOpt.get();

        // Marcar la foto como eliminada (columna eliminada = 1)
        foto.setEliminada(true);
        fotoRepository.save(foto);

        // Registrar la acción en la tabla log ──
        String mensaje = "eliminado foto " + fotoId
                       + " por usuario admin, motivo: " + motivoLimpio;
        logRepository.save(new Log(mensaje));
    }

    // Cuenta las fotos vigentes (eliminada = false)
    public long contarVigentes() {
        return fotoRepository.countByEliminada(false);
    }

    // Cuenta las fotos eliminadas (eliminada = true)
    public long contarEliminadas() {
        return fotoRepository.countByEliminada(true);
    }
}