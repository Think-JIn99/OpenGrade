package com.opengrade.server.controller;

import com.opengrade.server.config.security.JwtTokenProvider;
import com.opengrade.server.data.dto.RankingDto;
import com.opengrade.server.service.ReturnResultService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/result")
public class ReturnResultController {

    ReturnResultService returnResultService;
    JwtTokenProvider jwtTokenProvider;

    @Autowired
    ReturnResultController(ReturnResultService returnResultService, JwtTokenProvider jwtTokenProvider) {
        this.returnResultService = returnResultService;
        this.jwtTokenProvider = jwtTokenProvider;
    }

    @GetMapping("/allranking/{department}")
    public RankingDto allRanking(@RequestHeader String jwtToken, @PathVariable String department) {
        String studentId = jwtTokenProvider.getUsername(jwtToken);
        RankingDto rankingDto = new RankingDto();
        returnResultService.getAllGrade(rankingDto, studentId, department);
        return rankingDto;
    }

    @GetMapping("/applyranking/{department}")
    public RankingDto applyRanking(@RequestHeader String jwtToken, @PathVariable String department) {
        String studentId = jwtTokenProvider.getUsername(jwtToken);
        RankingDto rankingDto = new RankingDto();
        returnResultService.getApplyGrade(rankingDto, studentId, department);
        return rankingDto;
    }

}
