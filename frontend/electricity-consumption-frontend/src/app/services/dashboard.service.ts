import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { 
  ConsumerGrowthData, 
  ConsumerShareData, 
  PowerSalesGrowthData, 
  RevenueGrowthData, 
  ParametersData 
} from '../models/dashboard.models';

@Injectable({
  providedIn: 'root'
})
export class DashboardService {
  private apiUrl = 'http://localhost:8080/api/dashboard';

  constructor(private http: HttpClient) {}

  getConsumerGrowth(analysisType: string, viewMode: string): Observable<ConsumerGrowthData[]> {
    const params = new HttpParams()
      .set('analysisType', analysisType)
      .set('viewMode', viewMode);
    return this.http.get<ConsumerGrowthData[]>(`${this.apiUrl}/consumer-growth`, { params });
  }

  getConsumerShare(analysisType: string): Observable<ConsumerShareData[]> {
    const params = new HttpParams().set('analysisType', analysisType);
    return this.http.get<ConsumerShareData[]>(`${this.apiUrl}/consumer-share`, { params });
  }

  getPowerSalesGrowth(consumptionType: string, viewMode: string): Observable<PowerSalesGrowthData[]> {
    const params = new HttpParams()
      .set('consumptionType', consumptionType)
      .set('viewMode', viewMode);
    return this.http.get<PowerSalesGrowthData[]>(`${this.apiUrl}/power-sales-growth`, { params });
  }

  getRevenueGrowth(): Observable<RevenueGrowthData[]> {
    return this.http.get<RevenueGrowthData[]>(`${this.apiUrl}/revenue-growth`);
  }

  getParameters(): Observable<ParametersData> {
    return this.http.get<ParametersData>(`${this.apiUrl}/parameters`);
  }
}
