package com.opengrade.server.data.entity;

import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Id;

@Getter
@Setter
@NoArgsConstructor
@Entity
public class Grade {
    @Id
    private String nickname;

    // 컴0 솦1 ??
    @Column(nullable = false)
    private Boolean department;

    @Column(nullable = false)
    private int PHL_grade;

    @Column(nullable = false)
    private int math_grade;

    @Column(nullable = false)
    private int bigData_grade;

    @Column(nullable = false)
    private int programing_grade;

}
