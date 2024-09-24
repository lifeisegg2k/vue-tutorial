<script setup>
import { ref, onMounted, } from 'vue';

const name = ref('John Doe');
const status = ref('active');
const tasks = ref(['Task One', 'Task Two', 'Task Three', 'Task Four']);
const link = ref('https://google.com');

const toggleStatus = () => {
  if (status.value === 'active') {
    status.value = 'pending';
  } else if (status.value === 'pending') {
    status.value = 'inactive';
  } else {
    status.value = 'active';
  }
};

const newTask = ref('');

const addTask = () => {
  if (newTask.value.trim() !== '') {
    tasks.value.push(newTask.value);
    newTask.value = ''; // Clear input after adding task
  }
};

const deleteTask = (index) => {
  tasks.value.splice(index, 1);
};

onMounted(async () => {
  try {
    const response = await fetch('https://jsonplaceholder.typicode.com/todos');
    const data = await response.json();
    tasks.value = data.map((task) => task.title);
  } catch (error) {
    console.error('Error fetching tasks:', error);
  }
});
</script>

<template>
  <div class="flex flex-col items-center mt-10">
    <h1 class="text-2xl">{{ name }}</h1>
    <p v-if="status === 'active'" class="text-green-600">User is Active</p>
    <p v-else-if="status === 'pending'" class="text-yellow-600">
      User is Pending
    </p>
    <p v-else class="text-red-700">User is Inactive</p>
    <button
      @click="toggleStatus"
      class="mt-3 px-4 py-2 bg-blue-500 text-white rounded-md"
    >
      Change Status
    </button>
    <h3 class="text-xl my-3">Tasks:</h3>
    <ul>
      <li v-for="(task, index) in tasks" :key="index" class="flex items-center my-3">
        <span>{{ task }}</span>
        <button @click="deleteTask(index)" class="ml-2 px-3 py-1 bg-red-500 text-white rounded-md text-xs">x</button>
      </li>
    </ul>
    <a v-bind:href="link" class="text-blue-600">Link to Google</a>
  </div>
  <form @submit.prevent="addTask">
    <label for="newTask" class="block text-xl my-3">Add New Task:</label>
    <input
      type="text"
      id="newTask"
      v-model="newTask"
      class="border border-gray-300 rounded-md px-3 py-2 w-full"
    />
    <button
      type="submit"
      class="mt-3 px-4 py-2 bg-green-500 text-white rounded-md"
    >
      Add Task
    </button>
  </form>

</template>
