package com.opengrade.server.controller;

import com.opengrade.server.data.repository.GradeRepository;
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
    GradeRepository gradeRepository;

    @Autowired
    UserRepository userRepository;

    //스크래핑한테 토큰을 포스트 하기
    @PostMapping(value = "/request")
    public void ScrappingRequest(@RequestBody String sToken){
        //sToken을 post하는 코드를 여기에다가 짜기
        //숭실대 유세인트에서 SToken을 받아오기
        //그 토큰을 스크래핑한테 쏘기

        String scrappingUrl = "";

            // request의 body
            MultiValueMap<String, String> params = new LinkedMultiValueMap<>();

            //헤더
            //생성은 하고 add~ 안해도 됨
            HttpHeaders headers = new HttpHeaders();

            headers.add("referer", scrappingUrl);
            headers.add("user-agent", "");

            //바디와 헤더 합치기
            HttpEntity<MultiValueMap<String, String>> entity = new HttpEntity<>(params, headers);

            RestTemplate restTemplate = new RestTemplate();
            //.exchange: 모든 http 요청 메소드를 지원하며 원하는 서버에 요청시켜 주는 메소드
            ResponseEntity<String> response = restTemplate.exchange(
                    scrappingUrl, //요청할 서버 주소
                    HttpMethod.POST,  //요청할 방식
                    entity,  //요청할 때 보내는 데이터
                    String.class  //요청시 반환하는 데이터 타입
            );

        }
    }

