import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BaseChartDirective } from 'ng2-charts';
import { Chart, ChartConfiguration, ChartType, registerables } from 'chart.js';
import { DashboardService } from '../../services/dashboard.service';
import { PowerSalesGrowthData } from '../../models/dashboard.models';

Chart.register(...registerables);

@Component({
  selector: 'app-power-sales-growth',
  standalone: true,
  imports: [CommonModule, BaseChartDirective],
  templateUrl: './power-sales-growth.component.html',
  styleUrls: ['./power-sales-growth.component.scss']
})
export class PowerSalesGrowthComponent implements OnChanges {
  @Input() consumptionType = 'Sales per consumer';
  @Input() viewMode = 'Standard';

  data: PowerSalesGrowthData[] = [];
  loading = false;
  error: string | null = null;

  public barChartType: ChartType = 'bar';
  public barChartData: ChartConfiguration['data'] = {
    datasets: [],
    labels: []
  };
  
  public barChartOptions: ChartConfiguration['options'] = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      title: {
        display: true,
        text: 'Power Sales Growth',
        font: { size: 16, weight: 'bold' },
        color: '#333'
      },
      legend: {
        display: true,
        position: 'top'
      }
    },
    scales: {
      x: {
        title: {
          display: true,
          text: 'Year',
          font: { weight: 'bold' }
        }
      },
      y: {
        title: {
          display: true,
          text: this.consumptionType === 'Sales per consumer' ? 'Sales per Consumer' : 'Total Sales',
          font: { weight: 'bold' }
        },
        beginAtZero: true
      }
    }
  };

  constructor(private dashboardService: DashboardService) {}

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['consumptionType'] || changes['viewMode']) {
      this.loadData();
      this.updateYAxisTitle();
    }
  }

  ngOnInit(): void {
    this.loadData();
  }

  loadData(): void {
    this.loading = true;
    this.error = null;
    
    this.dashboardService.getPowerSalesGrowth(this.consumptionType, this.viewMode).subscribe({
      next: (data) => {
        this.data = data;
        this.updateChart();
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Failed to load power sales growth data';
        this.loading = false;
        console.error('Error loading power sales growth data:', err);
      }
    });
  }

  private updateYAxisTitle(): void {
    if (this.barChartOptions?.scales?.['y']) {
      const yScale = this.barChartOptions.scales['y'] as any;
      if (yScale.title) {
        yScale.title.text = this.consumptionType === 'Sales per consumer' ? 'Sales per Consumer' : 'Total Sales';
      }
    }
  }

  private updateChart(): void {
    const locations = [...new Set(this.data.map(d => d.location))];
    const years = [...new Set(this.data.map(d => d.year))].sort();
    
    const datasets = locations.map((location, index) => {
      const locationData = this.data.filter(d => d.location === location);
      const chartData = years.map(year => {
        const yearData = locationData.find(d => d.year === year);
        return yearData ? 
          (this.consumptionType === 'Sales per consumer' ? yearData.salesPerConsumer : yearData.totalSales) : 0;
      });
      
      const colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'];
      
      return {
        label: location,
        data: chartData,
        backgroundColor: colors[index % colors.length] + '80',
        borderColor: colors[index % colors.length],
        borderWidth: 2
      };
    });

    this.barChartData = {
      labels: years.map(y => y.toString()),
      datasets: datasets
    };
  }
}
