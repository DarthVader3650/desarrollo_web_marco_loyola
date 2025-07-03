package com.tarea4.tarea4.controllers;

import java.util.List;
import java.util.Map;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

import com.tarea4.tarea4.services.ActividadService;

@Controller
public class AppController {
    private final ActividadService actividadService;
    public AppController(ActividadService actividadService) {
        this.actividadService = actividadService;
    }

    @GetMapping("/")
    public String mostarActividades(Model model) {
        List<Map<String, Object>> actividades = actividadService.getActividadesRealizadas();
        // Para debugear:
        // System.out.println("Número de actividades en el controlador: " + actividades.size());
        model.addAttribute("actividades", actividades);
        return "tabla";
    }
}
