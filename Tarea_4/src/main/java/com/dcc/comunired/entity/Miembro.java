package com.dcc.comunired.entity;

import jakarta.persistence.*;
import java.time.LocalDateTime;

/**
 * Entidad Miembro: mapea la tabla "miembro".
 * Pertenece a una comuna.
 */
@Entity
@Table(name = "miembro")
public class Miembro {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @Column(nullable = false)
    private String nombre;

    @Column(nullable = false)
    private String email;

    @Column(nullable = false)
    private String telefono;

    // LocalDateTime es el tipo de Java para fecha + hora.
    @Column(name = "fecha_registro", nullable = false)
    private LocalDateTime fechaRegistro;

    @ManyToOne
    @JoinColumn(name = "comuna_id")
    private Comuna comuna;

    public Integer getId() { return id; }
    public void setId(Integer id) { this.id = id; }

    public String getNombre() { return nombre; }
    public void setNombre(String nombre) { this.nombre = nombre; }

    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }

    public String getTelefono() { return telefono; }
    public void setTelefono(String telefono) { this.telefono = telefono; }

    public LocalDateTime getFechaRegistro() { return fechaRegistro; }
    public void setFechaRegistro(LocalDateTime fechaRegistro) { this.fechaRegistro = fechaRegistro; }

    public Comuna getComuna() { return comuna; }
    public void setComuna(Comuna comuna) { this.comuna = comuna; }
}