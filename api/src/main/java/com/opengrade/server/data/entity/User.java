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
    private Integer id;

    @Column
    private int currentYear;

    @Column
    private int currentSemester;

    @Column
    private String department;

    @Column
    private LocalDateTime updateTime;

}
