package com.opengrade.server.service;

import org.springframework.stereotype.Service;

@Service
public interface ScrappingRequestService {


    public Boolean verifyGrade(String id);

    public String postRequest(String id, String sToken);

}
