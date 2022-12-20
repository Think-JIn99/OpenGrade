package com.opengrade.server.service.impl;

import com.opengrade.server.data.dto.LoginResponseDto;
import com.opengrade.server.data.entity.Grade;
import com.opengrade.server.data.entity.User;
import com.opengrade.server.data.repository.GradeRepository;
import com.opengrade.server.data.repository.UserRepository;
import com.opengrade.server.service.LoginService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.RestTemplate;

import java.time.LocalDateTime;

@Service
public class LoginServiceImpl implements LoginService {

    @Autowired
    GradeRepository gradeRepository;

    @Autowired
    UserRepository userRepository;

    public String tryLogin(String id, String pw) {

        String loginUrl = "https://smartid.ssu.ac.kr/Symtra_sso/smln_pcs.asp";

        // request의 body
        MultiValueMap<String, String> params = new LinkedMultiValueMap<>();

        params.add("in_tp_bit", "0");
        params.add("rqst_caus_cd", "03");
        params.add("userid", id);
        params.add("pwd", pw);

        //헤더
        //생성은 하고 add~ 안해도 됨
        HttpHeaders headers = new HttpHeaders();

        headers.add("referer", loginUrl);
        headers.add("user-agent", "");

        //바디와 헤더 합치기
        HttpEntity<MultiValueMap<String, String>> entity = new HttpEntity<>(params, headers);

        RestTemplate restTemplate = new RestTemplate();

        ResponseEntity<String> response = restTemplate.exchange(
                loginUrl,
                HttpMethod.POST,
                entity,
                String.class
        );

        return response.getHeaders().get("Set-Cookie").get(2);
    }

    public void isValidateLogin(String returnToken, LoginResponseDto loginResponseDto) {

        if (returnToken.substring(0,7).equals("sToken=")) {
            loginResponseDto.setSToken(returnToken.substring(7, returnToken.indexOf(";")));
            loginResponseDto.setLoginValidate(Boolean.TRUE);
        }
        else {
            loginResponseDto.setLoginValidate(Boolean.FALSE);
        }
    }

    public void loadUsaint(LoginResponseDto loginResponseDto) {
        String sapTokenUrl = "https://saint.ssu.ac.kr/webSSO/sso.jsp?sToken="+loginResponseDto.getSToken();

        HttpHeaders headers = new HttpHeaders();

        headers.add("Cookie", "sToken=" + loginResponseDto.getSToken());

        MultiValueMap<String, String> params = new LinkedMultiValueMap<>();

        HttpEntity<MultiValueMap<String, String>> entity = new HttpEntity<>(params, headers);

        RestTemplate restTemplate = new RestTemplate();

        ResponseEntity<String> response = restTemplate.exchange(
                sapTokenUrl,
                HttpMethod.GET,
                entity,
                String.class
        );

        HttpHeaders loginHeaders = new HttpHeaders();

        String returnMYSAPASS02 = response.getHeaders().get("Set-Cookie").get(1);

        loginHeaders.add("Cookie", returnMYSAPASS02.substring(0, returnMYSAPASS02.indexOf(";")));

        HttpEntity<MultiValueMap<String, String>> loginHttpEntity = new HttpEntity<>(params, loginHeaders);

        ResponseEntity<String> LoginResponse = restTemplate.exchange(
                "https://saint.ssu.ac.kr/webSSUMain/main_student.jsp",
                HttpMethod.GET,
                loginHttpEntity,
                String.class
        );

        if(LoginResponse.toString().contains("융합특성화자유전공학부")) {
            loginResponseDto.setDepartment("융합특성화자유전공학부");
        }
        else {
            loginResponseDto.setDepartment("");
        }
    }

    public void generateNickname(LoginResponseDto loginResponseDto) {

    }

    public void saveUser(String id, String tempSemester, String tempYear, String tempDepart) {
        User user = new User();
        LocalDateTime localDateTime = LocalDateTime.now();

        user.setStudentId(id);
        user.setCurrentYear(tempYear);
        user.setCurrentSemester(tempSemester);
        user.setDepartment(tempDepart);
        user.setUpdateTime(localDateTime);

        userRepository.save(user);
    }

    public void searchGrade(LoginResponseDto loginResponseDto, String id) {
//        User user = userRepository.getUserByStudentId(id);
//        Grade grade = gradeRepository.getGradeByStudentIdAndSemesterAndYear(id, user.getCurrentSemester(), user.getCurrentYear());
//        if (grade.getGrade().isEmpty()){
//            //셀레니움에 post보내서 성적 받아오기
//        }
//        loginResponseDto.setGrade(grade);
    }
}
