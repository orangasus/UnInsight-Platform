<script setup lang="ts">

const router = useRouter();
const route = useRoute();
const redirectPath = ref('/');


async function handleSession() {
  try {
    const response = await $fetch(getAPI() + '/users/get_session', {
      method: 'GET',
      credentials: 'include',
    });
    if(response.message === "Valid") {
    } else {
      redirectPath.value = route.fullPath;
      router.push({ path: '/login', query: { redirect: redirectPath.value } });
    }
  } catch (err) {
    redirectPath.value = route.fullPath;
    router.push({ path: '/login', query: { redirect: redirectPath.value } });

  }
}
onMounted(() => {
  handleSession();
});
</script>

<template></template>