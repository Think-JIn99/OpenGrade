package com.opengrade.server.service.impl;

import com.opengrade.server.service.ScrappingRequestService;
import org.springframework.stereotype.Service;

@Service
public class ScrappingRequestServiceImpl implements ScrappingRequestService {

    public Boolean verifyGrade(String id) {
        return true;
    }

    public void postRequest(String id, String sToken) {

    }
}
