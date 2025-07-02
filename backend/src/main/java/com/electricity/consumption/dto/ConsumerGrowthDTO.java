package com.electricity.consumption.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class ConsumerGrowthDTO {
    private String location;
    private Integer year;
    private Double consumerCount;
    private Double salesValue;
    private String classOfOwnership;
}
