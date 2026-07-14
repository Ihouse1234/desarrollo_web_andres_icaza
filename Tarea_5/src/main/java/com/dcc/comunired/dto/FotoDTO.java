package com.dcc.comunired.dto;


public class FotoDTO {

    private Integer id;
    private String nombreArchivo;   // para construir la ruta de la imagen
    private String fechaRegistro;   // fecha_registro del miembro (formateada)
    private String comuna;          // nombre de la comuna del miembro
    private String email;           // email del miembro
    private Boolean eliminada;      // estado de la foto

    public FotoDTO(Integer id, String nombreArchivo, String fechaRegistro,
                   String comuna, String email, Boolean eliminada) {
        this.id = id;
        this.nombreArchivo = nombreArchivo;
        this.fechaRegistro = fechaRegistro;
        this.comuna = comuna;
        this.email = email;
        this.eliminada = eliminada;
    }

    // ── Getters ──
    public Integer getId() { return id; }
    public String getNombreArchivo() { return nombreArchivo; }
    public String getFechaRegistro() { return fechaRegistro; }
    public String getComuna() { return comuna; }
    public String getEmail() { return email; }
    public Boolean getEliminada() { return eliminada; }
}