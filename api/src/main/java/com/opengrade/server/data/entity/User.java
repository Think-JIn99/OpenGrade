package com.opengrade.server.data.entity;

import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import org.hibernate.annotations.Type;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Id;
import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Getter
@Setter
@NoArgsConstructor
@Entity
public class User {

    @Id
    private Integer id;

    @Column
    private int year;

    @Column
    private int semester;

    @Type(type = "json")
    @Column(columnDefinition = "json")
    private Map<String, List<String>> grade = new HashMap<>();

    @Column
    private LocalDateTime time;

}
