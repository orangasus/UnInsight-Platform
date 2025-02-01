<script setup lang="ts">
import { ref, onMounted, watch } from "vue";
import { setConnected, isConnected } from "~/utils/utils";

const session = ref("");
const usernameCookie = useCookie("username");
const sessionCookie = useCookie("sessionid");
const tokenCookie = useCookie("csrftoken");

const log_out = async () => {
  try {
    await $fetch(getAPI() + '/users/logout', {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' }
    });
  } catch (e) {
    console.error(e);
  }
  setConnected(false);
  session.value = null;
  usernameCookie.value = null;
  sessionCookie.value = null;
  tokenCookie.value = null;
  window.location.href = "https://uni.styro.dev/" //TODO: Use router
};

const items = ref([
  {
    label: 'Home',
    command: () => navigateTo('/')
  },
  {
    label: 'Course & Professor Search',
    icon: 'pi pi-search',
    command: () => navigateTo('/search')
  }
]);

const menu_items = ref([]);

const guest_items = [
  {
    label: 'Log In',
    severity: 'secondary',
    button: true,
    color: 'text',
    command: () => navigateTo("/login")
  },
  {
    label: "Sign Up",
    button: true,
    color: 'accent',
    command: () => navigateTo("/signup")
  }
];

const user_items = [
  {
    label: 'Write a review',
    color: 'accent',
    button: true,
    command: () => navigateTo("/search")
  },
  {
    label: session,
    items: [
      {
        label: 'Courses',
        command: () => navigateTo('/search')
      },
      {
        label: "Log Out",
        color: 'red',
        command: log_out
      }
    ]
  }
];

function setUpGuest() {
  menu_items.value = guest_items;
}

function setUpUser() {
  session.value = usernameCookie.value;
  menu_items.value = user_items;
}

async function handleSession() {
  try {
    const response = await $fetch(getAPI() + '/users/get_session', {
      method: 'GET',
      credentials: 'include',
    });
    if(response.message === "Valid") {
      setUpUser();
      setConnected(true);
    } else {
      setUpGuest();user_items
      setConnected(false);
    }
  } catch (err) {
    console.error(err);
    setUpGuest();
    setConnected(false);

  }
}

onMounted(() => {
  handleSession();
});

watch(isConnected, (newVal) => {
  if (newVal) {
    setUpUser();
  } else {
    setUpGuest();
  }
});
</script>

<template>
  <header class="card">
    <Menubar :model="items" class="navbar">
      <template #start>
        <NuxtLink to="/" class="logo">
          <img src="../assets/images/uninsight-main-logo.svg" alt="Uninsight" class="logo title2" />
        </NuxtLink>
      </template>
      <template #end>
        <Menubar :model="menu_items" class="sub-menu">
          <template #item="{ item, props, hasSubmenu, root }">
            <Button
                v-if="item.button"
                :label="item.label"
                :severity="item.severity"
                v-bind="props.action"
                :class="item.color"
            />
            <a v-else v-ripple class="flex" v-bind="props.action">
              <span :style="{ color: item.color }">{{ item.label }}</span>
              <i
                  v-if="hasSubmenu"
                  :class="['pi pi-angle-down ml-auto', { 'pi-angle-down': root, 'pi-angle-right': !root }]"
              ></i>
            </a>
          </template>
        </Menubar>
      </template>
    </Menubar>
  </header>
</template>

<style scoped>
.navbar {
  margin: 0;
  border: none;
  border-radius: 0;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
  padding: 0.5rem 1rem;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 1000;
  display: flex;
  height: 78px;
  background-color: var(--background);
}

.p-button {
  margin: 0 0.2rem;
  font-size: 14px;
}

.sub-menu {
  width: 100%;
  height: 100%;
  border: none;
  padding: 0;
  background-color: var(--background);
}

.logo {
  height: 50px;
  width: auto;
  background: none;
}

.logo:hover {
  background: none;
}

.p-menubar-item:hover, .p-menubar-item-content:hover {
  background-color: red !important;
  color: #333333;
}

.navbar {
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
