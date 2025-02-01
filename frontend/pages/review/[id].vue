<script setup lang="ts">
import { ref } from 'vue';
import { zodResolver } from '@primevue/forms/resolvers/zod';
import { useToast } from "primevue/usetoast";
import { z } from 'zod';

const route = useRoute()
const id = route.params.id
const router = useRouter();

if(!id) {
  router.push('/search');
}

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

const course = ref(loadCourse(id.toString()));
const avg_rating = ref(1);
const error = ref(null);
//const uni = ref(loadUni(course.university));

async function loadCourse(id:String) {
  try {
    const response: Response = await $fetch(getAPI() + '/courses/get_course/' + id, {
      method: 'GET',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' }
    });
    if (response.status === "success") {
      course.value = response.data;
      console.log(course.value);
      avg_rating.value = course.value.avg_course_rating;
    } else {
      await router.push('/');
    }
  } catch(err) {
    console.log(err)
    error.value = "There was an error while trying to submit the review. Make sure you have not already reviews this course.";
  }
};
</script>

<template>
  <RequireLogin />
  <Back class="back"/>
  <h2 class="first-elem bold-700">Write a New Course Review</h2>
  <div class="divider" />
  <div class="course">
    <CourseCard :course="course" />
  </div>
  <Form v-slot="$form" :resolver="resolver" :initialValues="initialValues" @submit="onFormSubmit" class="gap-4">
    <div class="divider" />
    <div class="section">
      <h3>1. Cognitive Load</h3>
      <p class="question">How challenging was the course content to understand and apply?</p>
      <div class="columns">
        <Stars :rating="ratings[0]" @update:rating="value => ratings[0] = value" :clickable="true" size="big" class="column thirds"/>
      </div>
    </div>
    <div class="divider" />
    <div class="section">
      <h3>2. Engagement & enjoyment</h3>
      <p class="question">How engaging or enjoyable were the course activities and teaching methods?</p>
      <div class="columns">
        <Stars :rating="ratings[1]" @update:rating="value => ratings[1] = value" :clickable="true" size="big" class="column thirds"/>
      </div>
    </div>
    <div class="divider" />
    <div class="section">
      <h3>3. Usefulness & relevance</h3>
      <p class="question">How well did this course meet your expectations and provide useful knowledge or skills?</p>
      <div class="columns">
        <Stars :rating="ratings[2]" @update:rating="value => ratings[2] = value" :clickable="true" size="big" class="column thirds"/>
      </div>
    </div>
    <div class="divider" />
    <div class="section">
      <h3>4. Course delivery and support</h3>
      <p class="question">How would you rate the effectiveness of the teaching methods and the overall support provided during the course?</p>
      <div class="columns">
        <Stars :rating="ratings[3]" @update:rating="value => ratings[3] = value" :clickable="true" size="big" class="column thirds"/>
      </div>
    </div>
    <div class="divider" />
    <div class="section">
      <h3>5. Overall Score</h3>
      <p class="question">How would you rate the course as a whole?</p>
      <div class="columns">
        <Stars :rating="ratings[4]" @update:rating="value => ratings[4] = value" :clickable="true" size="big" class="column thirds"/>
      </div>
    </div>
    <div class="divider" />
    <div class="text-region cente    max-width: 780px;
r">
      <div class="review-element text-input">
        <FloatLabel>
          <InputText name="title" v-model="title" class="review-input" />
          <label>Title</label>
        </FloatLabel>
        <Message v-if="$form.title?.invalid" severity="error" size="small">{{ $form.title.error?.message }}</Message>
      </div>

      <div class="review-element text-input">
        <FloatLabel>
          <TextArea name="body" v-model="body" class="review-input review-body" rows="5" cols="30" style="resize: none" />
          <label>Review</label>
        </FloatLabel>
        <Message v-if="$form.body?.invalid" severity="error" size="small">{{ $form.body.error?.message }}</Message>
      </div>

      <Message v-if="error" severity="error" size="small">{{ error }}</Message>
      <Button type="submit" label="Submit Review" class="review-submit"/>
    </div>
  </Form>
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

.course {
  width: 90vw;
  max-width: 1400px;
}

.section {
  margin: 48px 0;
  max-width: 800px;
}

.divider {
  border-bottom: 1px solid var(--h-gray-tp);
  width: 800px;
}

h3 {
  margin-bottom: 24px;
}

h2 {
  margin-bottom: 24px;
}

.question {
  margin: 16px 0;
}

.stars {
  width: 30%;
}

.rate {
  width: 400px;
}

.review-body {
  height: 200px;
}

.text-input {
  margin-top: 48px;
}

.text-region {
  width: 100%;
  max-width: 800px; /* or whatever width you prefer */
  margin: 0 auto;
}

.review-submit {
  margin-top: 16px;
}

.back {
  position: absolute;
  left:10%;
  top:100px;
}
</style>
