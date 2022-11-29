//package com.opengrade.server.controller;
//
//import com.opengrade.server.data.dto.LoginResponseDto;
//import com.opengrade.server.service.LoginService;
//import lombok.extern.java.Log;
//import org.springframework.beans.factory.annotation.Autowired;
//import org.springframework.http.*;
//import org.springframework.util.LinkedMultiValueMap;
//import org.springframework.util.MultiValueMap;
//import org.springframework.web.bind.annotation.PostMapping;
//import org.springframework.web.bind.annotation.RequestMapping;
//import org.springframework.web.bind.annotation.RequestParam;
//import org.springframework.web.bind.annotation.RestController;
//import org.springframework.web.client.RestTemplate;
//
//@RestController
//@RequestMapping("/login")
//public class LoginController {
//
//    LoginService loginService;
//
//    @Autowired
//    public LoginController(LoginService loginService) {
//        this.loginService = loginService;
//    }
//
//
//    @PostMapping("/request")
//    public LoginResponseDto loginRequest(@RequestParam String id, @RequestParam String pw) {
//        String sToken = loginService.tryLogin(id, pw);
//        return loginService.isValidateLogin(sToken);
//    }
//}
