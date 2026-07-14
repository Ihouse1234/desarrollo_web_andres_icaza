package com.dcc.comunired.entity;

import jakarta.persistence.*;

@Entity
@Table(name = "foto")
public class Foto {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @Column(name = "ruta_archivo", nullable = false)
    private String rutaArchivo;

    @Column(name = "nombre_archivo", nullable = false)
    private String nombreArchivo;

    /*Se usa para llegar al miembro (foto -> actividad -> miembro -> comuna).*/
    @ManyToOne
    @JoinColumn(name = "actividad_id", nullable = false)
    private Actividad actividad;

    /**
     * false = foto vigente
     * true = foto eliminada
     */
    @Column(name = "eliminada", nullable = false)
    private Boolean eliminada = false;

    // ── Getters y setters ──
    public Integer getId() { return id; }
    public void setId(Integer id) { this.id = id; }

    public String getRutaArchivo() { return rutaArchivo; }
    public void setRutaArchivo(String rutaArchivo) { this.rutaArchivo = rutaArchivo; }

    public String getNombreArchivo() { return nombreArchivo; }
    public void setNombreArchivo(String nombreArchivo) { this.nombreArchivo = nombreArchivo; }

    public Actividad getActividad() { return actividad; }
    public void setActividad(Actividad actividad) { this.actividad = actividad; }

    public Boolean getEliminada() { return eliminada; }
    public void setEliminada(Boolean eliminada) { this.eliminada = eliminada; }
}