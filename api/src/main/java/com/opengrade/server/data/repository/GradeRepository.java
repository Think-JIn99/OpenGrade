package com.opengrade.server.data.repository;

import com.opengrade.server.data.entity.Grade;
import org.springframework.data.jpa.repository.JpaRepository;

public interface GradeRepository extends JpaRepository<Grade, String> {
}
