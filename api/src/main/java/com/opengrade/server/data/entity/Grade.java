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
    private Integer idx;

    @ManyToOne
    @JoinColumn(referencedColumnName = "id")
    private User id;

    @Column
    private int year;

    @Column
    private int semester;

    @Type(type = "json")
    @Column(columnDefinition = "json")
    private Map<String, Map<String, String>> grade = new HashMap<>();

    @Column
    private LocalDateTime updateTime;

}
