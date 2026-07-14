package com.dcc.comunired.dto;

public class ActividadDTO {

    private Integer id;
    private String nombreMiembro;   // nombre del miembro asociado
    private String dia;
    private String tipo;
    private String comuna;
    private String nombre;
    private String descripcion;
    private String nota;            // promedio formateado, o "-" si no tiene notas

    public ActividadDTO(Integer id, String nombreMiembro, String dia, String tipo,
                        String comuna, String nombre, String descripcion, String nota) {
        this.id = id;
        this.nombreMiembro = nombreMiembro;
        this.dia = dia;
        this.tipo = tipo;
        this.comuna = comuna;
        this.nombre = nombre;
        this.descripcion = descripcion;
        this.nota = nota;
    }

    public Integer getId() { return id; }
    public String getNombreMiembro() { return nombreMiembro; }
    public String getDia() { return dia; }
    public String getTipo() { return tipo; }
    public String getComuna() { return comuna; }
    public String getNombre() { return nombre; }
    public String getDescripcion() { return descripcion; }
    public String getNota() { return nota; }
}