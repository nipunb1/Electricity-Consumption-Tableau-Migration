package com.electricity.consumption.entity;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import javax.persistence.*;
import javax.validation.constraints.NotNull;

@Entity
@Table(name = "electricity_consumption")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class ElectricityConsumption {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(name = "entity")
    @NotNull
    private String entity;
    
    @Column(name = "city")
    @NotNull
    private String city;
    
    @Column(name = "state")
    @NotNull
    private String state;
    
    @Column(name = "ownership_class")
    @NotNull
    private String classOfOwnership;
    
    @Column(name = "consumption_year")
    @NotNull
    private Integer year;
    
    @Column(name = "sales_megawatthours")
    @NotNull
    private Integer salesMegawatthours;
    
    @Column(name = "number_of_consumers")
    @NotNull
    private Integer numberOfConsumers;
    
    @Column(name = "revenue_thousand_dollars")
    @NotNull
    private Double revenueThousandDollars;
    
    @Column(name = "average_retail_price_cents_kwh")
    @NotNull
    private Double averageRetailPriceCentsKwh;
    
    public Long getId() { return id; }
    public String getEntity() { return entity; }
    public String getCity() { return city; }
    public String getState() { return state; }
    public String getClassOfOwnership() { return classOfOwnership; }
    public Integer getYear() { return year; }
    public Integer getSalesMegawatthours() { return salesMegawatthours; }
    public Integer getNumberOfConsumers() { return numberOfConsumers; }
    public Double getRevenueThousandDollars() { return revenueThousandDollars; }
    public Double getAverageRetailPriceCentsKwh() { return averageRetailPriceCentsKwh; }
}
