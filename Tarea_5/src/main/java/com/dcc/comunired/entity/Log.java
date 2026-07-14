package com.dcc.comunired.entity;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "log")
public class Log {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    // Lo ponemos explícitamente desde Java para tener control del valor.
    @Column(name = "fecha", nullable = false)
    private LocalDateTime fecha;

    // El mensaje del formato
    // "eliminado foto {id-foto} por usuario admin, motivo: {motivo}"
    @Column(name = "mensaje", nullable = false, length = 300)
    private String mensaje;

    public Log() {}

    public Log(String mensaje) {
        this.mensaje = mensaje;
        this.fecha = LocalDateTime.now();
    }

    // ── Getters y setters ──
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public LocalDateTime getFecha() { return fecha; }
    public void setFecha(LocalDateTime fecha) { this.fecha = fecha; }

    public String getMensaje() { return mensaje; }
    public void setMensaje(String mensaje) { this.mensaje = mensaje; }
}