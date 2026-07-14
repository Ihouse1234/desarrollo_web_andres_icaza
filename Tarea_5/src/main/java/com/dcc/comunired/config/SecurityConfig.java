package com.dcc.comunired.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.crypto.password.NoOpPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.provisioning.InMemoryUserDetailsManager;
import org.springframework.security.web.SecurityFilterChain;

@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Bean
    public UserDetailsService userDetailsService() {
        UserDetails admin = User.builder()
                .username("cc5002")
                .password("examen")
                .roles("ADMIN")
                .build();

        UserDetails auditor = User.builder()
                .username("auditor")
                .password("log-auditor")
                .roles("AUDITOR")
                .build();

        return new InMemoryUserDetailsManager(admin, auditor);
    }

    @Bean
    @SuppressWarnings("deprecation")
    public PasswordEncoder passwordEncoder() {
        return NoOpPasswordEncoder.getInstance();
    }


    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/estadistica-fotos").permitAll()
                .requestMatchers("/api/estadistica-fotos").permitAll()
                .requestMatchers("/css/**", "/js/**", "/uploads/**").permitAll()  // recursos estáticos
                .requestMatchers("/", "/api/buscar", "/api/actividades/**").permitAll()  // Tarea 4

                .requestMatchers("/admin-fotos/**").hasRole("ADMIN")
                .requestMatchers("/api/fotos/**").hasRole("ADMIN")   // el endpoint de eliminar

                .requestMatchers("/mensajes-log/**").hasAnyRole("ADMIN", "AUDITOR")

                // Cualquier otra URL: permitida
                .anyRequest().permitAll()
            )
            // Formulario de login por defecto de Spring Security
            .formLogin(form -> form.permitAll())
            .logout(logout -> logout.permitAll())
            // CSRF desactivado para simplificar las llamadas AJAX del enunciado
            .csrf(csrf -> csrf.disable());

        return http.build();
    }
}