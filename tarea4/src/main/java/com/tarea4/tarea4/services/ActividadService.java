package com.tarea4.tarea4.services;

import com.tarea4.tarea4.models.Actividad;
import com.tarea4.tarea4.models.ActividadTema;
import com.tarea4.tarea4.models.Nota;
import com.tarea4.tarea4.models.ActividadRepository;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
public class ActividadService {
    private final ActividadRepository actividadRepository;
    public ActividadService(ActividadRepository actividadRepository) {
        this.actividadRepository = actividadRepository;
    }

    public List<Map<String, Object>> getActividadesRealizadas() {
        LocalDateTime fecha = LocalDateTime.now();
        List<Actividad> actividadesTerminadas = actividadRepository.findByDiaHoraTerminoBefore(fecha);
        // Para debugear:
        // System.out.println("Actividades encontradas: " + actividadesTerminadas.size());
        // if (actividadesTerminadas.isEmpty()) {
        //    System.out.println("¡Advertencia: No se encontraron actividades terminadas!");
        // }

        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("dd-MM-yyyy HH:mm");

        List<Map<String, Object>> data_terminada = new ArrayList<>();
        for(Actividad actividad : actividadesTerminadas) {
            Map<String, Object> actividadDetalle = new HashMap<>();
            actividadDetalle.put("id", actividad.getId());
            String fechaInicioFormateada = actividad.getDiaHoraInicio().format(formatter);
            actividadDetalle.put("fechaInicio", fechaInicioFormateada);
            String sector = "Sin especificar";
            if (!actividad.getSector().isEmpty()) {
                sector = actividad.getSector();
            }
            actividadDetalle.put("sector", sector);
            actividadDetalle.put("nombre", actividad.getNombre());

            ActividadTema actividad_tema = actividad.getActividadTema();
            String tema = "Sin Tema";
            if (actividad_tema != null) {
                tema = actividad_tema.getTema();
            }
            actividadDetalle.put("tema", tema);

            String nota_promedio = "";

            if (actividad.getNota() == null || actividad.getNota().isEmpty()) {
                nota_promedio = "-";
            } else {
                Double sumaNotas = 0.0;
                for (Nota nota : actividad.getNota()) {
                    sumaNotas += nota.getNota();
                }
                Double promedio = sumaNotas / actividad.getNota().size();
                Long promedioRedondeado = Math.round(promedio);
                nota_promedio = String.valueOf(promedioRedondeado);
            }
            actividadDetalle.put("notaPromedio", nota_promedio);
            data_terminada.add(actividadDetalle);
        }
        return data_terminada;
    }
}
