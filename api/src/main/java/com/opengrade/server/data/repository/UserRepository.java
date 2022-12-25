package com.opengrade.server.data.repository;

import com.opengrade.server.data.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface UserRepository extends JpaRepository<User, String> {
    User getUserByStudentId(Integer studentId);
    List<User> findAllByDepartment(String department);
    List<User> findAll();
}
