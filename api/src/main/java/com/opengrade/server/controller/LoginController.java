package com.opengrade.server.controller;

import com.opengrade.server.config.security.JwtTokenProvider;
import com.opengrade.server.data.dto.ApplyDepartmentDto;
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
    JwtTokenProvider jwtTokenProvider;

    @Autowired
    public LoginController(LoginService loginService, JwtTokenProvider jwtTokenProvider) {
        this.loginService = loginService;
        this.jwtTokenProvider = jwtTokenProvider;
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
            loginResponseDto.setSToken("");
            return loginResponseDto;
        }

        Boolean isPresent = loginService.isAlreadyPresentUser(loginDto.getId(), loginResponseDto);

        // 기존 회원은 여기서 끝
        if (isPresent == Boolean.TRUE) {
            loginService.generateToken(loginResponseDto, loginDto.getId());
            return loginResponseDto;
        }

        loginService.generateNickname(loginResponseDto);
        loginService.generateToken(loginResponseDto, loginDto.getId());

        loginService.saveUser(loginDto.getId(), loginResponseDto);
        return loginResponseDto;

    }

    @PostMapping("/apply")
    public void applyDepartment(@RequestHeader String jwtToken,
                                @Validated @RequestBody ApplyDepartmentDto applyDepartmentDto) {
        String studentId = jwtTokenProvider.getUsername(jwtToken);
        loginService.saveApply(studentId, applyDepartmentDto.getDepartment());
    }
}

