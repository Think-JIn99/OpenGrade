package com.opengrade.server.data.dto;


import com.opengrade.server.data.entity.User;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.util.List;

@Getter
@Setter
@NoArgsConstructor
public class RankingDto {
    private String nickname;
    private List<User> allUsers;

}
