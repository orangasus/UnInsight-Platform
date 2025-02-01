<script setup lang="ts">
import { computed, defineProps } from 'vue';

const props = defineProps({
  percentage: { type: Number, default: 0 },
  fillColor: { type: String, default: null },
});

const widthStyle = computed(() => ({
  width: `${Math.min(Math.max(props.percentage, 0), 100)}%`,
  backgroundColor: props.fillColor || 'var(--primary)',
}));
</script>

<template>
  <div class="progress-bar">
    <div class="progress-fill" :style="widthStyle"></div>
  </div>
</template>

<style scoped>
.progress-bar {
  width: 100%;
  height: 24px;
  background-color: none;
  border-radius: 8px;
  border: 1px solid var(--h-gray-tp);
  --un-border-opacity: 0.5;
}

.progress-fill {
  height: 100%;
  width: 0%;
  transition: width 0.3s ease-in-out;
  border-radius: 8px;
}
</style>
