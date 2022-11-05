<script setup lang="ts">
import { ref, onMounted } from 'vue'
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

export interface ChartProps {
  chartId?: string,
  width?: number,
  height?: number,
  cssClasses?: string,
  styles?: unknown,
  plugins?: unknown
}

const props = withDefaults(defineProps<ChartProps>(), {
  chartId: 'bar-chart',
  width: 400,
  height: 400,
  cssClasses: '',
  styles: () => {},
  plugins: () => {}
})

let chartData = ref({} as ChartData<'bar', DefaultDataPoint<'bar'>, unknown>)

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

function fillData() {
  const updatedChartData = {
    labels: [
      'January' + getRandomInt(),
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
          getRandomInt(),
          getRandomInt(),
          getRandomInt(),
          getRandomInt(),
          getRandomInt(),
          getRandomInt(),
          getRandomInt(),
          getRandomInt(),
          getRandomInt(),
          getRandomInt(),
          getRandomInt(),
          getRandomInt()
        ]
      }
    ]
  }
  
  chartData.value = { ...updatedChartData }
}

function getRandomInt() {
  return Math.floor(Math.random() * (50 - 5 + 1)) + 5
}

onMounted(() => {
  fillData();
  setInterval(() => { fillData() }, 2000);
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
    :styles="styles as unknown as Partial<CSSStyleDeclaration>"
    :plugins="plugins as unknown as Plugin<'bar', unknown>[]"
  />
</template>