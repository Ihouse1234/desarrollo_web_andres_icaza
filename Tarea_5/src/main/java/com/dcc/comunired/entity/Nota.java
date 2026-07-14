package com.dcc.comunired.entity;

import jakarta.persistence.*;

/**
 * Entidad Nota: mapea la tabla "nota" (creada con tabla-nota.sql).
 * Cada fila es UNA evaluación (1-7) de una actividad.
 * El promedio se calcula sumando todas las notas de una actividad.
 */
@Entity
@Table(name = "nota")
public class Nota {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @ManyToOne
    @JoinColumn(name = "actividad_id", nullable = false)
    private Actividad actividad;

    @Column(name = "nota", nullable = false)
    private Integer nota;
    
    public Integer getId() { return id; }
    public void setId(Integer id) { this.id = id; }

    public Actividad getActividad() { return actividad; }
    public void setActividad(Actividad actividad) { this.actividad = actividad; }

    public Integer getNota() { return nota; }
    public void setNota(Integer nota) { this.nota = nota; }
}