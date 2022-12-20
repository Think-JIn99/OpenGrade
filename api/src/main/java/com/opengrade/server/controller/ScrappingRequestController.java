package com.opengrade.server.controller;

import com.opengrade.server.data.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;

@RestController
@RequestMapping("/scrapping")
public class ScrappingRequestController {

    @Autowired
    UserRepository userRepository;

    @PostMapping(value = "/request")
    public void ScrappingRequest(@RequestBody String sToken){

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

