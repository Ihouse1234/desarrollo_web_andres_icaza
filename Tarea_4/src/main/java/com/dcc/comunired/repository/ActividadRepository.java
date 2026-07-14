package com.dcc.comunired.repository;

import com.dcc.comunired.entity.Actividad;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

public interface ActividadRepository extends JpaRepository<Actividad, Integer> {

    /**
     * - JOIN a.miembro m, accede al miembro de la actividad
     * - JOIN m.comuna c  y a su comuna
     * - LIKE %:patron%, busca el patrón en cualquier parte del texto
     * - LOWER(...), hace la búsqueda insensible a mayúsculas
     */
    @Query("SELECT a FROM Actividad a " +
           "JOIN a.miembro m " +
           "JOIN m.comuna c " +
           "WHERE LOWER(a.nombre) LIKE LOWER(CONCAT('%', :patron, '%')) " +
           "   OR LOWER(a.descripcion) LIKE LOWER(CONCAT('%', :patron, '%')) " +
           "   OR LOWER(c.nombre) LIKE LOWER(CONCAT('%', :patron, '%'))")
    List<Actividad> buscar(@Param("patron") String patron);
}