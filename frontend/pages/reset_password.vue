<script setup lang="ts">

import { ref } from 'vue';
import { zodResolver } from '@primevue/forms/resolvers/zod';
import { z } from 'zod';
import {getAPI} from "~/utils/constants";

const route = useRoute();
const router = useRouter();

const uidb64 = route.query.uidb64
const token = route.query.token

const password = ref('');
const email = ref('');
const error = ref(null);
const loading = ref(false);

const reset_initialValues = ref({
  confirmPassword: '',
  password: ''
});

const reset_resolver = ref(zodResolver(
    z.object({
      confirmPassword: z.string().min(1, { message: 'Password confirmation is required.' }),
      password: z.string().min(1, { message: 'Password is required.' }),
    }).refine(data => data.password === data.confirmPassword, {
      message: "Passwords do not match",
      path: ["confirmPassword"],
    })
));

const initialValues = ref({
  email: ''
});

const resolver = ref(zodResolver(
    z.object({
      email: z.string().min(1, { message: 'Email is required.' }).email({ message: 'Invalid email address.' })
    })
));

const onResetFormSubmit = ({ valid }) => {
  if (valid) {
    handleReset()
  }
};

const handleReset = async () => {
  loading.value = true;
  error.value = null;
  try {
    const response = await $fetch(getAPI() + '/users/reset_password/', {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: { 'token': token, 'uidb64':uidb64, 'new_password': password.value}
    });
    loading.value = false;

    await router.push({
      path: '/login',
      query: {
        message: "reset"
      },
    });
  } catch(err) {
    loading.value = false;
    error.value = 'An error occurred. Please try again.';
    console.log(err)
  }
};

const onFormSubmit = ({ valid }) => {
  if (valid) {
    handleResetRequest()
  }
};

const handleResetRequest = async () => {
  loading.value = true;
  error.value = null;
  try {
    const response = await $fetch(getAPI() + '/users/reset_password_request?email=' + email.value, {
      method: 'GET'
    });
    loading.value = false;

    await router.push({
      path: '/login',
      query: {
        message: "reset_request"
      },
    });
  } catch(err) {
    loading.value = false;
    error.value = 'An error occurred. Please try again.';
    console.log(err)
  }
};

</script>

<template>
  <Card class="auth panel" v-if="token">
    <template #header><h3 class="bold-700">Set your new password</h3></template>
    <template #content>
      <Message v-if="error" severity="error" size="small" variant="simple">{{ error }}</Message>
      <Form v-slot="$form" :resolver="reset_resolver" :initialValues="reset_initialValues" @submit="onResetFormSubmit" class="gap-4">
        <div class="auth element">
          <FloatLabel variant="on">
            <InputText name="password" type="password" class="auth input" v-model="password" />
            <label for="on_label">New Password</label>
          </FloatLabel>
          <Message v-if="$form.password?.invalid" severity="error" size="small" variant="simple">{{ $form.password.error?.message }}</Message>
        </div>
        <div class="auth element">
          <FloatLabel variant="on">
            <InputText name="confirmPassword" type="password" class="auth input" />
            <label for="on_label">Confirm new password</label>
          </FloatLabel>
          <Message v-if="$form.confirmPassword?.invalid" severity="error" size="small" variant="simple">{{ $form.confirmPassword.error?.message }}</Message>
        </div>
        <Button type="submit" label="Reset" class="auth submit" :disabled="loading"/>
      </Form>
    </template>
    <template #footer>
    </template>
  </Card>
  <Card class="auth panel" v-else>
    <template #header>
      <h3 class="bold-700">Reset your password</h3>
      <p class="box subtext gray">Enter your email address below, and we’ll send you instructions to reset your password. If you don’t receive an email within a few minutes, please check your spam folder.</p>
    </template>
    <template #content>
      <Message v-if="error" severity="error" size="small" variant="simple">{{ error }}</Message>
      <Form v-slot="$form" :resolver="resolver" :initialValues="initialValues" @submit="onFormSubmit" class="gap-4">
        <div class="auth element">
          <FloatLabel variant="on">
            <InputText name="email" type="text" class="auth input" v-model="email" />
            <label for="on_label">Email</label>
          </FloatLabel>
          <Message v-if="$form.email?.invalid" severity="error" size="small" variant="simple">{{ $form.email.error?.message }}</Message>
        </div>
        <Button type="submit" label="Reset" class="auth submit" :disabled="loading"/>
      </Form>
    </template>
    <template #footer>
    </template>
  </Card>
</template>

<style scoped>
.box {
  margin-bottom: -40px;
}
</style>