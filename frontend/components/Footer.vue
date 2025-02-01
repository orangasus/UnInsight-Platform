<script setup lang="ts">

</script>
<template>
  <footer class="footer">
    <div class="footer-content">
      <div class="columns">
        <div class="column fourths center">
          <img src="../assets/images/uninsight-main-logo-white.svg" alt="Uninsight" width="280px" height="auto">
        </div>
        <div class="column fourths center">
          <div class="tleft l1">
            <p class="accent bold-700 link-title">Quick Links</p>
            <NuxtLink to="/" class="text-link"><p class="white link">Home</p></NuxtLink>
            <NuxtLink to="/search" class="text-link"><p class="white link">Course & Professor Search</p></NuxtLink>
          </div>
        </div>
        <div class="column fourths center l2">
          <div class="tleft">
            <p class="accent bold-700 link-title">Follow us</p>
            <NuxtLink to="/instagram" class="text-link" ><p class="white link">Instagram</p></NuxtLink>
            <NuxtLink to="/facebook" class="text-link"><p class="white link">Facebook</p></NuxtLink>
          </div>
        </div>
        <div class="column last center">
          <h3 class="accent bold-600 tright">Shaping Better<br>Choices Through<br>Honest Reviews.</h3>
        </div>
      </div>
      <div class="footer-content">
        <div class="footer-text">
          <p>Copyright © 2025 Uninsight. All rights reserved.</p>
          <div class="footer-links">
            <a href="/privacy-policy" class="footer-link">Privacy Policy</a>
            <a href="/terms-of-service" class="footer-link">Terms of Service</a>
          </div>
        </div>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.footer {
  background-color: var(--primary);
  color: var(--background);
  padding: 20px;
  text-align: center;
  font-size: 14px;
  width: 100vw;
  height: 550px;
  margin-bottom: -150px;
  margin-top: 100px;
}

.fourths {
  width: 25%;
}

.link {
  margin: 4px 0;
  line-height: 0;
  opacity: 80%;
  transition: opacity 0.2s ease-in-out;
}

.text-link {
  margin: 4px 0;
}

.link:hover {
  opacity: 100%;
}

.link-title {
  margin-bottom: 4px;
}

.l2 {
  padding-right: 340px;
}

.footer-content {
  margin-top: 150px;
  margin-bottom: 0;
  width: 100vw;
  padding: 0;
}

.footer-text {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.footer-text p {
  margin: 0;
  color: var(--background);
  opacity: 20%;
}

.footer-links {
  display: flex;
  gap: 15px;
  margin-right: 48px;
  color: var(--background);
}

.footer-link {
  color: var(--background);
  opacity: 20%;
  background: none;
}

.footer-link:hover {
  background: none;
  opacity: 40%;
}

@media (max-width: 768px) {
  .columns {
    flex-direction: column;
  }
}


</style>
