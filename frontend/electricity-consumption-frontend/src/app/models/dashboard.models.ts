export interface ConsumerGrowthData {
  location: string;
  year: number;
  consumerCount: number;
  salesValue: number;
  classOfOwnership: string;
}

export interface ConsumerShareData {
  classOfOwnership: string;
  location: string;
  percentage: number;
  consumerCount: number;
  revenue: number;
}

export interface PowerSalesGrowthData {
  location: string;
  year: number;
  salesPerConsumer: number;
  totalSales: number;
  growthRate: number;
}

export interface RevenueGrowthData {
  location: string;
  year: number;
  revenue: number;
  growthRate: number;
  classOfOwnership: string;
}

export interface ParametersData {
  consumptionTypes: string[];
  analysisTypes: string[];
  viewModes: string[];
  states: string[];
  cities: string[];
  classOfOwnership: string[];
  years: number[];
}
