package com.dcc.comunired.entity;

import jakarta.persistence.*;

/**
 * Entidad Region: mapea la tabla "region".
 * Equivale al modelo Region de Flask.
 */
@Entity                       
@Table(name = "region")       
public class Region {

    @Id                                                  
    @GeneratedValue(strategy = GenerationType.IDENTITY)  
    private Integer id;

    @Column(nullable = false)
    private String nombre;

    public Integer getId() { return id; }
    public void setId(Integer id) { this.id = id; }

    public String getNombre() { return nombre; }
    public void setNombre(String nombre) { this.nombre = nombre; }
}