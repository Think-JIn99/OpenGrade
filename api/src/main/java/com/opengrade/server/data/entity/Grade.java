package com.opengrade.server.data.entity;

import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import org.hibernate.annotations.Type;

import javax.persistence.*;
import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.Map;

@Getter
@Setter
@NoArgsConstructor
@Entity
public class Grade {

    @Id
    @GeneratedValue(strategy=GenerationType.IDENTITY)
    private Integer idx;

    @ManyToOne
    @JoinColumn(referencedColumnName = "student_id", name = "student_id")
    private User studentId;

    @Column
    private String year;

    @Column
    private String semester;

    @Type(type = "json")
    @Column(columnDefinition = "json")
    private Map<String, Map<String, String>> grade = new HashMap<>();

    @Column
    private LocalDateTime updateTime;

}
