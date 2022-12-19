package com.opengrade.server.data.entity;

import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Id;
import java.time.LocalDateTime;

@Getter
@Setter
@NoArgsConstructor
@Entity
public class User {

    @Id
    @Column(name = "student_id")
    private String studentId;

    @Column
    private String currentYear;

    @Column
    private String currentSemester;

    @Column
    private String department;

    @Column
    private String apply;

    @Column
    private String comScore;

    @Column
    private String softScore;

    @Column
    private LocalDateTime updateTime;

}

