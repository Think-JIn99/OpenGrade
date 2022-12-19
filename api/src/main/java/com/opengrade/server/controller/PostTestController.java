package com.opengrade.server.controller;

import com.opengrade.server.data.entity.Grade;
import com.opengrade.server.data.entity.User;
import com.opengrade.server.data.repository.GradeRepository;
import com.opengrade.server.data.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/test")
public class PostTestController {

    @Autowired
    UserRepository userRepository;

    @Autowired
    GradeRepository gradeRepository;

    @PostMapping("/post")
    public void testApi() {
        Map<String, String> gradeMath = new HashMap<>();
        Map<String, String> gradeProgram = new HashMap<>();

        LocalDateTime localDateTime = LocalDateTime.now();

        HashMap<String, Map<String, String>> gradeAll = new HashMap<>();
        User user1 = new User();
        Grade grade1 = new Grade();

        gradeMath.put("과목명", "컴수");
        gradeMath.put("이수학점", "3");
        gradeMath.put("성적", "97");
        gradeMath.put("등급", "A+");
        gradeMath.put("교수명", "최종선");

        gradeProgram.put("과목명", "플밍");
        gradeProgram.put("이수학점", "3");
        gradeProgram.put("성적", "90");
        gradeProgram.put("등급", "A-");
        gradeProgram.put("교수명", "김익수");

        gradeAll.put("123456", gradeMath);
        gradeAll.put("78910", gradeProgram);

        user1.setStudentId("20212227");
        user1.setCurrentSemester("2");
        user1.setCurrentYear("2022");
        user1.setDepartment("컴퓨터학부");
        user1.setUpdateTime(localDateTime);

        grade1.setGrade(gradeAll);
        grade1.setStudentId(user1);
        grade1.setYear("2021");
        grade1.setSemester("1");
        grade1.setUpdateTime(localDateTime);

        userRepository.save(user1);
        gradeRepository.save(grade1);

    }

}
