<template>
  <q-layout view="lHh Lpr lFf" class="bg-violet-strong text-dark">
    <q-header elevated class="bg-transparent">
      <q-tabs
          v-model="tab"
          class="text-white"
          active-color="white"
          indicator-color="white"
          align="justify"
          dense
          animated
          @update:model-value="loadData"
      >
        <q-tab name="users" label="Пользователи" />
        <q-tab name="teams" label="Команды" />
        <q-tab name="projects" label="Проекты" />
        <q-tab name="contests" label="Конкурсы" />
      </q-tabs>
    </q-header>

    <q-page-container class="q-pa-md">
      <q-tab-panels v-model="tab" animated transition-prev="slide-right" transition-next="slide-left">

        <!-- Пользователи -->
        <q-tab-panel name="users">
          <div class="violet-card q-pa-md">
            <q-table
                title="Пользователи"
                :rows="users"
                :columns="userColumns"
                row-key="id"
                @row-click="openEdit('users', $event)"
                :loading="loadingUsers"
                dense
                flat
            />
          </div>
        </q-tab-panel>

        <!-- Команды -->
        <q-tab-panel name="teams">
          <div class="violet-card q-pa-md">
            <q-table
                title="Команды"
                :rows="teams"
                :columns="teamColumns"
                row-key="id"
                @row-click="openEdit('teams', $event)"
                :loading="loadingTeams"
                dense
                flat
            />
          </div>
        </q-tab-panel>

        <!-- Проекты -->
        <q-tab-panel name="projects">
          <div class="violet-card q-pa-md">
            <q-table
                title="Проекты"
                :rows="projects"
                :columns="projectColumns"
                row-key="id"
                @row-click="openEdit('projects', $event)"
                :loading="loadingProjects"
                dense
                flat
            />
          </div>
        </q-tab-panel>

        <!-- Конкурсы -->
        <q-tab-panel name="contests">
          <div class="violet-card q-pa-md">
            <q-table
                title="Конкурсы"
                :rows="contests"
                :columns="contestColumns"
                row-key="id"
                @row-click="openEdit('contests', $event)"
                :loading="loadingContests"
                dense
                flat
            />
          </div>
        </q-tab-panel>

      </q-tab-panels>
    </q-page-container>

    <!-- Модальное окно редактирования -->
    <q-dialog v-model="dialogVisible" persistent>
      <q-card style="min-width: 350px; max-width: 700px;">
        <q-card-section>
          <div class="text-h6">Редактирование {{ dialogType }}</div>
        </q-card-section>

        <q-separator />

        <q-card-section>
          <pre>{{ dialogData }}</pre>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Закрыть" color="primary" @click="closeDialog" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-layout>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'

// Импорты API
import fetchTeams from '@/api/teams/getTeams.js'
import fetchUsers from '@/api/users/getUsers.js'
import fetchProjects from '@/api/projects/getProjects.js'
import fetchContests from '@/api/contests/getContests.js'
import updateTeam from '@/api/teams/updateTeam.js'

// Активная вкладка
const tab = ref('users')

// Данные
const users = ref([])
const teams = ref([])
const projects = ref([])
const contests = ref([])

// Загрузка
const loadingUsers = ref(false)
const loadingTeams = ref(false)
const loadingProjects = ref(false)
const loadingContests = ref(false)

// Колонки
const userColumns = [
  { name: 'id', label: 'ID', field: 'id', sortable: true },
  { name: 'name', label: 'Имя', field: 'name', sortable: true },
  { name: 'email', label: 'Email', field: 'email', sortable: true },
]

const teamColumns = [
  { name: 'title', label: 'Название команды', field: 'title', sortable: true },
  { name: 'description', label: 'Описание', field: 'description', sortable: true },
  { name: 'logo', label: 'Логотип', field: 'logo', sortable: true },
  { name: 'git_url', label: 'Git URL', field: 'git_url', sortable: true },
]


const projectColumns = [
  { name: 'id', label: 'ID', field: 'id', sortable: true },
  { name: 'projectName', label: 'Проект', field: 'projectName', sortable: true },
]

const contestColumns = [
  { name: 'id', label: 'ID', field: 'id', sortable: true },
  { name: 'contestName', label: 'Конкурс', field: 'contestName', sortable: true },
]

// Модалка
const dialogVisible = ref(false)
const dialogData = ref({})
const dialogType = ref('')

// Функция открытия редактирования
function openEdit(type, row) {
  dialogType.value = type
  // Клонируем объект, чтобы не менять данные в таблице до сохранения
  dialogData.value = JSON.parse(JSON.stringify(row))
  dialogVisible.value = true
}

// Функция сохранения изменений
async function saveChanges() {
  if (dialogType.value === 'teams') {
    try {
      await updateTeam(dialogData.value)
      // Обновляем локальные данные команды
      const index = teams.value.findIndex(t => t.id === dialogData.value.id)
      if (index !== -1) {
        teams.value[index] = JSON.parse(JSON.stringify(dialogData.value))
      }
      closeDialog()
    } catch (error) {
      console.error('Ошибка при сохранении:', error.message)
      // Можно добавить уведомление об ошибке
    }
  }
}

// Закрыть модалку
function closeDialog() {
  dialogVisible.value = false
}

// Загрузка данных
async function loadData(name) {
  switch (name) {
    case 'users':
      loadingUsers.value = true
      try {
        users.value = await fetchUsers() || []
      } catch (error) {
        users.value = []
        console.error(error.message)
      } finally {
        loadingUsers.value = false
      }
      break

    case 'teams':
      loadingTeams.value = true
      try {
        teams.value = await fetchTeams() || []
      } catch (error) {
        teams.value = []
        console.error(error.message)
      } finally {
        loadingTeams.value = false
      }
      break

    case 'projects':
      loadingProjects.value = true
      try {
        projects.value = await fetchProjects() || []
      } catch (error) {
        projects.value = []
        console.error(error.message)
      } finally {
        loadingProjects.value = false
      }
      break

    case 'contests':
      loadingContests.value = true
      try {
        contests.value = await fetchContests() || []
      } catch (error) {
        contests.value = []
        console.error(error.message)
      } finally {
        loadingContests.value = false
      }
      break
  }
}

// Начальная загрузка
onMounted(() => loadData(tab.value))

// Загрузка при смене вкладки
watch(tab, (newTab) => {
  loadData(newTab)
})
</script>

<style scoped>
.bg-violet-strong {
  background: linear-gradient(135deg, #4f046f 0%, #7c3aed 100%);
  min-height: 100vh;
}

.violet-card {
  border-radius: 22px;
  background: #ede9fe;
  box-shadow: 0 6px 32px rgba(124, 58, 237, 0.13), 0 1.5px 6px rgba(124, 58, 237, 0.10);
}
</style>
