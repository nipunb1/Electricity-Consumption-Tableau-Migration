import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BaseChartDirective } from 'ng2-charts';
import { Chart, ChartConfiguration, ChartType, registerables } from 'chart.js';
import { DashboardService } from '../../services/dashboard.service';
import { ConsumerGrowthData } from '../../models/dashboard.models';

Chart.register(...registerables);

@Component({
  selector: 'app-consumer-growth',
  standalone: true,
  imports: [CommonModule, BaseChartDirective],
  templateUrl: './consumer-growth.component.html',
  styleUrls: ['./consumer-growth.component.scss']
})
export class ConsumerGrowthComponent implements OnChanges {
  @Input() analysisType = 'By City';
  @Input() viewMode = 'Standard';

  data: ConsumerGrowthData[] = [];
  loading = false;
  error: string | null = null;

  public lineChartType: ChartType = 'line';
  public lineChartData: ChartConfiguration['data'] = {
    datasets: [],
    labels: []
  };
  
  public lineChartOptions: ChartConfiguration['options'] = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      title: {
        display: true,
        text: 'Consumer Growth Analysis',
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
          text: 'Consumer Count',
          font: { weight: 'bold' }
        },
        beginAtZero: true
      }
    }
  };

  constructor(private dashboardService: DashboardService) {}

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['analysisType'] || changes['viewMode']) {
      this.loadData();
    }
  }

  ngOnInit(): void {
    this.loadData();
  }

  loadData(): void {
    this.loading = true;
    this.error = null;
    
    this.dashboardService.getConsumerGrowth(this.analysisType, this.viewMode).subscribe({
      next: (data) => {
        this.data = data;
        this.updateChart();
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Failed to load consumer growth data';
        this.loading = false;
        console.error('Error loading consumer growth data:', err);
      }
    });
  }

  private updateChart(): void {
    const locations = [...new Set(this.data.map(d => d.location))];
    const years = [...new Set(this.data.map(d => d.year))].sort();
    
    const datasets = locations.map((location, index) => {
      const locationData = this.data.filter(d => d.location === location);
      const chartData = years.map(year => {
        const yearData = locationData.find(d => d.year === year);
        return yearData ? yearData.consumerCount : 0;
      });
      
      const colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'];
      
      return {
        label: location,
        data: chartData,
        borderColor: colors[index % colors.length],
        backgroundColor: colors[index % colors.length] + '20',
        fill: false,
        tension: 0.1
      };
    });

    this.lineChartData = {
      labels: years.map(y => y.toString()),
      datasets: datasets
    };
  }
}
