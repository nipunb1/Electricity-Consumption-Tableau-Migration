package com.electricity.consumption.repository;

import com.electricity.consumption.entity.ElectricityConsumption;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ElectricityConsumptionRepository extends JpaRepository<ElectricityConsumption, Long> {
    
    List<ElectricityConsumption> findByYear(Integer year);
    
    List<ElectricityConsumption> findByState(String state);
    
    List<ElectricityConsumption> findByCity(String city);
    
    List<ElectricityConsumption> findByClassOfOwnership(String classOfOwnership);
    
    List<ElectricityConsumption> findByYearBetween(Integer startYear, Integer endYear);
    
    @Query("SELECT DISTINCT e.year FROM ElectricityConsumption e ORDER BY e.year")
    List<Integer> findDistinctYears();
    
    @Query("SELECT DISTINCT e.state FROM ElectricityConsumption e ORDER BY e.state")
    List<String> findDistinctStates();
    
    @Query("SELECT DISTINCT e.city FROM ElectricityConsumption e ORDER BY e.city")
    List<String> findDistinctCities();
    
    @Query("SELECT DISTINCT e.classOfOwnership FROM ElectricityConsumption e ORDER BY e.classOfOwnership")
    List<String> findDistinctClassOfOwnership();
}
