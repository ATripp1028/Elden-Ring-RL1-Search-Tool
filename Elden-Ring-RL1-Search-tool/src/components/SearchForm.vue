<script setup lang="ts">
import { ref } from 'vue';

const strength = ref(10);
const dexterity = ref(10);
const intelligence = ref(10);
const faith = ref(10);
const arcane = ref(10);
</script>

<template>
  <div class="search-form">
    <div class="form-group">
      <label for="field1">Strength</label>
      <input type="text" id="field1" v-model="strength" placeholder="Enter text...">
    </div>
    
    <div class="form-group">
      <label for="field2">Dexterity</label>
      <input type="text" id="field2" v-model="dexterity" placeholder="Enter text...">
    </div>
    
    <div class="form-group">
      <label for="field3">Intelligence</label>
      <input type="text" id="field3" v-model="intelligence" placeholder="Enter text...">
    </div>
    
    <div class="form-group">
      <label for="field4">Faith</label>
      <input type="text" id="field4" v-model="faith" placeholder="Enter text...">
    </div>
    
    <div class="form-group">
      <label for="field5">Arcane</label>
      <input type="text" id="field5" v-model="arcane" placeholder="Enter text...">
    </div>
  </div>
</template>

<style scoped>
.search-form {
  width: 300px;
  padding: 20px;
  background-color: #f5f5f5;
  height: 100vh;
  position: fixed;
  left: 0;
  top: 0;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
  color: #333;
}

input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

input:focus {
  outline: none;
  border-color: #666;
  box-shadow: 0 0 3px rgba(0, 0, 0, 0.1);
}
</style>
