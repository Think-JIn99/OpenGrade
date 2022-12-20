package com.opengrade.server.data.dto;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class LoginResponseDto {

    private Boolean loginValidate;
    private String sToken;
    private String department;
    private String nickName;
    private String Token;

}
