package com.opengrade.server.data.repository;

import com.opengrade.server.data.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;

public interface UserRepository extends JpaRepository<User, String> {
    User getUserByStudentId(Integer studentId);
}
