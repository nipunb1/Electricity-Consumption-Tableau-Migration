package com.electricity.consumption.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class RevenueGrowthDTO {
    private String location;
    private Integer year;
    private Double revenue;
    private Double growthRate;
    private String classOfOwnership;
}
