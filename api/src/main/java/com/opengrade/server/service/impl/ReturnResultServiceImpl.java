package com.opengrade.server.service.impl;

import com.opengrade.server.data.dto.RankingDto;
import com.opengrade.server.data.entity.User;
import com.opengrade.server.data.repository.UserRepository;
import com.opengrade.server.service.ReturnResultService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.Comparator;
import java.util.List;

@Service
public class ReturnResultServiceImpl implements ReturnResultService {

    UserRepository userRepository;

    @Autowired
    ReturnResultServiceImpl(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    public void getAllGrade(RankingDto rankingDto, String studentId, String department) {
        int tempId = Integer.parseInt(studentId);
        User user = userRepository.getUserByStudentId(Integer.valueOf(tempId));
        rankingDto.setNickname(user.getNickname());

        if (department.equals("com")) {

            department = "컴";
            Comparator<User> comparator = new Comparator<User>() {
                @Override
                public int compare(User a, User b) {
                    return (int) (b.getComScore() - a.getComScore());
                }
            };

            List<User> allGrade = userRepository.findAll();
            //List<User> allGrade = userRepository.findAllByDepartment(department);
            allGrade.sort(comparator);
            rankingDto.setAllUsers(allGrade);
        } else if (department.equals("soft")) {

            department = "솦";
            Comparator<User> comparator = new Comparator<User>() {
                @Override
                public int compare(User a, User b) {
                    return (int) (b.getSoftScore() - a.getSoftScore());
                }
            };

            List<User> allGrade = userRepository.findAll();
            //List<User> allGrade = userRepository.findAllByDepartment(department);
            allGrade.sort(comparator);
            rankingDto.setAllUsers(allGrade);

        }

    }

    public void getApplyGrade(RankingDto rankingDto, String studentId, String department) {
        int tempId = Integer.parseInt(studentId);
        User user = userRepository.getUserByStudentId(Integer.valueOf(tempId));
        rankingDto.setNickname(user.getNickname());

        if (department.equals("com")) {

            department = "컴";
            Comparator<User> comparator = new Comparator<User>() {
                @Override
                public int compare(User a, User b) {
                    return (int) (b.getComScore() - a.getComScore());
                }
            };

            List<User> allGrade = userRepository.findAllByDepartment(department);
            allGrade.sort(comparator);
            rankingDto.setAllUsers(allGrade);
        } else if (department.equals("soft")) {

            department = "솦";
            Comparator<User> comparator = new Comparator<User>() {
                @Override
                public int compare(User a, User b) {
                    return (int) (b.getSoftScore() - a.getSoftScore());
                }
            };

            List<User> allGrade = userRepository.findAllByDepartment(department);
            allGrade.sort(comparator);
            rankingDto.setAllUsers(allGrade);

        }
    }
}
