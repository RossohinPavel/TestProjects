<template>
  <div class="about">
    <h1>Информация о пользователе</h1>
    <h2>Имя: <span>{{ first_name }}</span></h2>
    <h2>Фамилия: <b>{{ last_name }}</b></h2>
    <h2>Никнейм: <b>{{ username }}</b></h2>
    <h2>Дней до дня рождения: <b>{{ birth_date }}</b></h2>
  </div>
</template>

<style>
@media (min-width: 1024px) {
  .about {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }
}
</style>

<script>
let url = "http://localhost:8000/api/v1/0"

let response = await fetch(url);
let response_data = await response.json();

let d1 = new Date()
let d2 = new Date(response_data.birth_date)
let timeDiff = Math.abs(d1.getTime() - d2.getTime());
let diffDays = Math.ceil(timeDiff / (1000 * 3600 * 24)); 

export default { 
  data() {
    return {
      first_name: response_data.first_name,
      last_name: response_data.last_name,
      username: response_data.username,
      birth_date: diffDays,
    }
  }
}
</script>