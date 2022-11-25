package com.opengrade.server.controller;

import com.opengrade.server.data.dto.InputGradeDto;
import com.opengrade.server.data.dto.InputResultDto;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;



@RestController
@RequestMapping("submit")
public class SubmitController {

    @PostMapping("/grade")
    public InputResultDto submitGrade(
            @Validated InputGradeDto inputGradeDto) {
        InputResultDto inputResultDto = new InputResultDto();
        return inputResultDto;
    }

}
