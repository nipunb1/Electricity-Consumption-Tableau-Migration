package com.electricity.consumption.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class ParametersDTO {
    private List<String> consumptionTypes;
    private List<String> analysisTypes;
    private List<String> viewModes;
    private List<String> states;
    private List<String> cities;
    private List<String> classOfOwnership;
    private List<Integer> years;
}
