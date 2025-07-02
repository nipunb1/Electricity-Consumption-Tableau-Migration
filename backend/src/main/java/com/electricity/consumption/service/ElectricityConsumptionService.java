package com.electricity.consumption.service;

import com.electricity.consumption.dto.*;
import com.electricity.consumption.entity.ElectricityConsumption;
import com.electricity.consumption.repository.ElectricityConsumptionRepository;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.*;
import java.util.stream.Collectors;

@Service
@Slf4j
public class ElectricityConsumptionService {
    
    @Autowired
    private ElectricityConsumptionRepository repository;
    
    @Autowired
    private CalculationService calculationService;
    
    public List<ConsumerGrowthDTO> getConsumerGrowthData(String analysisType, String viewMode) {
        log.info("Getting consumer growth data: analysisType={}, viewMode={}", analysisType, viewMode);
        
        List<ElectricityConsumption> allData = repository.findAll();
        List<ConsumerGrowthDTO> result = new ArrayList<>();
        
        Map<String, Map<Integer, List<ElectricityConsumption>>> groupedData;
        
        if ("By City".equals(analysisType)) {
            groupedData = allData.stream()
                .collect(Collectors.groupingBy(
                    ElectricityConsumption::getCity,
                    Collectors.groupingBy(ElectricityConsumption::getYear)
                ));
        } else {
            groupedData = allData.stream()
                .collect(Collectors.groupingBy(
                    ElectricityConsumption::getState,
                    Collectors.groupingBy(ElectricityConsumption::getYear)
                ));
        }
        
        for (Map.Entry<String, Map<Integer, List<ElectricityConsumption>>> locationEntry : groupedData.entrySet()) {
            String location = locationEntry.getKey();
            
            for (Map.Entry<Integer, List<ElectricityConsumption>> yearEntry : locationEntry.getValue().entrySet()) {
                Integer year = yearEntry.getKey();
                List<ElectricityConsumption> yearData = yearEntry.getValue();
                
                Double consumerCount = calculationService.calculateConsumerCount(yearData, viewMode);
                Double salesValue = calculationService.calculateUnifiedSalesDimension(yearData, "Electricity Sales", viewMode);
                
                result.add(new ConsumerGrowthDTO(location, year, consumerCount, salesValue, "All"));
            }
        }
        
        result.sort(Comparator.comparing(ConsumerGrowthDTO::getLocation).thenComparing(ConsumerGrowthDTO::getYear));
        log.debug("Generated {} consumer growth records", result.size());
        
        return result;
    }
    
    public List<ConsumerShareDTO> getConsumerShareData(String analysisType) {
        log.info("Getting consumer share data: analysisType={}", analysisType);
        
        List<ElectricityConsumption> allData = repository.findAll();
        List<ConsumerShareDTO> result = new ArrayList<>();
        
        Map<String, Map<String, List<ElectricityConsumption>>> groupedData;
        
        if ("By City".equals(analysisType)) {
            groupedData = allData.stream()
                .collect(Collectors.groupingBy(
                    ElectricityConsumption::getCity,
                    Collectors.groupingBy(ElectricityConsumption::getClassOfOwnership)
                ));
        } else {
            groupedData = allData.stream()
                .collect(Collectors.groupingBy(
                    ElectricityConsumption::getState,
                    Collectors.groupingBy(ElectricityConsumption::getClassOfOwnership)
                ));
        }
        
        for (Map.Entry<String, Map<String, List<ElectricityConsumption>>> locationEntry : groupedData.entrySet()) {
            String location = locationEntry.getKey();
            Map<String, List<ElectricityConsumption>> classData = locationEntry.getValue();
            
            double totalConsumersInLocation = classData.values().stream()
                .flatMap(List::stream)
                .mapToDouble(ElectricityConsumption::getNumberOfConsumers)
                .sum();
            
            for (Map.Entry<String, List<ElectricityConsumption>> classEntry : classData.entrySet()) {
                String classOfOwnership = classEntry.getKey();
                List<ElectricityConsumption> classRecords = classEntry.getValue();
                
                double classConsumers = classRecords.stream()
                    .mapToDouble(ElectricityConsumption::getNumberOfConsumers)
                    .sum();
                
                double percentage = totalConsumersInLocation > 0 ? (classConsumers / totalConsumersInLocation) * 100 : 0;
                double revenue = calculationService.calculateTotalRevenue(classRecords);
                
                result.add(new ConsumerShareDTO(classOfOwnership, location, percentage, classConsumers, revenue));
            }
        }
        
        result.sort(Comparator.comparing(ConsumerShareDTO::getLocation).thenComparing(ConsumerShareDTO::getClassOfOwnership));
        log.debug("Generated {} consumer share records", result.size());
        
        return result;
    }
    
    public List<PowerSalesGrowthDTO> getPowerSalesGrowthData(String consumptionType, String viewMode) {
        log.info("Getting power sales growth: consumptionType={}, viewMode={}", consumptionType, viewMode);
        
        List<ElectricityConsumption> allData = repository.findAll();
        List<PowerSalesGrowthDTO> result = new ArrayList<>();
        
        Map<String, Map<Integer, List<ElectricityConsumption>>> groupedData = allData.stream()
            .collect(Collectors.groupingBy(
                ElectricityConsumption::getCity,
                Collectors.groupingBy(ElectricityConsumption::getYear)
            ));
        
        for (Map.Entry<String, Map<Integer, List<ElectricityConsumption>>> locationEntry : groupedData.entrySet()) {
            String location = locationEntry.getKey();
            Map<Integer, List<ElectricityConsumption>> yearData = locationEntry.getValue();
            
            List<Integer> sortedYears = yearData.keySet().stream().sorted().collect(Collectors.toList());
            
            for (int i = 0; i < sortedYears.size(); i++) {
                Integer year = sortedYears.get(i);
                List<ElectricityConsumption> currentYearData = yearData.get(year);
                
                Double salesPerConsumer = calculationService.calculateUnifiedSalesDimension(currentYearData, "Sales per consumer", viewMode);
                Double totalSales = calculationService.calculateUnifiedSalesDimension(currentYearData, "Electricity Sales", viewMode);
                
                Double growthRate = 0.0;
                if (i > 0) {
                    Integer previousYear = sortedYears.get(i - 1);
                    List<ElectricityConsumption> previousYearData = yearData.get(previousYear);
                    Double previousSales = calculationService.calculateUnifiedSalesDimension(previousYearData, consumptionType, viewMode);
                    
                    if (previousSales > 0) {
                        Double currentSales = calculationService.calculateUnifiedSalesDimension(currentYearData, consumptionType, viewMode);
                        growthRate = ((currentSales - previousSales) / previousSales) * 100;
                    }
                }
                
                result.add(new PowerSalesGrowthDTO(location, year, salesPerConsumer, totalSales, growthRate));
            }
        }
        
        result.sort(Comparator.comparing(PowerSalesGrowthDTO::getLocation).thenComparing(PowerSalesGrowthDTO::getYear));
        log.debug("Generated {} power sales growth records", result.size());
        
        return result;
    }
    
    public List<RevenueGrowthDTO> getRevenueGrowthData() {
        log.info("Getting revenue growth data");
        
        List<ElectricityConsumption> allData = repository.findAll();
        List<RevenueGrowthDTO> result = new ArrayList<>();
        
        Map<String, Map<Integer, Map<String, List<ElectricityConsumption>>>> groupedData = allData.stream()
            .collect(Collectors.groupingBy(
                ElectricityConsumption::getCity,
                Collectors.groupingBy(
                    ElectricityConsumption::getYear,
                    Collectors.groupingBy(ElectricityConsumption::getClassOfOwnership)
                )
            ));
        
        for (Map.Entry<String, Map<Integer, Map<String, List<ElectricityConsumption>>>> locationEntry : groupedData.entrySet()) {
            String location = locationEntry.getKey();
            Map<Integer, Map<String, List<ElectricityConsumption>>> yearData = locationEntry.getValue();
            
            List<Integer> sortedYears = yearData.keySet().stream().sorted().collect(Collectors.toList());
            
            for (int i = 0; i < sortedYears.size(); i++) {
                Integer year = sortedYears.get(i);
                Map<String, List<ElectricityConsumption>> classData = yearData.get(year);
                
                for (Map.Entry<String, List<ElectricityConsumption>> classEntry : classData.entrySet()) {
                    String classOfOwnership = classEntry.getKey();
                    List<ElectricityConsumption> currentYearClassData = classEntry.getValue();
                    
                    Double revenue = calculationService.calculateTotalRevenue(currentYearClassData);
                    
                    Double growthRate = 0.0;
                    if (i > 0) {
                        Integer previousYear = sortedYears.get(i - 1);
                        List<ElectricityConsumption> previousYearClassData = yearData.get(previousYear).get(classOfOwnership);
                        
                        if (previousYearClassData != null && !previousYearClassData.isEmpty()) {
                            Double previousRevenue = calculationService.calculateTotalRevenue(previousYearClassData);
                            if (previousRevenue > 0) {
                                growthRate = ((revenue - previousRevenue) / previousRevenue) * 100;
                            }
                        }
                    }
                    
                    result.add(new RevenueGrowthDTO(location, year, revenue, growthRate, classOfOwnership));
                }
            }
        }
        
        result.sort(Comparator.comparing(RevenueGrowthDTO::getLocation)
            .thenComparing(RevenueGrowthDTO::getYear)
            .thenComparing(RevenueGrowthDTO::getClassOfOwnership));
        log.debug("Generated {} revenue growth records", result.size());
        
        return result;
    }
    
    public ParametersDTO getParameters() {
        log.info("Getting parameters data");
        
        ParametersDTO parameters = new ParametersDTO();
        parameters.setConsumptionTypes(Arrays.asList("Sales per consumer", "Electricity Sales"));
        parameters.setAnalysisTypes(Arrays.asList("By City", "By State"));
        parameters.setViewModes(Arrays.asList("Standard", "Thousands", "MWh"));
        parameters.setStates(repository.findDistinctStates());
        parameters.setCities(repository.findDistinctCities());
        parameters.setClassOfOwnership(repository.findDistinctClassOfOwnership());
        parameters.setYears(repository.findDistinctYears());
        
        return parameters;
    }
}
