package com.opengrade.server.controller;

import com.opengrade.server.config.security.JwtTokenProvider;
import com.opengrade.server.data.repository.UserRepository;
import com.opengrade.server.service.ScrappingRequestService;
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
    JwtTokenProvider jwtTokenProvider;
    ScrappingRequestService scrappingRequestService;

    @Autowired
    public ScrappingRequestController(JwtTokenProvider jwtTokenProvider, ScrappingRequestService scrappingRequestService) {
        this.jwtTokenProvider = jwtTokenProvider;
        this.scrappingRequestService = scrappingRequestService;
    }

    @PostMapping(value = "/request")
    public void ScrappingRequest(@RequestHeader String jwtToken){

        String studentId = jwtTokenProvider.getUsername(jwtToken);
        String sToken = jwtTokenProvider.getsToken(jwtToken);

        Boolean isPresent = scrappingRequestService.verifyGrade(studentId);

        if (isPresent == Boolean.FALSE) {
            scrappingRequestService.postRequest(studentId, sToken);
        }


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

