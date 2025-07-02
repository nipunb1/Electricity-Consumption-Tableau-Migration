import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { DashboardService } from '../../services/dashboard.service';
import { ParametersData } from '../../models/dashboard.models';
import { ConsumerGrowthComponent } from '../consumer-growth/consumer-growth.component';
import { ConsumerShareComponent } from '../consumer-share/consumer-share.component';
import { PowerSalesGrowthComponent } from '../power-sales-growth/power-sales-growth.component';
import { RevenueGrowthComponent } from '../revenue-growth/revenue-growth.component';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [
    CommonModule, 
    FormsModule,
    ConsumerGrowthComponent,
    ConsumerShareComponent,
    PowerSalesGrowthComponent,
    RevenueGrowthComponent
  ],
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit {
  parameters: ParametersData | null = null;
  
  selectedConsumptionType = 'Sales per consumer';
  selectedAnalysisType = 'By City';
  selectedViewMode = 'Standard';
  
  loading = false;
  error: string | null = null;

  constructor(private dashboardService: DashboardService) {}

  ngOnInit(): void {
    this.loadParameters();
  }

  loadParameters(): void {
    this.loading = true;
    this.dashboardService.getParameters().subscribe({
      next: (data) => {
        this.parameters = data;
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Failed to load parameters';
        this.loading = false;
        console.error('Error loading parameters:', err);
      }
    });
  }

  onParameterChange(): void {
    console.log('Parameters changed:', {
      consumptionType: this.selectedConsumptionType,
      analysisType: this.selectedAnalysisType,
      viewMode: this.selectedViewMode
    });
  }
}
