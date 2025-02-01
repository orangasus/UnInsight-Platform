<script setup lang="ts">
import {defineEmits, ref, watchEffect} from "vue";
import CourseCard from "~/components/CourseCard.vue";
import {getDepartments, getProfessorData, getReviews, getUniversityName} from "~/utils/utils";

const route = useRoute()
const id = route.params.id
const router = useRouter();

const course = ref(loadCourse(id.toString()));
const avg_rating = ref(1);
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
    await router.push('/');
  }
};


/*async function loadUni(id:String){
  try {
    const response: Response = await $fetch(getAPI() + '/courses/get_course/' + id, {
      method: 'GET',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: { }
    });
    if (response.success) {
      course.value = response.data;
    } else {
      await router.push('/');
    }
  } catch(err) {
    console.log(err)
    await router.push('/');
  }
};*/
const statDesc = ["Awful", "Bad", "Ok", "Good", "Great"]

function getStatPercentage(rating:number) {
  return Math.round((rating / 5) * 100);
}

function getStatDescription(rating:number) {
  return statDesc[Math.floor(rating-0.45)];
}

const reviews = ref([]);
const loading = ref(true);
const professor = ref({"name":"Unknown", "rating":"0"});
const departments = ref(null);


watchEffect(async () => {
  if (!course.value || !course.value.id) return;
  loading.value = true;
  professor.value = await getProfessorData(course.value.professors[0]); //TODO: Make it work with multiple
  loading.value = false;
});

watchEffect(async () => {
  if (!course.value || !course.value.id) return;
  loading.value = true;
  reviews.value = await getReviews(course.value.id);
  departments.value = getDepartments(course);
  loading.value = false;
});
</script>

<template>
  <div class="bg-effect" />
  <Back class="back"/>
  <div class="container first-elem">
    <span class="subtitle content"> {{course.course_code}} </span>
  </div>
  <div class="course-info">
    <div>
      <h2 class="bold-700 box title">{{course.course_name}}</h2>
      <div class="columns box center" v-if="departments">
        <div class="column first center">
          <div class="columns">
            <p class=""><PhosphorIconMapPin /> {{ course.university_name}}</p>
          </div>
        </div>
        <div class="column second center">
          <div class="columns center">
            <p class="texticon"><i class="pi pi-book"></i></p>
            <p class="text">{{departments}} </p>
          </div>
        </div>
      </div>
      <div class="column center" v-else>
        <p class=""><PhosphorIconMapPin /> {{ course.university_name}}</p>
      </div>
      <div class="columns">
        <div class="column info left">
          <div class="container column center main_stats">
            <p class="">Overall Rating</p>
            <h2>{{course.avg_course_rating || '0.0'}}</h2>
            <Stars :rating="parseInt(course.avg_course_rating || '0')" size="small" />
            <p class="subtext gray">( {{reviews.length}} review{{reviews.length == 1 ? "" : "s"}} )</p>
          </div>
          <div class="container column center main_stats">
            <p class="subtext gray">Professor</p>
            <h4 class="bold-600" v-for="prof_name in course.professors_names">{{prof_name}}</h4>
            <Stars :rating="parseInt(professor.rating || '0')" size="small"/>
          </div>
        </div>
        <div class="column info right">
          <div class="container column center stats">
            <div class="columns center">
              <div class="column thirds"><p class="tleft subtext gray">{{getStatPercentage(course.avg_cognitive_load_rating)}}%</p></div>
              <div class="column thirds"><p class="tcenter">Cognitive Load</p></div>
              <div class="column thirds"><p class="tright subtext gray">{{getStatDescription(course.avg_cognitive_load_rating)}}</p></div>
            </div>
            <Bar :percentage="getStatPercentage(course.avg_cognitive_load_rating)" />
          </div>

          <div class="container column center stats">
            <div class="columns center">
              <div class="column thirds"><p class="tleft subtext gray">{{getStatPercentage(course.avg_delivery_support_rating)}}%</p></div>
              <div class="column thirds"><p class="tcenter">Support</p></div>
              <div class="column thirds"><p class="tright subtext gray">{{getStatDescription(course.avg_delivery_support_rating)}}</p></div>
            </div>
            <Bar :percentage="getStatPercentage(course.avg_delivery_support_rating)" />

          </div>

          <div class="container column center stats">
            <div class="columns center">
              <div class="column thirds"><p class="tleft subtext gray">{{getStatPercentage(course.avg_engagement_enjoyment_rating)}}%</p></div>
              <div class="column thirds"><p class="tcenter">Enjoyment</p></div>
              <div class="column thirds"><p class="tright subtext gray">{{getStatDescription(course.avg_engagement_enjoyment_rating)}}</p></div>
            </div>
            <Bar :percentage="getStatPercentage(course.avg_engagement_enjoyment_rating)" />
          </div>

          <div class="container column center stats">
            <div class="columns center">
              <div class="column thirds"><p class="tleft subtext gray">{{getStatPercentage(course.avg_usefulness_relevance_rating)}}%</p></div>
              <div class="column thirds"><p class="tcenter">Usefulness</p></div>
              <div class="column thirds"><p class="tright subtext gray">{{getStatDescription(course.avg_usefulness_relevance_rating)}}</p></div>
            </div>
            <Bar :percentage="getStatPercentage(course.avg_usefulness_relevance_rating)" />
          </div>
        </div>
      </div>
    </div>
    <div class="row"><!--
      <Badge value="Online" severity="secondary" />
      <Badge value="Advanced" severity="secondary" />
      <Badge severity="secondary">Estimated weekly hours:&nbsp&nbsp<b class="bold-800">8-10 hours</b> </Badge>-->
    </div>
  </div>

  <div class="bottom">
    <h2>Reviews & Comments</h2>
    <p class="box desc">Dive into detailed reviews from students who've taken this course. Discover their experiences, insights,
      and advice to help you decide if this course s right for you, </p>
</div>

    <div class="reviews-header">
      <span class="bold-600 text">{{ reviews.length }} Review{{reviews.length == 1 ? "" : "s"}}</span>
      <Button label="Write a review" @click="$router.push({
      'path': '/review/' + course.id
      })"/>
    </div>
    <div v-if="loading">
      <p>Loading reviews...</p>
    </div>

    <div v-else-if="reviews.length > 0" class="courses">
      <Reviews :reviews="reviews" />
    </div>

    <p v-else>There are no reviews yet for this course. Be the first one to add one!.</p>

</template>

<style scoped>
.back {
  position: absolute;
  left:10%;
  top:100px;
}

.reviews-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  margin-top: 48px;
}

.first-elem {
  margin-top: 200px;
}

.title {
  margin-bottom: 48px;
}

.course-info {
  width: 50vw;
  max-width: 700px;
}

@media (max-width: 768px) {
  .course-info {
    max-width: 600px;
    width: 90vw;
  }
}

.main_stats {
  padding-top: 34px;
  padding-bottom: 34px;
}

.stats {
  padding-top: 8px;
  padding-bottom: 8px;
}

.first {
  width: 60%;
}

.info {
  margin-top: 24px;
}

.info.left {
  width: 30%;
}

.info.right {
  width: 70%;
}

.reviews-header {
  max-width: 1400px;
  gap: 53vw;
}

.bottom {
  margin-top: 220px;
  margin-bottom: 80px;
}
</style>