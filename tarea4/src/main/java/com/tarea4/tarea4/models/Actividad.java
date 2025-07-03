package com.tarea4.tarea4.models;

import java.time.LocalDateTime;

import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.OneToMany;
import jakarta.persistence.OneToOne;
import jakarta.persistence.Table;
import jakarta.validation.constraints.NotNull;
import jakarta.persistence.CascadeType;
import java.util.List;

@Entity
@Table(name = "actividad")
public class Actividad {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @NotNull
    private Integer comuna_id;

    private String sector;

    @NotNull 
    private String nombre;

    @NotNull
    private String email;

    private String celular;

    @NotNull
    private LocalDateTime diaHoraInicio;

    private LocalDateTime diaHoraTermino;

    private String descripcion;

    @OneToOne(mappedBy = "actividad", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private ActividadTema actividadTema;

    @OneToMany(mappedBy = "actividad", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<Nota> nota;

    public Actividad() {
    }

    public Actividad(Integer comuna_id, 
                String sector, 
                String nombre, 
                String email, 
                String celular, 
                LocalDateTime diaHoraInicio,
                LocalDateTime diaHoraTermino,
                String descripcion) {
                    this.comuna_id = comuna_id;
                    this.sector = sector;
                    this.nombre = nombre;
                    this.email = email;
                    this.celular = celular;
                    this.diaHoraInicio = diaHoraInicio;
                    this.diaHoraTermino = diaHoraTermino;
                    this.descripcion = descripcion;
                }

    public ActividadTema getActividadTema() { 
        return actividadTema; 
    }

    public List<Nota> getNota() { 
        return nota; 
    }
    
    public Integer getId() {
        return id;
    }

    public Integer getComuna() {
        return comuna_id;
    }

    public String getSector() {
        return sector;
    }

    public String getNombre() {
        return nombre;
    }

    public String getEmail() {
        return email;
    }

    public String getCelular() {
        return celular;
    }

    public LocalDateTime getDiaHoraInicio() {
        return diaHoraInicio;
    }

    public LocalDateTime getDiaHoraTermino() {
        return diaHoraTermino;
    }

    public String getDescripcion() {
        return descripcion;
    }
}
