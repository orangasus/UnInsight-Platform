<script setup lang="ts">
import { computed, watchEffect } from "vue";
import { useRoute, useRouter } from "vue-router";

const route = useRoute();
const router = useRouter();

const uidb64 = computed(() => route.query.uidb64);
const token = computed(() => route.query.token);

const handleConfirmation = async () => {
  try {
    const response = await $fetch(`https://ui.styro.dev/emails/activate/${uidb64.value}/${token.value}`, {
      method: "GET",
    });
    console.log(response);
    await router.push({
      path: "/login",
      query: {
        message: "verified",
      },
    });
  } catch (err) {
    console.log("ERROR");
    console.error(err);
    await router.push({
      path: "/login",
      query: {
        message: "verify_failed",
      },
    });
  }
};

watchEffect(() => {
  if (uidb64.value && token.value) {
    handleConfirmation();
  }
});
</script>

<template>

</template>

<style scoped>

</style>