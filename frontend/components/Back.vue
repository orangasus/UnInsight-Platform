<script setup lang="ts">

</script>

<template>
  <Button @click="$router.back()" class="back"><PhosphorIconCaretLeft :size="24" />Back</Button>
</template>

<style scoped>
.back {
  background: none;
  border: none;
  color: var(--h-gray);
  opacity: 60%;
}

.back:hover {
  background: none;
  border: none;
  color: var(--h-gray);
  opacity: 80%;
}
</style>