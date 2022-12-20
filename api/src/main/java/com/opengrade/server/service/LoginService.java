package com.opengrade.server.service;

import com.opengrade.server.data.dto.LoginResponseDto;
import org.springframework.stereotype.Service;

@Service
public interface LoginService {

    public String tryLogin(String id, String pw);

    public void isValidateLogin(String returnToken, LoginResponseDto loginResponseDto);

    public void searchGrade(LoginResponseDto loginResponseDto, String id);

    public void saveUser(String id, LoginResponseDto loginResponseDto);

    public void loadUsaint(LoginResponseDto loginResponseDto);

    public void generateNickname(LoginResponseDto loginResponseDto);

    public void generateToken(LoginResponseDto loginResponseDto, String id);

    public void saveApply(String studentId, String department);
}
