package com.electricity.consumption.controller;

import com.electricity.consumption.dto.*;
import com.electricity.consumption.service.ElectricityConsumptionService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/dashboard")
@CrossOrigin(origins = "http://localhost:4200")
@Slf4j
public class DashboardController {
    
    @Autowired
    private ElectricityConsumptionService service;
    
    @GetMapping("/consumer-growth")
    public ResponseEntity<List<ConsumerGrowthDTO>> getConsumerGrowth(
        @RequestParam(defaultValue = "By City") String analysisType,
        @RequestParam(defaultValue = "Standard") String viewMode) {
        
        log.info("Getting consumer growth data: analysisType={}, viewMode={}", analysisType, viewMode);
        List<ConsumerGrowthDTO> data = service.getConsumerGrowthData(analysisType, viewMode);
        return ResponseEntity.ok(data);
    }
    
    @GetMapping("/consumer-share")
    public ResponseEntity<List<ConsumerShareDTO>> getConsumerShare(
        @RequestParam(defaultValue = "By City") String analysisType) {
        
        log.info("Getting consumer share data: analysisType={}", analysisType);
        List<ConsumerShareDTO> data = service.getConsumerShareData(analysisType);
        return ResponseEntity.ok(data);
    }
    
    @GetMapping("/power-sales-growth")
    public ResponseEntity<List<PowerSalesGrowthDTO>> getPowerSalesGrowth(
        @RequestParam(defaultValue = "Sales per consumer") String consumptionType,
        @RequestParam(defaultValue = "Standard") String viewMode) {
        
        log.info("Getting power sales growth: consumptionType={}, viewMode={}", consumptionType, viewMode);
        List<PowerSalesGrowthDTO> data = service.getPowerSalesGrowthData(consumptionType, viewMode);
        return ResponseEntity.ok(data);
    }
    
    @GetMapping("/revenue-growth")
    public ResponseEntity<List<RevenueGrowthDTO>> getRevenueGrowth() {
        log.info("Getting revenue growth data");
        List<RevenueGrowthDTO> data = service.getRevenueGrowthData();
        return ResponseEntity.ok(data);
    }
    
    @GetMapping("/parameters")
    public ResponseEntity<ParametersDTO> getParameters() {
        log.info("Getting parameters data");
        ParametersDTO parameters = service.getParameters();
        return ResponseEntity.ok(parameters);
    }
}
