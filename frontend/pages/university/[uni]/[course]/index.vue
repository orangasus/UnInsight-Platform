<script setup lang="ts">
const route = useRoute()
const uni = route.params.uni
const course = route.params.course
</script>

<template>
<h1>University: {{ uni }}, Course: {{ course}}</h1>
</template>

<style scoped>

</style>