package com.opengrade.server.controller;

import com.opengrade.server.data.entity.User;
import com.opengrade.server.data.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

@RestController
@RequestMapping("/test")
public class PostTestController {

    @Autowired
    UserRepository userRepository;

    @PostMapping("/post")
    public void testApi() {
        ArrayList<String> test1 = new ArrayList<>();
        ArrayList<String> test2 = new ArrayList<>();

        LocalDateTime localDateTime = LocalDateTime.now();

        HashMap<String, List<String>> testMap = new HashMap<>();
        User user1 = new User();

        test1.add("123456");
        test1.add("컴수");
        test1.add("3");
        test1.add("97");
        test1.add("A+");
        test1.add("최종선");

        test2.add("78910");
        test2.add("플밍");
        test2.add("3");
        test2.add("92");
        test2.add("A0");
        test2.add("김익수");

        testMap.put("컴수", test1);
        testMap.put("플밍", test2);

        user1.setGrade(testMap);
        user1.setId(20212227);
        user1.setSemester(1);
        user1.setYear(2021);
        user1.setTime(localDateTime);

        userRepository.save(user1);

    }

}
