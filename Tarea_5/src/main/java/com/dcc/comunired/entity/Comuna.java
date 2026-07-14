package com.dcc.comunired.entity;

import jakarta.persistence.*;

/**
 * Entidad Comuna: mapea la tabla "comuna".
 * Tiene una relación con Region (muchas comunas pertenecen a una región).
 */
@Entity
@Table(name = "comuna")
public class Comuna {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @Column(nullable = false)
    private String nombre;

    /**
     * Relación con Region: muchas comunas -> una región.
     * @JoinColumn especifica la columna FK en la tabla comuna.
     */
    
    @ManyToOne
    @JoinColumn(name = "region_id")
    private Region region;

    public Integer getId() { return id; }
    public void setId(Integer id) { this.id = id; }

    public String getNombre() { return nombre; }
    public void setNombre(String nombre) { this.nombre = nombre; }

    public Region getRegion() { return region; }
    public void setRegion(Region region) { this.region = region; }
}