<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import { Notify } from 'quasar'
import loginUser from "../api/auth/loginRequest.js"

const router = useRouter()
const login = ref('')
const password = ref('')
const loading = ref(false)

const marqueeTrack = ref(null)
const marqueeText = ref(null)
const animationDuration = ref(7) // секунд

// Динамически рассчитываем длительность анимации в зависимости от ширины текста
const updateAnimation = () => {
  if (marqueeTrack.value && marqueeText.value) {
    const textWidth = marqueeText.value.offsetWidth
    const containerWidth = marqueeTrack.value.offsetWidth / 2
    // Скорость: 100px/sec (можно подстроить)
    const speed = 100
    animationDuration.value = (textWidth + containerWidth) / speed
    marqueeTrack.value.style.setProperty('--marquee-width', `${textWidth}px`)
    marqueeTrack.value.style.setProperty('--marquee-duration', `${animationDuration.value}s`)
  }
}

onMounted(() => {
  setTimeout(updateAnimation, 100) // Дать DOM отрисоваться
  window.addEventListener('resize', updateAnimation)
})
onBeforeUnmount(() => {
  window.removeEventListener('resize', updateAnimation)
})

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
      message: 'Успешный вход!',
      icon: 'check_circle'
    })

    router.push('/')
  } catch (error) {
    Notify.create({
      type: 'negative',
      message: error.message || 'Ошибка входа',
      icon: 'error'
    })
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="fullscreen flex flex-center bg-violet-strong">
    <q-card class="q-pa-xl shadow-violet card-animate violet-card" style="width: 370px; max-width: 92vw;">
      <q-card-section>
        <div class="marquee-outer q-mb-md">
          <div
              class="marquee-track"
              ref="marqueeTrack"
          >
            <div
                class="marquee-text text-h5 text-weight-bold text-center text-violet-strong"
                ref="marqueeText"
            >
              <q-icon name="key" size="32px" class="q-mr-sm text-violet-accent"/>
              Добро пожаловать
            </div>
            <div
                class="marquee-text text-h5 text-weight-bold text-center text-violet-strong"
            >
              <q-icon name="key" size="32px" class="q-mr-sm text-violet-accent"/>
              Добро пожаловать
            </div>
          </div>
        </div>
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
              class="q-mb-md lavender-input"
              lazy-rules="ondemand"
              :rules="[ val => (val && val.length > 0) || 'Введите логин' ]"
              :disable="loading"
              rounded
              color="deep-purple-5"
          >
            <template #prepend>
              <q-icon name="person" :color="'deep-purple-5'"/>
            </template>
          </q-input>
          <q-input
              v-model="password"
              type="password"
              label="Пароль"
              dense
              outlined
              class="q-mb-lg lavender-input"
              lazy-rules="ondemand"
              :rules="[ val => (val && val.length > 0) || 'Введите пароль' ]"
              :disable="loading"
              rounded
              color="deep-purple-5"
          >
            <template #prepend>
              <q-icon name="lock" :color="'deep-purple-5'"/>
            </template>
          </q-input>

          <q-btn
              label="Войти"
              type="submit"
              color="deep-purple-5"
              class="full-width q-mt-sm btn-rounded shimmer-btn"
              :loading="loading"
              unelevated
              size="lg"
              icon="arrow_forward"
              no-caps
              rounded
          />
        </q-form>
      </q-card-section>
    </q-card>
  </div>
</template>

<style scoped>
.bg-violet-strong {
  background: linear-gradient(135deg, #4f046f 0%, #7c3aed 100%);
  min-height: 100vh;
}

.violet-card {
  border-radius: 22px;
  background: #ede9fe;
  box-shadow: 0 6px 32px 0 rgba(124, 58, 237, 0.13), 0 1.5px 6px 0 rgba(124, 58, 237, 0.10);
}

.card-animate {
  animation: fadeInUp 0.7s cubic-bezier(.39, .575, .565, 1) both;
}
@keyframes fadeInUp {
  0% { opacity: 0; transform: translateY(40px);}
  100% { opacity: 1; transform: none;}
}

/* Бегущая строка на всю ширину карточки, без видимых полей */
.marquee-outer {
  width: 100%;
  height: 42px;
  border-radius: 14px;
  background: transparent;
  box-shadow: none;
  position: relative;
  overflow: hidden;
  display: flex;
  align-items: center;
}

.marquee-track {
  --marquee-width: 370px;
  --marquee-duration: 7s;
  display: flex;
  align-items: center;
  will-change: transform;
  animation: marquee-move var(--marquee-duration) linear infinite;
}



.marquee-text {
  display: flex;
  align-items: center;
  white-space: nowrap;
  font-family: 'Montserrat', 'Roboto', sans-serif;
  font-size: 1.25rem;
  padding: 0 1rem;
  line-height: 42px;
}

@keyframes marquee-move {
  0%   { transform: translateX(0); }
  100% { transform: translateX(calc(-1 * var(--marquee-width, 370px))); }
}

.q-input,
.q-field__control,
.q-field__native,
.q-field__inner {
  border-radius: 14px !important;
}

.btn-rounded {
  border-radius: 16px;
}

.shimmer-btn {
  position: relative;
  overflow: hidden;
  transition: box-shadow 0.2s;
}
.shimmer-btn::after {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(
      120deg,
      rgba(167, 139, 250, 0.2) 0%,
      rgba(167, 139, 250, 0.6) 50%,
      rgba(167, 139, 250, 0.2) 100%
  );
  opacity: 0;
  transition: opacity 0.3s;
  pointer-events: none;
  z-index: 1;
}
.shimmer-btn:hover::after {
  opacity: 1;
  animation: shimmer 1.2s infinite linear;
}
@keyframes shimmer {
  0% { transform: translateX(-60%) skewX(-20deg);}
  100% { transform: translateX(60%) skewX(-20deg);}
}
.shimmer-btn:hover {
  box-shadow: 0 0 18px 0 #a78bfa, 0 1.5px 6px 0 rgba(124, 58, 237, 0.10);
}
.shimmer-btn:active {
  background: #ede9fe !important;
}

.lavender-input .q-field__control,
.lavender-input .q-field__native,
.lavender-input .q-field__inner {
  background: #f6f0ff !important;
}

.text-violet-strong {
  color: #4f046f;
}
.text-violet-accent {
  color: #a78bfa;
}
</style>
