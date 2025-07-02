package com.electricity.consumption.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class ConsumerShareDTO {
    private String classOfOwnership;
    private String location;
    private Double percentage;
    private Double totalConsumers;
    private Double revenue;
}
