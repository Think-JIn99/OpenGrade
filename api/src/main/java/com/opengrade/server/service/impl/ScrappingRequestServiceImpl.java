package com.opengrade.server.service.impl;

import com.opengrade.server.data.entity.User;
import com.opengrade.server.data.repository.UserRepository;
import com.opengrade.server.service.ScrappingRequestService;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.RestTemplate;

@Service
public class ScrappingRequestServiceImpl implements ScrappingRequestService {
    private final UserRepository userRepository;

    public ScrappingRequestServiceImpl(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    public Boolean verifyGrade(String id) {
        int tempId = Integer.parseInt(id);
        User user = userRepository.getUserByStudentId(Integer.valueOf(tempId));

        try {
            Integer mathGrade = user.getMath();
            return Boolean.TRUE;
        } catch (NullPointerException e) {
            return Boolean.FALSE;
        }
    }

    public String postRequest(String id, String sToken) {
        String scrappingUrl = "http://34.64.211.170:8080/grade/year";

        MultiValueMap<String, String> params = new LinkedMultiValueMap<>();
        params.add("sToken", sToken);
        params.add("studentId", id);

        HttpHeaders headers = new HttpHeaders();

        HttpEntity<MultiValueMap<String, String>> entity = new HttpEntity<>(params, headers);

        RestTemplate restTemplate = new RestTemplate();

        ResponseEntity<String> response = restTemplate.exchange(
                scrappingUrl,
                HttpMethod.POST,
                entity,
                String.class
        );

        return response.getBody();
    }
}
