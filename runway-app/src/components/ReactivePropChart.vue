<script lang="ts">
import { defineComponent } from 'vue'
import type { PropType } from 'vue'
import { Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
} from 'chart.js'

import type { Plugin, ChartData, DefaultDataPoint } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

export default defineComponent({
  name: 'ReactiveChart',
  components: {
    Bar
  },
  props: {
    chartId: {
      type: String,
      default: 'bar-chart'
    },
    width: {
      type: Number,
      default: 400
    },
    height: {
      type: Number,
      default: 400
    },
    cssClasses: {
      default: '',
      type: String
    },
    styles: {
      type: Object as PropType<Partial<CSSStyleDeclaration>>,
      default: () => {}
    },
    plugins: {
      type: Array as PropType<Plugin<'bar'>[]>,
      default: () => []
    }
  },
  data() {
    return {
      chartData: {} as ChartData<'bar', DefaultDataPoint<'bar'>, unknown>
    }
  },
  methods: {
    fillData() {
      const updatedChartData = {
        labels: [
          'January' + this.getRandomInt(),
          'February',
          'March',
          'April',
          'May',
          'June',
          'July',
          'August',
          'September',
          'October',
          'November',
          'December'
        ],
        datasets: [
          {
            label: 'Data One',
            backgroundColor: '#f87979',
            data: [
              this.getRandomInt(),
              this.getRandomInt(),
              this.getRandomInt(),
              this.getRandomInt(),
              this.getRandomInt(),
              this.getRandomInt(),
              this.getRandomInt(),
              this.getRandomInt(),
              this.getRandomInt(),
              this.getRandomInt(),
              this.getRandomInt(),
              this.getRandomInt()
            ]
          }
        ]
      }

      this.chartData = { ...updatedChartData }
    },
    getRandomInt() {
      return Math.floor(Math.random() * (50 - 5 + 1)) + 5
    }
  },
  mounted() {
    this.fillData();
    setInterval(() => { this.fillData() }, 2000);
  }
})
</script>

<template>
  <Bar
    :chart-data="chartData"
    :chart-options='{
      responsive: true,
      maintainAspectRatio: false
    }'
    :chart-id="chartId"
    :width="width"
    :height="height"
    :css-classes="cssClasses"
    :styles="styles"
    :plugins="plugins"
    />
</template>