<script setup lang="ts">
import { ref } from 'vue';
import { zodResolver } from '@primevue/forms/resolvers/zod';
import { useToast } from "primevue/usetoast";
import { z } from 'zod';

const route = useRoute()
const id = route.params.id
const router = useRouter();

const title = ref('');
const body = ref('');
const ratings = ref([0, 0, 0, 0, 0]);

const initialValues = ref({
  title: '',
  body: '',
  ratings: [0, 0, 0, 0, 0]
});

const resolver = ref(zodResolver(
    z.object({
      title: z.string().min(1, { message: 'Title is required.' }),
      body: z.string().min(1, { message: 'Review body is required.' }),
      ratings: z.array(z.number().min(1, { message: 'Each rating must be at least 1.' })).length(5)
    })
));

const onFormSubmit = ({ valid }) => {
  if (valid) {
    submitReview();
  }
};

const submitReview = async () => {
  try {
    const r = ratings.value;
    const response = await $fetch(getAPI() + '/reviews/create/', {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: {
        title: title.value, body: body.value,
        cognitive_load_rating: r[0], delivery_support_rating: r[1], engagement_enjoyment_rating: r[2], usefulness_relevance_rating: r[3], overall_rating: r[4],
        user: 1, course: id }
    });
    router.push(`/course/${id}`);
  } catch (error) {
    console.error(error);
    router.push('/');
  }
};
</script>

<template>
  <RequireLogin />
  <Card class="review-panel">
    <template #header>Leave a Review</template>
    <template #content>
      <Form v-slot="$form" :resolver="resolver" :initialValues="initialValues" @submit="onFormSubmit" class="gap-4">
        <div class="review-element">
          <FloatLabel>
            <InputText name="title" v-model="title" class="review-input" />
            <label>Title</label>
          </FloatLabel>
          <Message v-if="$form.title?.invalid" severity="error" size="small">{{ $form.title.error?.message }}</Message>
        </div>

        <div class="review-element">
          <FloatLabel>
            <Textarea name="body" v-model="body" class="review-input" />
            <label>Review</label>
          </FloatLabel>
          <Message v-if="$form.body?.invalid" severity="error" size="small">{{ $form.body.error?.message }}</Message>
        </div>

        <div class="review-element" v-for="(rating, index) in ratings" :key="index">
          <label>Category {{ index + 1 }}</label>
          <Stars :rating="ratings[index]" @update:rating="value => ratings[index] = value" :clickable="true" />
          <Message v-if="$form.ratings?.invalid" severity="error" size="small">Each rating must be at least 1.</Message>
        </div>

        <Button type="submit" label="Submit Review" class="review-submit"/>
      </Form>
    </template>
  </Card>
</template>

<style scoped>
.review-panel {
  width: 100%;
  max-width: 500px;
  margin: auto;
}
.review-element {
  margin-bottom: 1rem;
}
.review-input {
  width: 100%;
}
.review-submit {
  width: 100%;
}
</style>
