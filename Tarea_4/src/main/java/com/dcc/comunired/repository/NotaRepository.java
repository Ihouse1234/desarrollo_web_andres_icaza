package com.dcc.comunired.repository;

import com.dcc.comunired.entity.Nota;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

public interface NotaRepository extends JpaRepository<Nota, Integer> {

    List<Nota> findByActividad_Id(Integer actividadId);

    
    // Calcula el promedio de notas de una actividad directamente.
    @Query("SELECT AVG(n.nota) FROM Nota n WHERE n.actividad.id = :actividadId")
    Double calcularPromedio(@Param("actividadId") Integer actividadId);
}