package com.opengrade.server.controller;

import com.opengrade.server.config.security.JwtTokenProvider;
import com.opengrade.server.data.dto.ScrappingResponseDto;
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
    public ScrappingResponseDto ScrappingRequest(@RequestHeader String jwtToken) {

        ScrappingResponseDto scrappingResponseDto = new ScrappingResponseDto();

        String studentId = jwtTokenProvider.getUsername(jwtToken);
        String sToken = jwtTokenProvider.getsToken(jwtToken);

        Boolean isPresent = scrappingRequestService.verifyGrade(studentId);

        if (isPresent == Boolean.FALSE) {
            String message = scrappingRequestService.postRequest(studentId, sToken);
            scrappingResponseDto.setMessage(message);
            return scrappingResponseDto;
        }

        scrappingResponseDto.setMessage("success");
        return scrappingResponseDto;
    }

}

