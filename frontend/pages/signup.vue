<script setup lang="ts">

import { ref } from 'vue';
import { zodResolver } from '@primevue/forms/resolvers/zod';
import { z } from 'zod';
import {getAPI} from "~/utils/constants";

const username = ref('');
const email = ref('');
const password = ref('');

const error = ref(null);
const router = useRouter();

const loading = ref(false);

const initialValues = ref({
  username: '',
  email: '',
  confirmPassword: '',
  password: ''
});

const resolver = ref(zodResolver(
    z.object({
      username: z.string().min(1, { message: 'Username is required.' }),
      email: z.string().min(1, { message: 'Email is required.' }).email({ message: 'Invalid email address.' }),
      confirmPassword: z.string().min(1, { message: 'Password confirmation is required.' }),
      password: z.string().min(1, { message: 'Password is required.' }).min(8, { message: 'Password must be at least 8 characters long.' }),
    }).refine(data => data.password === data.confirmPassword, {
      message: "Passwords do not match",
      path: ["confirmPassword"],
    })
));

const onFormSubmit = ({ valid }) => {
  if (valid) {
    handleSignUp()
  }
};

const handleSignUp = async () => {
  loading.value = true;
  error.value = null;
  try {
    const response = await $fetch(getAPI() + '/users/signup', {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: { 'username': username.value, 'email': email.value,'password': password.value}
    });
    loading.value = false;
    if (response.status === "success") {
      // Redirect after successful login
      await router.push({
        path: '/login',
        query: {
          message: "signup"
        },
      });
    } else {
      await router.push({
        path: '/login',
        query: {
          message: "signup"
        },
      });
    }
  } catch(err) {
    loading.value = false;
    error.value = 'An error occurred. Please try again.';
    console.log(err)
  }
};

</script>

<template>
  <Card class="auth panel">
    <template #header><h3 class="bold-700">Create an Account</h3></template>
    <template #content>
      <Message v-if="error" severity="error" size="small" variant="simple">{{ error }}</Message>
      <Form v-slot="$form" :resolver="resolver" :initialValues="initialValues" @submit="onFormSubmit" class="gap-4">
        <div class="auth element">
          <FloatLabel variant="on">
            <InputText name="username" type="text" class="auth input" v-model="username" />
            <label for="on_label">Username</label>
          </FloatLabel>
          <Message v-if="$form.username?.invalid" severity="error" size="small" variant="simple">{{ $form.email.error?.message }}</Message>
        </div>
        <div class="auth element separate">
          <FloatLabel variant="on">
            <InputText name="email" type="text" class="auth input" v-model="email" />
            <label for="on_label">Email</label>
          </FloatLabel>
          <Message v-if="$form.email?.invalid" severity="error" size="small" variant="simple">{{ $form.email.error?.message }}</Message>
        </div>
        <div class="auth element separate">
          <FloatLabel variant="on">
            <InputText name="password" type="password" class="auth input" v-model="password" />
            <label for="on_label">Password</label>
          </FloatLabel>
          <Message v-if="$form.password?.invalid" severity="error" size="small" variant="simple">{{ $form.password.error?.message }}</Message>
        </div>
        <div class="auth element">
          <FloatLabel variant="on">
            <InputText name="confirmPassword" type="password" class="auth input" />
            <label for="on_label">Confirm password</label>
          </FloatLabel>
          <Message v-if="$form.confirmPassword?.invalid" severity="error" size="small" variant="simple">{{ $form.confirmPassword.error?.message }}</Message>
        </div>
        <Button type="submit" label="Sign Up" class="auth submit" :disabled="loading"/>
      </Form>
    </template>
    <template #footer>
      <p class="m-0">
        Already have an account? <NuxtLink to="/login" class="text-link">Log in</NuxtLink>
      </p>
    </template>
  </Card>
</template>

<style scoped>
.separate {
}
</style>