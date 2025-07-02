import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BaseChartDirective } from 'ng2-charts';
import { Chart, ChartConfiguration, ChartType, registerables } from 'chart.js';
import { DashboardService } from '../../services/dashboard.service';
import { ConsumerShareData } from '../../models/dashboard.models';

Chart.register(...registerables);

@Component({
  selector: 'app-consumer-share',
  standalone: true,
  imports: [CommonModule, BaseChartDirective],
  templateUrl: './consumer-share.component.html',
  styleUrls: ['./consumer-share.component.scss']
})
export class ConsumerShareComponent implements OnChanges {
  @Input() analysisType = 'By City';

  data: ConsumerShareData[] = [];
  loading = false;
  error: string | null = null;

  public pieChartType: ChartType = 'pie';
  public pieChartData: ChartConfiguration['data'] = {
    datasets: [],
    labels: []
  };
  
  public pieChartOptions: ChartConfiguration['options'] = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      title: {
        display: true,
        text: 'Consumer Share by Class',
        font: { size: 16, weight: 'bold' },
        color: '#333'
      },
      legend: {
        display: true,
        position: 'right'
      }
    }
  };

  constructor(private dashboardService: DashboardService) {}

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['analysisType']) {
      this.loadData();
    }
  }

  ngOnInit(): void {
    this.loadData();
  }

  loadData(): void {
    this.loading = true;
    this.error = null;
    
    this.dashboardService.getConsumerShare(this.analysisType).subscribe({
      next: (data) => {
        this.data = data;
        this.updateChart();
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Failed to load consumer share data';
        this.loading = false;
        console.error('Error loading consumer share data:', err);
      }
    });
  }

  private updateChart(): void {
    const labels = this.data.map(d => d.classOfOwnership);
    const percentages = this.data.map(d => d.percentage);
    
    const colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'];
    
    this.pieChartData = {
      labels: labels,
      datasets: [{
        data: percentages,
        backgroundColor: colors.slice(0, labels.length),
        borderColor: colors.slice(0, labels.length),
        borderWidth: 2
      }]
    };
  }
}
