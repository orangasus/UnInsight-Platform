<script setup lang="ts">
import {defineProps} from "vue";

const props = defineProps({
  reviews: {
    type: Array,
    default: []
  }
});
</script>

<template>
  <div class="grid">
    <div
        class="container grid-item review center"
        v-for="review in reviews"
    >
      <Stars :rating="parseInt(review.overall_rating)" size="big"/>
      <h4 class="bold-600 box">{{review.title}}</h4>
      <p>"{{ review.body }}"</p>
      <div class="columns stats center">
        <div class="container column thirds">
          <h4 class="tcenter tcenter">{{ review.cognitive_load_rating }}/5</h4>
          <p class="gray subtext tcenter">Cognitive<br>Load</p>
        </div>
        <div class="container column thirds">
          <h4 class="tcenter">{{ review.delivery_support_rating }}/5</h4>
          <p class="gray subtext tcenter stat-name">Support</p>
        </div>
        <div class="container column thirds">
          <h4 class="tcenter">{{ review.engagement_enjoyment_rating }}/5</h4>
          <p class="gray subtext tcenter stat-name">Engagement</p>
        </div>
        <div class="container column thirds">
          <h4 class="tcenter">{{ review.usefulness_relevance_rating }}/5</h4>
          <p class="gray subtext tcenter stat-name">Usefulness</p>
        </div>
      </div>
<!--      <p class="subtext gray"><i class="pi texticon like" :class="review.liked ? 'pi-thumbs-up-fill' : 'pi-thumbs-up'"></i>3 likes</p>-->
    </div>

  </div>
</template>

<style scoped>
.review {
  padding: 32px 48px;
  text-align: left;
}

.stats {
  width: 70%;
  margin-top: 16px;
}

.stat-name {
  margin-top: 6px;
  margin-bottom: 12px;
}

.like:hover {
  cursor: pointer;
}

</style>