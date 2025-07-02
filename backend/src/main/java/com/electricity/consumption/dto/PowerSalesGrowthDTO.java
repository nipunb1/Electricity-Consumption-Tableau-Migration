package com.electricity.consumption.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class PowerSalesGrowthDTO {
    private String location;
    private Integer year;
    private Double salesPerConsumer;
    private Double totalSales;
    private Double growthRate;
}
