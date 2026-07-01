package com.dcc.comunired.entity;

import jakarta.persistence.*;
import java.util.List;

/**
 * Entidad Actividad: mapea la tabla "actividad".
 * Pertenece a un Miembro y puede tener muchas Notas.
 */
@Entity
@Table(name = "actividad")
public class Actividad {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @ManyToOne
    @JoinColumn(name = "miembro_id")
    private Miembro miembro;

    // Los ENUM de MySQL se mapean como String en Java.
    @Column(name = "dia")
    private String dia;

    @Column(name = "hora_inicio")
    private String horaInicio;

    @Column(name = "duracion")
    private String duracion;

    @Column(name = "tipo")
    private String tipo;

    @Column(name = "nombre")
    private String nombre;

    @Column(name = "descripcion")
    private String descripcion;

    /**
     * Relación con Nota: una actividad -> muchas notas.
     * mappedBy="actividad" indica que la FK está en la entidad Nota.
     */
    @OneToMany(mappedBy = "actividad")
    private List<Nota> notas;

    // ── Getters y setters ──
    public Integer getId() { return id; }
    public void setId(Integer id) { this.id = id; }

    public Miembro getMiembro() { return miembro; }
    public void setMiembro(Miembro miembro) { this.miembro = miembro; }

    public String getDia() { return dia; }
    public void setDia(String dia) { this.dia = dia; }

    public String getHoraInicio() { return horaInicio; }
    public void setHoraInicio(String horaInicio) { this.horaInicio = horaInicio; }

    public String getDuracion() { return duracion; }
    public void setDuracion(String duracion) { this.duracion = duracion; }

    public String getTipo() { return tipo; }
    public void setTipo(String tipo) { this.tipo = tipo; }

    public String getNombre() { return nombre; }
    public void setNombre(String nombre) { this.nombre = nombre; }

    public String getDescripcion() { return descripcion; }
    public void setDescripcion(String descripcion) { this.descripcion = descripcion; }

    public List<Nota> getNotas() { return notas; }
    public void setNotas(List<Nota> notas) { this.notas = notas; }
}