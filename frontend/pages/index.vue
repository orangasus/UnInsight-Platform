<script setup lang="ts">
import {ref, watchEffect} from "vue";

const reviews = ref([]);
const loading = ref(true);

async function getReviews() {
  try {
    const response: Response = await $fetch(getAPI() + '/reviews/latest_reviews/', {
      method: "GET",
      credentials: "include",
    });
    return response.data;
  } catch (err) {
    console.error("Search failed:", err);
    return [];
  }
}

watchEffect(async () => {
  loading.value = true;
  reviews.value = await getReviews();
  loading.value = false;
});
</script>

<template>
  <div class="bg-effect long-bg" />
  <div class="title first-elem center">
    <h1 class="bold-800">Unbiased Reviews of<br>University Courses,<br><span class="bold-800 secondary">All in One Place.</span></h1>
    <p class="box">
      Easily explore and compare university courses. Read honest student
      reviews and make informed decisions to find the right course for you.
    </p>
  </div>
  <CourseSearchBar />

  <div class="info">
    <div class="columns center panels">
      <div class="column container thirds center panel">
        <h4><PhosphorIconBookOpenText :size="48"/></h4>
        <p>Browse Courses from<br>Universities worldwide</p>
      </div>
      <div class="column container thirds center panel">
        <h4><PhosphorIconStar :size="48"/></h4>
        <p>Honest, Anonymous<br>Reviews</p>
      </div>
      <div class="column container thirds center panel">
        <h4><PhosphorIconChatText :size="48"/></h4>
        <p>Help other by<br>sharing your opinion</p>
      </div>
    </div>
  </div>
  <div class="info container center full">
    <div>
      <h2 class="white">Choosing The Right Course<br>Shouldn't Be A Gamble.<br><b class="bold-700 accent">So We Solved It.</b></h2>
      <div class="columns site-stats">
        <div class="column thirds center">
          <h2 class="white">50+</h2>
          <h4 class="white">Universities</h4>
        </div>
        <div class="column thirds center">
          <h2 class="white">6400+</h2>
          <h4 class="white">Courses</h4>
        </div>
        <div class="column thirds center">
          <h2 class="white">400+</h2>
          <h4 class="white">Professors</h4>
        </div>
      </div>
    </div>
  </div>
  <div class="info center recent-rev">
    <h2>Recent Course Reviews</h2>
    <p class="box desc">See what students are saying! Check out the latest reviews to get real,
      up-to-date insights on courses from universities around the world. </p>
    </div>
    <div v-if="loading">
      <p>Loading reviews...</p>
    </div>
    <div v-else-if="reviews.length > 0" class="courses">
      <Reviews :reviews="reviews" class="reviews"/>
    </div>
    <p v-else>Weird! There are no new reviews yet.</p>
    <Button label="Browse Courses & Professors" class="box" @click="navigateTo('/search')"/>
  <div class="info container center full">
      <div class="columns site-stats">
        <div class="column half cleft">
          <h2 class="accent tleft bold-600">
            Ready to start reviewing<br>
            your own courses?
          </h2>
          <p class="white box">
            Your experience matters! Share your thoughts on the courses you've taken
            and help other students make smarter choices. Join our community today
            and start leaving reviews that make a difference.
          </p>
          <div>
            <Button label="Sign up to write your first review " class="tleft inv-button" @click="navigateTo(isConnected() ? '/search' : '/signup')" />
          </div>
        </div>
        <div class="column half center">
          <img src="../assets/images/stars-uninsight.svg" width="467px" height="auto"  alt="⭐⭐⭐⭐⭐" class="stars-img"/>
        </div>
    </div>
  </div>
  <div class="info center">
    <h2>FAQ</h2>
    <p class="box desc">Got questions? We've got answers! Explore our frequently asked questions to learn how our
      platform works, how to get started, and why it's the best place for university course reviews. </p>
    <Accordion>
      <AccordionPanel value="0">
        <AccordionHeader>What is this platform all about? </AccordionHeader>
        <AccordionContent>
          <p class="m-0">
            This platform helps students review university courses, offering insights to help you choose the right ones.
          </p>
        </AccordionContent>
      </AccordionPanel>
      <AccordionPanel value="1">
        <AccordionHeader>Is it free to use? </AccordionHeader>
        <AccordionContent>
          <p class="m-0">
            Yes, the platform is completely free! You can browse and submit reviews without any cost.
          </p>
        </AccordionContent>
      </AccordionPanel>
      <AccordionPanel value="2">
        <AccordionHeader>How do you ensure the reviews are honest and reliable? </AccordionHeader>
        <AccordionContent>
          <p class="m-0">
            We use AI and manual moderation to ensure reviews are genuine and helpful, providing reliable feedback for students.
          </p>
        </AccordionContent>
      </AccordionPanel>
      <AccordionPanel value="3">
        <AccordionHeader>Do I need an account to leave a review?  </AccordionHeader>
        <AccordionContent>
          <p class="m-0">
            Yes, you’ll need an account to submit a review. This helps us manage and moderate content effectively and prevent spam.
          </p>
        </AccordionContent>
      </AccordionPanel>
      <AccordionPanel value="4">
        <AccordionHeader>Are the reviews anonymous?  </AccordionHeader>
        <AccordionContent>
          <p class="m-0">
            Reviews are not publicly linked to your account, ensuring your privacy while still keeping the content trustworthy.
          </p>
        </AccordionContent>
      </AccordionPanel>
    </Accordion>
  </div>

  <Footer />


</template>

<style scoped>
.info {
  width: 70vw;
  max-width: 1100px;
  margin-top: 200px;
}

.full {
  width: 95vw;
  max-width: none;
  background: var(--primary);
  color: var(--background);
  padding: 6rem;
}

.white {
  color: var(--background);
}

.panels {
  gap: 24px;
}

.panel {
  padding: 24px;
}

.long-bg {
  height: 190vw;
}

.site-stats {
  margin-top: 4rem;
  gap: 6vw;
}

.cleft {
  justify-content: flex-start;
}

.inv-button {
  display: inline-block;
  width: auto;
  height: auto;
  flex-shrink: 0;
  background: var(--accent);
  border-color: var(--accent);
  color: var(--primary);
}

.inv-button:hover {
  background: var(--accent-hover);
  border-color: var(--accent-hover);
  color: var(--primary);
}

.inv-button:focus {
  background: var(--accent-focus);
  border-color: var(--accent-focus);
  color: var(--primary);
}

.recent-rev {
  width: 500vw;
  padding: 0;
}

.reviews {
  padding: 0;
  width: 100%;
}
</style>