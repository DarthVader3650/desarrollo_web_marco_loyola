package com.tarea4.tarea4.models;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.OneToOne;
import jakarta.persistence.Table;
import jakarta.validation.constraints.NotNull;

@Entity
@Table(name = "actividad_tema")
public class ActividadTema {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @NotNull
    private String tema;

    private String glosa_otro;

    @OneToOne
    @JoinColumn(name = "actividad_id", referencedColumnName = "id")
    private Actividad actividad;

    public ActividadTema() {
    }

    public ActividadTema(String tema,
                    String glosa_otro,
                    Actividad actividad) {
                        this.tema = tema;
                        this.glosa_otro = glosa_otro;
                        this.actividad = actividad;
                    }

    public Integer getId() {
        return id;
    }

    public String getTema() {
        return tema;
    }

    public String getGlosaOtro() {
        return glosa_otro;
    }

    public Actividad getActividad() {
        return actividad;
    }
}
