<script setup lang="ts">
// Just a home page! Informational
</script>

<template>
  <h3>Welcome to runway!</h3>
  (where all the models strut their stuff &#x1f31d;)
  <div class="mt-4"><strong><u>Overview</u></strong></div>
  <div class="mt-4 mw-50">
    <strong>runway</strong> is a proof-of-concept project to explore the idea of a highly interactive, mobile-friendly, web-based platform
    for the construction and sharing of datasets and machine learning models.
  </div>
  <div class="mt-4"><strong><u>Architecture</u></strong></div>
  <div class="mt-4 mw-50">
    Technologies used include:
    <ul>
      <li><a href="https://vuejs.org/" target="_blank" ref="noopener">Vue.js</a> for the front end</li>
      <li><a href="https://flask.palletsprojects.com/en/2.2.x/" target="_blank" ref="noopener">Flask</a> for the REST API</li>
      <li><a href="https://www.sqlalchemy.org/" target="_blank" ref="noopener">SQLAlchemy</a> to communicate with the back end database</li>
      <li><a href="https://www.postgresql.org/" target="_blank" ref="noopener">PostgreSQL</a> for back-end storage</li>
      <li><a href="https://auth0.com/" target="_blank" ref="noopener">Auth0</a> to handle user management and authentication</li>
      <li><a href="https://scikit-learn.org/stable/" target="_blank" ref="noopener">scikit-learn</a> for machine learning</li>
    </ul>
  </div>
  <div class="mt-4"><strong><u>Take a look</u></strong></div>
  <div class="mt-4 mw-50">
    <ul>
      <li><RouterLink to="/datasets">Datasets</RouterLink> to view and create datasets</li>
      <li><RouterLink to="/models">Models</RouterLink> to view and create models</li>
      <li>NOTE: you must be logged in to create or download datasets and models!</li>
    </ul>
  </div>
</template>
