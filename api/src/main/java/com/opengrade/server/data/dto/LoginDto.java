package com.opengrade.server.data.dto;

import io.swagger.annotations.ApiParam;
import lombok.*;
import javax.validation.constraints.NotBlank;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
@ToString
public class LoginDto {

    @ApiParam(value = "id", required = true)
    @NotBlank
    private String id;

    @ApiParam(value = "pw", required = true)
    @NotBlank
    private String pw;

}
