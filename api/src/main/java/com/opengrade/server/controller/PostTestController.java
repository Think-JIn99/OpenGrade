package com.opengrade.server.controller;

import com.opengrade.server.data.entity.Grade;
import com.opengrade.server.data.entity.User;
import com.opengrade.server.data.repository.GradeRepository;
import com.opengrade.server.data.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
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
        Map<String, String> test1 = new HashMap<>();
        Map<String, String> test2 = new HashMap<>();

        LocalDateTime localDateTime = LocalDateTime.now();

        HashMap<String, Map<String, String>> testMap = new HashMap<>();
        User user1 = new User();
        Grade grade1 = new Grade();

        test1.put("과목명", "컴수");
        test1.put("이수학점", "3");
        test1.put("성적", "97");
        test1.put("등급", "A+");
        test1.put("교수명", "최종선");

        test2.put("과목명", "플밍");
        test2.put("이수학점", "3");
        test2.put("성적", "90");
        test2.put("등급", "A-");
        test2.put("교수명", "김익수");

        testMap.put("123456", test1);
        testMap.put("78910", test2);

        user1.setId(20212227);
        user1.setCurrentSemester(1);
        user1.setCurrentSemester(2021);
        user1.setUpdateTime(localDateTime);

        grade1.setGrade(testMap);
        grade1.setId(user1);
        grade1.setYear(2021);
        grade1.setSemester(1);
        grade1.setUpdateTime(localDateTime);
        grade1.setIdx(1);

        userRepository.save(user1);
        gradeRepository.save(grade1);

    }

}
