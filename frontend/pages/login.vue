<script setup lang="ts">

import { ref } from 'vue';
import { zodResolver } from '@primevue/forms/resolvers/zod';
import { useToast } from "primevue/usetoast";
import { z } from 'zod';
import {useRoute} from "vue-router";

const router = useRouter();
const route = useRoute();

const messages = {
  "reset": "Password reset successful. Log in with your new password.",
  "reset_request": "Check your email for a password reset link.",
  "confirm": "Account activated. Log in to continue.",
  "signup": "Account created successfully. Check your email for an activation link before continuing.",
  "verified": "Account activated. Log in to continue.",
  "verify_failed": "Account activated. Log in to continue."
}

const username = ref(null);
const password = ref(null);
const error = ref(null);
const message = ref(null);

const message_name = route.query.message;
if (message_name) {
  message.value = messages[message_name];
}

const loading = ref(false);

const usernameCookie = useCookie("username");

const initialValues = ref({
  username: '',
  password: ''
});

const resolver = ref(zodResolver(
    z.object({
      username: z.string().min(1, { message: 'Username is required.' }),//.email({ message: 'Invalid email address.' }),
      password: z.string().min(1, { message: 'Password is required.' }),
    })
));

const onFormSubmit = ({ valid }) => {
  if (valid) {
    handleLogin();
  }
};

const handleLogin = async () => {
  error.value = null;
  loading.value = true;
  try {
    const response = await $fetch(getAPI() + '/users/login', {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: { 'username': username.value, 'password': password.value }
    });
    loading.value = false;

    if (username.value) {
      usernameCookie.value = username.value.toLowerCase();
    }

    const redirectTo = route.query.redirect || '/';
    setConnected(true);

    window.location.href = "https://uni.styro.dev" + redirectTo //TODO: Use router
  } catch (err) {
    loading.value = false;
    if (err.response && err.response.status === 404) {
      error.value = 'Incorrect username or password. Make sure your email is activated.';
    } else {
      error.value = 'An error occurred. Please try again.';
    }
    console.log(err);
  }
};
</script>

<template>
  <Message v-if="message" size="small" variant="simple" class="message">{{ message }}</Message>
  <Card class="auth panel">
    <template #header>
      <h3 class="bold-700">Log in to Site</h3>
    </template>
    <template #content>
      <Message v-if="error" severity="error" size="small" variant="simple">{{ error }}</Message>
      <Form v-slot="$form" :resolver="resolver" :initialValues="initialValues" @submit="onFormSubmit" class="gap-4">
        <div class="auth element">
          <FloatLabel variant="on">
            <InputText name="username" type="text" v-model="username" class="auth input" />
            <label for="on_label">Username</label>
          </FloatLabel>
          <Message v-if="$form.username?.invalid" severity="error" size="small" variant="simple">{{ $form.username.error?.message }}</Message>
        </div>
        <div class="auth element">
          <FloatLabel variant="on">
            <InputText name="password" v-model="password" type="password" class="auth input"/>
            <label for="on_label">Password</label>
          </FloatLabel>
          <Message v-if="$form.password?.invalid" severity="error" size="small" variant="simple">{{ $form.password.error?.message }}</Message>
        </div>
        <Button type="submit" label="Log In" class="auth submit" :disabled="loading"/>
      </Form>
    </template>
    <template #footer>
      <p class="m-0">
        Don't have an account? <NuxtLink to="/signup" class="text-link">Sign up</NuxtLink>
      </p>
      <p class="m-0 box">
        <NuxtLink to="/reset_password" class="text-link">Reset your password</NuxtLink>
      </p>
    </template>
  </Card>
</template>

<style scoped>
.message {
  margin-bottom: 16px;
}
</style>