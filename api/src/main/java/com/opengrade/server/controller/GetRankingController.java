package com.opengrade.server.controller;

import com.opengrade.server.data.dto.AllRankingDto;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("getranking")
public class GetRankingController {

    private AllRankingDto allRankingDto;

    public GetRankingController() {
        this.allRankingDto = new AllRankingDto();
    }


    @GetMapping("/all")
    public ResponseEntity<AllRankingDto> getAllRanking() {
        return ResponseEntity.status(HttpStatus.OK).body(this.allRankingDto);
    }

}
