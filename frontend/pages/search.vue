<script setup lang="ts">
import {ref, watch, nextTick, onMounted, computed} from "vue";
import { useRoute, useRouter } from "vue-router";
import CourseCard from "~/components/CourseCard.vue";

const route = useRoute();
const router = useRouter();

const searchTerm = ref(route.query.search || null);
const searchOption = ref(route.query.option || "0");
const searchResults = ref([]);
const loading = ref(true);

async function search(query: string) {
  try {
    const url = getAPI() + "/courses/search/search_query/" + (query ? "?search_query=" + query : "");
    const response = await $fetch(url, {
      method: "GET",
      credentials: "include",
    });

    if (response.status === "success") {
      return response.data;
    } else {
      await router.push("/");
      return [];
    }
  } catch (err) {
    console.error("Search failed:", err);
    await router.push("/");
    return [];
  }scrollToResults
}

const fetchSearchResults = async () => {
  loading.value = true;
  const currentValue = searchTerm.value || "";
  searchResults.value = await search(currentValue.trim());
  loading.value = false;
  if(searchTerm.value !== null)
    scrollToResults();
  searchTerm.value = currentValue.trim();
};

const scrollToResults = () => {
  if (process.client) {
    const resultsSection = document.querySelector(".results");
    if (resultsSection) {
      const offset = 100;
      slowScrollTo(resultsSection.offsetTop - offset, 1000);
    }
  }
};

const slowScrollTo = (targetPosition, duration) => {
  const startPosition = window.scrollY;
  const distance = targetPosition - startPosition;
  let startTime = null;

  const easeInOutQuad = (t) => t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;

  const animation = (currentTime) => {
    if (startTime === null) startTime = currentTime;
    const timeElapsed = currentTime - startTime;
    const progress = Math.min(timeElapsed / duration, 1);
    const easedProgress = easeInOutQuad(progress);

    window.scrollTo(0, startPosition + distance * easedProgress);

    if (timeElapsed < duration) {
      requestAnimationFrame(animation);
    }
  };

  requestAnimationFrame(animation);
};

watch(() => route.query.search, async (newSearchTerm) => {
  searchTerm.value = newSearchTerm ?? "";
  if (searchTerm.value) {
    await fetchSearchResults();
  }
});

watch(() => route.query.option, async (newSearchOption) => {
  searchOption.value = newSearchOption;
  if (searchTerm.value) {
    await fetchSearchResults();
  }
});

onMounted(() => {
  if (searchOption.value) {
    fetchSearchResults();
  }
});
</script>

<template>
  <div class="bg-effect" />
  <div class="title first-elem center">
    <h1 class="bold-800">Read Reviews Of<br><span class="bold-800 secondary">6400+</span> Courses</h1>
    <p class="box">
      Explore courses and professors from universities worldwide. Use filters to find<br>
      exactly what you're looking for—whether it's the perfect course to match your<br>
      interests or insights into professors' teaching styles.
    </p>
  </div>
  <CourseSearchBar :default-search-type-index="parseInt(searchOption)" />

  <div class="results">
    <h3 class="tleft">Find The Right Course</h3>
    <CourseSearchBar :default-search-term="searchTerm" :default-search-type-index="parseInt(searchOption)" class="search-bottom" />

    <p v-if="loading" class="tcenter gray">Loading courses...</p>
    <div v-else-if="searchResults.length > 0" class="courses center">
      <p class="tcenter gray">{{searchResults.length}} Results</p>
      <CourseCard v-for="course in searchResults" :key="course.id" :course="course" />
    </div>
    <p v-else class="tcenter gray">0 Results</p>
  </div>

  <Footer />
</template>

<style scoped>
.courses {
  width: 100%;
}

.title {
  margin-top: 300px;
}

.results {
  margin-top: 400px;
  margin-bottom: 80px;
  width: 90vw;
  max-width: 1400px;
}

.search-bottom {
  margin: 24px 0;
}
</style>
