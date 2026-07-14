package com.dcc.comunired.repository;

import com.dcc.comunired.entity.Foto;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

import java.util.List;

public interface FotoRepository extends JpaRepository<Foto, Integer> {

    /**
     * Trae las fotos ordenadas de la mas reciente a la mas antigua.
     * La cadena de JOINs sigue la relación:
     *   foto -> actividad -> miembro -> comuna
     */
    
    @Query("SELECT f FROM Foto f " +
           "JOIN FETCH f.actividad a " +
           "JOIN FETCH a.miembro m " +
           "JOIN FETCH m.comuna c " +
           "ORDER BY m.fechaRegistro DESC")
    List<Foto> listarParaAdmin();

    long countByEliminada(Boolean eliminada);
}