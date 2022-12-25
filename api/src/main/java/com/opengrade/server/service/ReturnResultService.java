package com.opengrade.server.service;

import com.opengrade.server.data.dto.RankingDto;
import org.springframework.stereotype.Service;

@Service
public interface ReturnResultService {


    public void getAllGrade(RankingDto rankingDto, String studentId, String department);

    public void getApplyGrade(RankingDto rankingDto, String studentId, String department);

}

