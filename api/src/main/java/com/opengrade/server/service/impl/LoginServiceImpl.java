package com.opengrade.server.service.impl;

import com.opengrade.server.data.dto.LoginResponseDto;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.RestTemplate;

public class LoginServiceImpl {

    public String tryLogin(String id, String pw) {

        String loginUrl = "https://smartid.ssu.ac.kr/Symtra_sso/smln_pcs.asp";

        MultiValueMap<String, String> params = new LinkedMultiValueMap<>();

        params.add("in_tp_bit", "0");
        params.add("rqst_caus_cd", "03");
        params.add("userid", id);
        params.add("pwd", pw);

        HttpHeaders headers = new HttpHeaders();

        headers.add("referer", loginUrl);
        headers.add("user-agent", "");

        HttpEntity<MultiValueMap<String, String>> entity = new HttpEntity<>(params, headers);

        RestTemplate restTemplate = new RestTemplate();

        ResponseEntity<String> response = restTemplate.exchange(
                loginUrl,
                HttpMethod.POST,
                entity,
                String.class
        );

        return response.getHeaders().get("Set-Cookie").get(2);
    }

    public LoginResponseDto isValidateLogin(String sToken) {

        LoginResponseDto loginResponseDto = new LoginResponseDto();

        if (sToken.substring(0,7).equals("sToken=")) {
            sToken = sToken.substring(7);
            loginResponseDto.setSToken(sToken);
            return loginResponseDto;
        }
        loginResponseDto.setSToken(null);
        return loginResponseDto;
    }


}
