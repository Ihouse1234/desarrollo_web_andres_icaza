package com.dcc.comunired.controller;

import com.dcc.comunired.service.LogService;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class LogController {

    private final LogService logService;

    public LogController(LogService logService) {
        this.logService = logService;
    }

    /**
     * Muestra la tabla completa de logs de la más reciente a la más antigua.
     */
    @GetMapping("/mensajes-log")
    public String mensajesLog(Model model) {
        model.addAttribute("logs", logService.listarTodos());
        return "mensajes-log";   // renderiza templates/mensajes-log.html
    }
}