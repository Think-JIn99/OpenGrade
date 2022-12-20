package com.opengrade.server.controller;

import com.opengrade.server.config.security.JwtTokenProvider;
import com.opengrade.server.data.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Component;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;

@RestController
@RequestMapping("/scrapping")
public class ScrappingRequestController {

    UserRepository userRepository;
    JwtTokenProvider jwtTokenProvider;

    @Autowired
    public ScrappingRequestController(UserRepository userRepository, JwtTokenProvider jwtTokenProvider) {
        this.userRepository = userRepository;
        this.jwtTokenProvider = jwtTokenProvider;
    }

    @PostMapping(value = "/request")
    public void ScrappingRequest(@RequestHeader String jwtToken){

        String studentId = jwtTokenProvider.getUsername(jwtToken);
        String sToken = jwtTokenProvider.getsToken(jwtToken);

        String scrappingUrl = "";

            MultiValueMap<String, String> params = new LinkedMultiValueMap<>();
            params.add("sToken", sToken);

            HttpHeaders headers = new HttpHeaders();

            HttpEntity<MultiValueMap<String, String>> entity = new HttpEntity<>(params, headers);

            RestTemplate restTemplate = new RestTemplate();

            ResponseEntity<String> response = restTemplate.exchange(
                    scrappingUrl,
                    HttpMethod.POST,
                    entity,
                    String.class
            );

        }
    }

