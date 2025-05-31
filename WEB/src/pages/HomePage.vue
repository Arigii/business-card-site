<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'



const router = useRouter()

// Реактивное вычисление статуса авторизации
const isAuthenticated = computed(() => !!localStorage.getItem('access_token'))

const goToLogin = () => router.push('/login')
const logout = () => {
  localStorage.removeItem('access_token')
  router.go(0) // Принудительное обновление страницы для обновления состояния
}
</script>

<template>
  <div class="home-page q-pa-md q-gutter-md">
    <h4 class="text-center">Добро пожаловать!</h4>

    <div v-if="isAuthenticated" class="q-gutter-sm">
      <q-btn label="Редактировать профиль" color="secondary" />
      <q-btn label="Выход" color="negative" @click="logout" />
    </div>

    <q-btn
        v-else
        label="Авторизация"
        color="primary"
        @click="goToLogin"
    />
  </div>
</template>

<style scoped>
.home-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  gap: 20px;
}
</style>