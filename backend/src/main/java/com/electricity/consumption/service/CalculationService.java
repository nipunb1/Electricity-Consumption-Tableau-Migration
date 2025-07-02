package com.electricity.consumption.service;

import com.electricity.consumption.entity.ElectricityConsumption;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@Slf4j
public class CalculationService {
    
    public Double calculateAverageYearlySalesStandard(List<ElectricityConsumption> data) {
        log.debug("Calculating average yearly sales (standard) for {} records", data.size());
        if (data.isEmpty()) {
            return 0.0;
        }
        
        double totalSales = data.stream().mapToDouble(ElectricityConsumption::getSalesMegawatthours).sum();
        double totalConsumers = data.stream().mapToDouble(ElectricityConsumption::getNumberOfConsumers).sum();
        
        if (totalConsumers == 0) {
            return 0.0;
        }
        
        return (totalSales * 100 / totalConsumers) / 12;
    }
    
    public Double calculateAverageYearlySalesMWh(List<ElectricityConsumption> data) {
        log.debug("Calculating average yearly sales (MWh) for {} records", data.size());
        if (data.isEmpty()) {
            return 0.0;
        }
        
        double totalSalesMWh = data.stream().mapToDouble(e -> calculateElectricitySalesMWh(e.getSalesMegawatthours())).sum();
        double totalConsumers = data.stream().mapToDouble(ElectricityConsumption::getNumberOfConsumers).sum();
        
        if (totalConsumers == 0) {
            return 0.0;
        }
        
        return (totalSalesMWh * 100 / totalConsumers) / 12;
    }
    
    public Double calculateElectricitySalesMWh(Integer salesMegawatthours) {
        return salesMegawatthours / 1000.0;
    }
    
    public Double calculateRevenue(Double revenueThousandDollars) {
        return revenueThousandDollars * 100;
    }
    
    public Double calculateConsumerCount(List<ElectricityConsumption> data, String viewMode) {
        if (data.isEmpty()) {
            return 0.0;
        }
        
        double totalConsumers = data.stream().mapToDouble(ElectricityConsumption::getNumberOfConsumers).sum();
        long distinctYears = data.stream().map(ElectricityConsumption::getYear).distinct().count();
        
        if (distinctYears == 0) {
            return 0.0;
        }
        
        if ("Thousands".equals(viewMode)) {
            return totalConsumers / (distinctYears * 1000);
        }
        return totalConsumers / distinctYears;
    }
    
    public Double calculateUnifiedSalesDimension(List<ElectricityConsumption> data, 
                                               String consumptionType, String viewMode) {
        log.debug("Calculating unified sales dimension: type={}, mode={}", consumptionType, viewMode);
        
        if (data.isEmpty()) {
            return 0.0;
        }
        
        if ("Standard".equals(viewMode) || "Thousands".equals(viewMode)) {
            if ("Sales per consumer".equals(consumptionType)) {
                return calculateAverageYearlySalesStandard(data);
            } else {
                return data.stream().mapToDouble(ElectricityConsumption::getSalesMegawatthours).sum();
            }
        } else if ("MWh".equals(viewMode)) {
            if ("Sales per consumer".equals(consumptionType)) {
                return calculateAverageYearlySalesMWh(data);
            } else {
                return data.stream().mapToDouble(e -> calculateElectricitySalesMWh(e.getSalesMegawatthours())).sum();
            }
        }
        
        return 0.0;
    }
    
    public Double calculateTotalRevenue(List<ElectricityConsumption> data) {
        return data.stream().mapToDouble(e -> calculateRevenue(e.getRevenueThousandDollars())).sum();
    }
    
    public Double calculateAverageRetailPrice(List<ElectricityConsumption> data) {
        if (data.isEmpty()) {
            return 0.0;
        }
        
        return data.stream().mapToDouble(ElectricityConsumption::getAverageRetailPriceCentsKwh).average().orElse(0.0);
    }
}
