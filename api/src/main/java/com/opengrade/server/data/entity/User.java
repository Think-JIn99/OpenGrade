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
    @Column(name = "studentid", nullable = false)
    private Integer studentId;

    @Column
    private Integer phl;

    @Column
    private Integer math;

    @Column(name = "bigdata")
    private Integer bigData;

    @Column
    private Integer programming;

    @Column(name = "businessmanagement")
    private Integer businessManagement;

    @Column(length = 1)
    private String department;

    @Column(name = "com_score", precision = 3, scale = 2)
    private Float comScore;

    @Column(name = "soft_score", precision = 3, scale = 2)
    private Float softScore;

    @Column(name = "updatedate")
    private LocalDateTime updateDate;

    @Column(name = "nickname")
    private String nickname;

}

