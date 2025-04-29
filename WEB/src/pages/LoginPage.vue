<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { Notify } from 'quasar'
import loginUser from "../api/auth/loginRequest.js";

const router = useRouter()

const login = ref('')
const password = ref('')
const loading = ref(false)

const authorisation = async () => {

  loading.value = true

  try {
    const accessToken = await loginUser({
      login: login.value,
      password: password.value
    })

    localStorage.setItem('access_token', accessToken)

    Notify.create({
      type: 'positive',
      message: 'Успешный вход!'
    })

    router.push('/dashboard')
  } catch (error) {
    Notify.create({
      type: 'negative',
      message: error.message || 'Ошибка входа'
    })
  } finally {
    loading.value = false
  }
}
</script>


<template>
  <div class="fullscreen flex flex-center bg-grey-2">
    <q-card class="q-pa-lg shadow-2" style="width: 350px">
      <q-card-section>
        <div class="text-h6 text-center">Вход</div>
      </q-card-section>

      <q-card-section>
        <q-form @submit.prevent="authorisation">
          <q-input
              v-model="login"
              type="text"
              label="Логин"
              dense
              outlined
              autofocus
              class="q-mb-md"
              lazy-rules="ondemand"
              :rules="[ val => (val && val.length > 0) || 'Введите логин' ]"
          />
          <q-input
              v-model="password"
              type="password"
              label="Пароль"
              dense
              outlined
              class="q-mb-lg"
              lazy-rules="ondemand"
              :rules="[ val => (val && val.length > 0) || 'Введите пароль' ]"
          />

          <q-btn
              label="Войти"
              type="submit"
              color="primary"
              class="full-width"
              :loading="loading"
          />
        </q-form>
      </q-card-section>
    </q-card>
  </div>
</template>

<style scoped>
.fullscreen {
  height: 100vh;
}
</style>
