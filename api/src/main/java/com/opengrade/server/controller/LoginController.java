package com.opengrade.server.controller;

import com.opengrade.server.data.dto.LoginResponseDto;
import com.opengrade.server.service.LoginService;
import com.opengrade.server.data.dto.LoginDto;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/login")
public class LoginController {

    LoginService loginService;

    @Autowired
    public LoginController(LoginService loginService) {
        this.loginService = loginService;
    }


    @PostMapping(value = "/request")
    public LoginResponseDto loginRequest(@Validated @RequestBody LoginDto loginDto) {

        LoginResponseDto loginResponseDto = new LoginResponseDto();
        String returnToken = loginService.tryLogin(loginDto.getId(), loginDto.getPw());
        loginService.isValidateLogin(returnToken, loginResponseDto);

        // 로그인 실패시 여기서 끝
        if (loginResponseDto.getLoginValidate() == Boolean.FALSE) {
            return loginResponseDto;
        }

        loginService.loadUsaint(loginResponseDto);

        // 융특아니면 끝
        if (!loginResponseDto.getDepartment().equals("융합특성화자유전공학부")) {
            return loginResponseDto;
        }

        loginService.generateNickname(loginResponseDto);

        return loginResponseDto;

    }
}

    // 지망 학과 받기


    //성적 조회
    //loginService.saveUser(loginDto.getId(), tempSemester, tempYear, tempDepart);
    //loginService.searchGrade(loginResponseDto, loginDto.getId());
    //return loginResponseDto;


