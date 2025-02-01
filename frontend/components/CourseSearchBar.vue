<script setup lang="ts">
import { ref, computed, defineProps, watch } from "vue";
import { getUniversityName} from "~/utils/utils";
import { useRouter } from "vue-router";

const router = useRouter();

const props = defineProps({
  defaultSearchTerm: String,
  defaultSearchTypeIndex: {
    type: Number,
    default: 0
  }
});

const selectedCourse = ref(props.defaultSearchTerm || "");
const filteredCourses = ref([]);

let debounceTimer: number | null = null;

const search = (event) => {
  const query = event.query.trim();
  if (!query) {
    filteredCourses.value = [];
    return;
  }

  if (debounceTimer) {
    clearTimeout(debounceTimer);
  }

  debounceTimer = setTimeout(async () => {
    try {
      const url = getAPI() + "/courses/search/search_query/" + "?search_query=" + encodeURIComponent(query);
      const response = await $fetch(url, {
        method: "GET",
        credentials: "include",
      });

      if (response.status === "success" && Array.isArray(response.data)) {
        // Group courses by university
        const universityGroups = new Map();

        for (const course of response.data) {
          const universityCode = course.university.toString();

          if (!universityGroups.has(universityCode)) {

            universityGroups.set(universityCode, {
              'code': universityCode.toString(),
              'label': await getUniversityName(course.university),
              'items': []
            });
          }

          universityGroups.get(universityCode).items.push({
            'label': course.course_code + ': ' + course.course_name,
            'value': course.id.toString()
          });
        }

        // Convert Map to Array and force reactivity update
        filteredCourses.value = [...universityGroups.values()];
      } else {
        filteredCourses.value = [];
      }
    } catch (err) {
      console.error("Autocomplete failed:", err);
      filteredCourses.value = [];
    }
  }, 1000);
};

const search_types = [
  { name: 'Course', id: 0 },
  { name: 'Professor', id: 1 }
];

const selectedSearch = ref(search_types[props.defaultSearchTypeIndex] || search_types[0]);

const onFormSubmit = ({ valid }) => {
  if(typeof selectedCourse.value === 'string') {
    router.push({
      path: '/search',
      query: {
        search: selectedCourse.value || " ",
        option: selectedSearch.value.id
      }
    });
  } else {
    router.push({
      path: '/course/' + selectedCourse.value.value
    });
  }
};

const placeholder = computed(() => {
  if (selectedSearch.value.id === 0) {
    return 'Course name, code or keyword';
  } else if (selectedSearch.value.id === 1) {
    return 'Professor name';
  }
  return 'Search';
});

watch(() => props.defaultSearchTerm, (newSearchTerm) => {
  selectedCourse.value = newSearchTerm || "";
});

watch(() => props.defaultSearchTypeIndex, (newSearchTypeIndex) => {
  selectedSearch.value = search_types[newSearchTypeIndex] || search_types[0];
});

  const handleKeydown = (event) => {
    if (event.key === 'Enter') {
      event.preventDefault();
      onFormSubmit({ valid: true });
    }
  }
</script>

<template>
  <Form @submit="onFormSubmit">
    <div class="searchbar-container">
      <Select
          v-model="selectedSearch"
          :options="search_types"
          optionLabel="name"
          class="searchbar-element select"
      />
      <AutoComplete
          v-model="selectedCourse"
          class="searchbar-element autocomplete"
          :suggestions="filteredCourses"
          @complete="search"
          optionLabel="label"
          optionGroupLabel="label"
          optionGroupChildren="items"
          :placeholder="placeholder"
          @keydown="handleKeydown"
      >
        <template #optiongroup="slotProps">
          <div class="flex items-center">
            <img
                :alt="slotProps.option.label"
                src="https://primefaces.org/cdn/primevue/images/flag/flag_placeholder.png"
                :class="`flag flag-${slotProps.option.code.toLowerCase()} mr-2`"
                style="width: 18px"
            />
            <div>{{ slotProps.option.label }}</div>
          </div>
        </template>
      </AutoComplete>
      <Button icon="pi pi-filter" aria-label="Filter" class="iconbutton" />
      <Button type="submit" label="Search" class="search-btn" />
    </div>
  </Form>
</template>


<style scoped>
.searchbar-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  min-width: 35vw;
  padding: 0.5rem;
  background: white;
  border: 1px solid rgba(217, 217, 217, 1);
  border-radius: 8px;
  gap: 0.5rem;
}

.searchbar-element {
  margin: 0;
}

.select {
  flex-shrink: 0;
}

.autocomplete {
  flex-grow: 1;
  min-width: 200px;
}

.iconbutton {
  background: none !important;
  border: none !important;
  color: var(--primary) !important;
}

.iconbutton:hover {
  background: none !important;
  border: none !important;
  color: var(--primary) !important;
}

.search-btn {
  flex-shrink: 0;
}
</style>
