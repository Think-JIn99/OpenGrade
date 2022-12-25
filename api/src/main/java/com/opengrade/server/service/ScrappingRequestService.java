package com.opengrade.server.service;

import org.springframework.stereotype.Service;

@Service
public interface ScrappingRequestService {


    public Boolean verifyGrade(String id);

    public void postRequest(String id, String sToken);

}
