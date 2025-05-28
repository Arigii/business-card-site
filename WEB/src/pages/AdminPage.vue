<template>
  <div class="q-pa-md">
    <q-card>
      <q-card-section>
        <div class="text-h4 q-mb-md">
          <q-icon name="admin_panel_settings" class="q-mr-sm" />
          Управление данными
        </div>

        <!-- Навигационные вкладки -->
        <q-tabs
            v-model="activeTab"
            dense
            class="text-grey"
            active-color="primary"
            indicator-color="primary"
            align="justify"
            narrow-indicator
        >
          <q-tab name="team" label="Команда" />
          <q-tab name="members" label="Участники" />
          <q-tab name="contests" label="Конкурсы" />
          <q-tab name="projects" label="Проекты" />
          <q-tab name="achievements" label="Достижения" />
        </q-tabs>
      </q-card-section>

      <q-separator />

      <q-card-section>
        <q-tab-panels v-model="activeTab">

          <!-- Управление командой -->
          <q-tab-panel name="team">
            <div class="text-h5 q-mb-md">Информация о команде</div>

            <q-form @submit="onSubmitTeam" class="q-gutter-md">
              <div class="row q-gutter-md">
                <div class="col-12 col-md-6">
                  <q-input
                      filled
                      v-model="teamForm.name"
                      label="Название команды *"
                      lazy-rules
                      :rules="[val => val && val.length > 0 || 'Поле обязательно']"
                  />
                </div>

                <div class="col-12 col-md-5">
                  <q-file
                      filled
                      bottom-slots
                      v-model="teamForm.logo"
                      label="Логотип команды"
                      counter
                      accept=".jpg, .png, .jpeg, image/*"
                  >
                    <template v-slot:prepend>
                      <q-icon name="cloud_upload" @click.stop.prevent />
                    </template>
                    <template v-slot:append>
                      <q-icon name="close" @click.stop.prevent="teamForm.logo = null" class="cursor-pointer" />
                    </template>
                  </q-file>
                </div>
              </div>

              <q-input
                  filled
                  type="textarea"
                  v-model="teamForm.description"
                  label="Краткое описание команды *"
                  lazy-rules
                  :rules="[val => val && val.length > 0 || 'Поле обязательно']"
                  rows="3"
              />

              <q-input
                  filled
                  v-model="teamForm.giteaUrl"
                  label="URL профиля команды на Gitea"
                  hint="Например: https://gitea.example.com/team"
              />

              <div>
                <q-btn label="Сохранить изменения" type="submit" color="primary"/>
                <q-btn label="Очистить" type="reset" color="primary" flat class="q-ml-sm" />
              </div>
            </q-form>
          </q-tab-panel>

          <!-- Управление участниками -->
          <q-tab-panel name="members">
            <div class="row justify-between items-center q-mb-md">
              <div class="text-h5">Участники команды</div>
              <q-btn color="primary" label="Добавить участника" @click="showAddMemberDialog" />
            </div>

            <!-- Список участников -->
            <q-list bordered separator>
              <q-item v-for="member in members" :key="member.id" clickable v-ripple>
                <q-item-section avatar>
                  <q-avatar>
                    <img :src="member.avatar || '/api/placeholder/40/40'" />
                  </q-avatar>
                </q-item-section>

                <q-item-section>
                  <q-item-label>{{ member.fullName }}</q-item-label>
                  <q-item-label caption>{{ member.role || 'Участник' }}</q-item-label>
                  <q-item-label caption>{{ member.email }}</q-item-label>
                </q-item-section>

                <q-item-section side>
                  <div class="text-grey-8 q-gutter-xs">
                    <q-btn class="gt-xs" size="12px" flat dense round icon="edit" @click="editMember(member)" />
                    <q-btn class="gt-xs" size="12px" flat dense round icon="delete" color="negative" @click="deleteMember(member.id)" />
                  </div>
                </q-item-section>
              </q-item>
            </q-list>
          </q-tab-panel>

          <!-- Управление конкурсами -->
          <q-tab-panel name="contests">
            <div class="row justify-between items-center q-mb-md">
              <div class="text-h5">Конкурсы</div>
              <q-btn color="primary" label="Добавить конкурс" @click="showAddContestDialog" />
            </div>

            <!-- Список конкурсов -->
            <div class="row q-gutter-md">
              <q-card v-for="contest in contests" :key="contest.id" class="col-12 col-md-5">
                <q-img
                    :src="contest.image || '/api/placeholder/300/200'"
                    style="height: 140px"
                >
                  <div class="absolute-bottom">
                    <div class="text-h6">{{ contest.name }}</div>
                  </div>
                </q-img>

                <q-card-section>
                  <div class="text-caption text-grey">{{ contest.year }}</div>
                  <div class="text-body2 q-mt-sm">{{ contest.description?.substring(0, 100) }}...</div>
                </q-card-section>

                <q-card-actions>
                  <q-btn flat color="primary" label="Редактировать" @click="editContest(contest)" />
                  <q-btn flat color="negative" label="Удалить" @click="deleteContest(contest.id)" />
                </q-card-actions>
              </q-card>
            </div>
          </q-tab-panel>

          <!-- Управление проектами -->
          <q-tab-panel name="projects">
            <div class="row justify-between items-center q-mb-md">
              <div class="text-h5">Проекты</div>
              <q-btn color="primary" label="Добавить проект" @click="showAddProjectDialog" />
            </div>

            <!-- Список проектов -->
            <q-list bordered separator>
              <q-item v-for="project in projects" :key="project.id" clickable v-ripple>
                <q-item-section>
                  <q-item-label>{{ project.name }}</q-item-label>
                  <q-item-label caption>{{ project.description }}</q-item-label>
                  <q-item-label caption>
                    <q-chip v-for="tech in project.technologies" :key="tech" size="sm" color="primary" text-color="white">
                      {{ tech }}
                    </q-chip>
                  </q-item-label>
                </q-item-section>

                <q-item-section side>
                  <div class="text-grey-8 q-gutter-xs">
                    <q-btn class="gt-xs" size="12px" flat dense round icon="edit" @click="editProject(project)" />
                    <q-btn class="gt-xs" size="12px" flat dense round icon="delete" color="negative" @click="deleteProject(project.id)" />
                  </div>
                </q-item-section>
              </q-item>
            </q-list>
          </q-tab-panel>

          <!-- Управление достижениями -->
          <q-tab-panel name="achievements">
            <div class="row justify-between items-center q-mb-md">
              <div class="text-h5">Достижения и курсы</div>
              <q-btn color="primary" label="Добавить достижение" @click="showAddAchievementDialog" />
            </div>

            <!-- Список достижений -->
            <q-list bordered separator>
              <q-item v-for="achievement in achievements" :key="achievement.id" clickable v-ripple>
                <q-item-section>
                  <q-item-label>{{ achievement.title }}</q-item-label>
                  <q-item-label caption>{{ achievement.description }}</q-item-label>
                  <q-item-label caption>{{ achievement.date }} • {{ achievement.type }}</q-item-label>
                </q-item-section>

                <q-item-section side>
                  <div class="text-grey-8 q-gutter-xs">
                    <q-btn class="gt-xs" size="12px" flat dense round icon="edit" @click="editAchievement(achievement)" />
                    <q-btn class="gt-xs" size="12px" flat dense round icon="delete" color="negative" @click="deleteAchievement(achievement.id)" />
                  </div>
                </q-item-section>
              </q-item>
            </q-list>
          </q-tab-panel>

        </q-tab-panels>
      </q-card-section>
    </q-card>

    <!-- Dialog для добавления/редактирования участника -->
    <q-dialog v-model="memberDialog">
      <q-card style="min-width: 400px">
        <q-card-section>
          <div class="text-h6">{{ editingMember ? 'Редактировать участника' : 'Добавить участника' }}</div>
        </q-card-section>

        <q-card-section class="q-pt-none">
          <q-form @submit="onSubmitMember" class="q-gutter-md">
            <q-input
                filled
                v-model="memberForm.fullName"
                label="ФИО *"
                lazy-rules
                :rules="[val => val && val.length > 0 || 'Поле обязательно']"
            />

            <q-input
                filled
                v-model="memberForm.email"
                label="Email *"
                type="email"
                lazy-rules
                :rules="[
                val => val && val.length > 0 || 'Поле обязательно',
                val => /.+@.+\..+/.test(val) || 'Введите корректный email'
              ]"
            />

            <q-input
                filled
                v-model="memberForm.role"
                label="Роль в команде"
                hint="Например: Frontend разработчик, Team Lead"
            />

            <q-input
                filled
                type="textarea"
                v-model="memberForm.bio"
                label="Краткая информация"
                rows="3"
            />

            <q-file
                filled
                v-model="memberForm.avatar"
                label="Фото профиля"
                accept=".jpg, .png, .jpeg, image/*"
            />

            <q-input
                filled
                v-model="memberForm.giteaUsername"
                label="Username на Gitea"
            />

            <div>
              <q-btn label="Сохранить" type="submit" color="primary"/>
              <q-btn label="Отмена" v-close-popup flat class="q-ml-sm" />
            </div>
          </q-form>
        </q-card-section>
      </q-card>
    </q-dialog>

    <!-- Dialog для добавления/редактирования конкурса -->
    <q-dialog v-model="contestDialog">
      <q-card style="min-width: 500px">
        <q-card-section>
          <div class="text-h6">{{ editingContest ? 'Редактировать конкурс' : 'Добавить конкурс' }}</div>
        </q-card-section>

        <q-card-section class="q-pt-none">
          <q-form @submit="onSubmitContest" class="q-gutter-md">
            <q-input
                filled
                v-model="contestForm.name"
                label="Название конкурса *"
                lazy-rules
                :rules="[val => val && val.length > 0 || 'Поле обязательно']"
            />

            <div class="row q-gutter-md">
              <div class="col">
                <q-input
                    filled
                    v-model="contestForm.year"
                    label="Год *"
                    type="number"
                    lazy-rules
                    :rules="[val => val && val > 2000 || 'Введите корректный год']"
                />
              </div>
              <div class="col">
                <q-file
                    filled
                    v-model="contestForm.image"
                    label="Главное фото"
                    accept="image/*"
                />
              </div>
            </div>

            <q-input
                filled
                type="textarea"
                v-model="contestForm.description"
                label="Описание конкурса *"
                lazy-rules
                :rules="[val => val && val.length > 0 || 'Поле обязательно']"
                rows="4"
            />

            <q-input
                filled
                v-model="contestForm.websiteUrl"
                label="Ссылка на сайт конкурса"
                type="url"
            />

            <q-input
                filled
                v-model="contestForm.giteaRepo"
                label="Репозиторий на Gitea"
                hint="Например: team/contest-project-2024"
            />

            <q-select
                filled
                v-model="contestForm.participants"
                :options="members"
                option-value="id"
                option-label="fullName"
                label="Участники от команды"
                multiple
                use-chips
                stack-label
            />

            <div>
              <q-btn label="Сохранить" type="submit" color="primary"/>
              <q-btn label="Отмена" v-close-popup flat class="q-ml-sm" />
            </div>
          </q-form>
        </q-card-section>
      </q-card>
    </q-dialog>

    <!-- Dialog для добавления/редактирования проекта -->
    <q-dialog v-model="projectDialog">
      <q-card style="min-width: 500px">
        <q-card-section>
          <div class="text-h6">{{ editingProject ? 'Редактировать проект' : 'Добавить проект' }}</div>
        </q-card-section>

        <q-card-section class="q-pt-none">
          <q-form @submit="onSubmitProject" class="q-gutter-md">
            <q-input
                filled
                v-model="projectForm.name"
                label="Название проекта *"
                lazy-rules
                :rules="[val => val && val.length > 0 || 'Поле обязательно']"
            />

            <q-input
                filled
                type="textarea"
                v-model="projectForm.description"
                label="Описание проекта *"
                lazy-rules
                :rules="[val => val && val.length > 0 || 'Поле обязательно']"
                rows="3"
            />

            <q-select
                filled
                v-model="projectForm.technologies"
                :options="technologyOptions"
                label="Технологии"
                multiple
                use-input
                use-chips
                @new-value="createValue"
                stack-label
            />

            <div class="row q-gutter-md">
              <div class="col">
                <q-input
                    filled
                    v-model="projectForm.giteaRepo"
                    label="Репозиторий на Gitea"
                />
              </div>
              <div class="col">
                <q-input
                    filled
                    v-model="projectForm.demoUrl"
                    label="Ссылка на демо"
                    type="url"
                />
              </div>
            </div>

            <q-select
                filled
                v-model="projectForm.author"
                :options="members"
                option-value="id"
                option-label="fullName"
                label="Автор проекта"
            />

            <div>
              <q-btn label="Сохранить" type="submit" color="primary"/>
              <q-btn label="Отмена" v-close-popup flat class="q-ml-sm" />
            </div>
          </q-form>
        </q-card-section>
      </q-card>
    </q-dialog>

    <!-- Dialog для добавления/редактирования достижения -->
    <q-dialog v-model="achievementDialog">
      <q-card style="min-width: 500px">
        <q-card-section>
          <div class="text-h6">{{ editingAchievement ? 'Редактировать достижение' : 'Добавить достижение' }}</div>
        </q-card-section>

        <q-card-section class="q-pt-none">
          <q-form @submit="onSubmitAchievement" class="q-gutter-md">
            <q-input
                filled
                v-model="achievementForm.title"
                label="Название достижения/курса *"
                lazy-rules
                :rules="[val => val && val.length > 0 || 'Поле обязательно']"
            />

            <q-input
                filled
                type="textarea"
                v-model="achievementForm.description"
                label="Описание *"
                lazy-rules
                :rules="[val => val && val.length > 0 || 'Поле обязательно']"
                rows="3"
            />

            <div class="row q-gutter-md">
              <div class="col">
                <q-select
                    filled
                    v-model="achievementForm.type"
                    :options="['Достижение', 'Курс', 'Сертификат', 'Диплом']"
                    label="Тип *"
                    lazy-rules
                    :rules="[val => val && val.length > 0 || 'Поле обязательно']"
                />
              </div>
              <div class="col">
                <q-input
                    filled
                    v-model="achievementForm.date"
                    label="Дата получения"
                    type="date"
                />
              </div>
            </div>

            <q-file
                filled
                v-model="achievementForm.certificate"
                label="Скан диплома/сертификата"
                accept=".pdf,.jpg,.png,.jpeg"
            />

            <q-select
                filled
                v-model="achievementForm.owner"
                :options="members"
                option-value="id"
                option-label="fullName"
                label="Владелец достижения *"
                lazy-rules
                :rules="[val => val !== null || 'Поле обязательно']"
            />

            <div>
              <q-btn label="Сохранить" type="submit" color="primary"/>
              <q-btn label="Отмена" v-close-popup flat class="q-ml-sm" />
            </div>
          </q-form>
        </q-card-section>
      </q-card>
    </q-dialog>

  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'

export default {
  name: 'AdminDataManagement',
  setup() {
    const activeTab = ref('team')

    // Dialogs
    const memberDialog = ref(false)
    const contestDialog = ref(false)
    const projectDialog = ref(false)
    const achievementDialog = ref(false)

    // Editing states
    const editingMember = ref(false)
    const editingContest = ref(false)
    const editingProject = ref(false)
    const editingAchievement = ref(false)

    // Forms
    const teamForm = reactive({
      name: 'DevTeam',
      description: 'Команда разработчиков, специализирующаяся на создании инновационных веб-решений',
      logo: null,
      giteaUrl: 'https://gitea.example.com/devteam'
    })

    const memberForm = reactive({
      fullName: '',
      email: '',
      role: '',
      bio: '',
      avatar: null,
      giteaUsername: ''
    })

    const contestForm = reactive({
      name: '',
      year: new Date().getFullYear(),
      description: '',
      image: null,
      websiteUrl: '',
      giteaRepo: '',
      participants: []
    })

    const projectForm = reactive({
      name: '',
      description: '',
      technologies: [],
      giteaRepo: '',
      demoUrl: '',
      author: null
    })

    const achievementForm = reactive({
      title: '',
      description: '',
      type: '',
      date: '',
      certificate: null,
      owner: null
    })

    // Data
    const members = ref([
      {
        id: 1,
        fullName: 'Иван Иванов',
        email: 'ivan@example.com',
        role: 'Frontend Developer',
        avatar: '/api/placeholder/40/40'
      },
      {
        id: 2,
        fullName: 'Мария Петрова',
        email: 'maria@example.com',
        role: 'Backend Developer',
        avatar: '/api/placeholder/40/40'
      }
    ])

    const contests = ref([
      {
        id: 1,
        name: 'Хакатон IT-решений 2024',
        year: 2024,
        description: 'Региональный хакатон по разработке IT-решений для бизнеса',
        image: '/api/placeholder/300/200'
      },
      {
        id: 2,
        name: 'Web Development Challenge',
        year: 2023,
        description: 'Международный конкурс веб-разработки',
        image: '/api/placeholder/300/200'
      }
    ])

    const projects = ref([
      {
        id: 1,
        name: 'Система управления проектами',
        description: 'Веб-приложение для управления проектами команды',
        technologies: ['Vue.js', 'Node.js', 'PostgreSQL']
      },
      {
        id: 2,
        name: 'Мобильное приложение для заказа еды',
        description: 'React Native приложение с интеграцией платежных систем',
        technologies: ['React Native', 'Firebase', 'Stripe']
      }
    ])

    const achievements = ref([
      {
        id: 1,
        title: 'Сертификат Vue.js Developer',
        description: 'Успешное прохождение курса по Vue.js разработке',
        type: 'Сертификат',
        date: '2024-01-15'
      },
      {
        id: 2,
        title: '1 место в хакатоне',
        description: 'Победа в региональном хакатоне IT-решений',
        type: 'Достижение',
        date: '2024-03-20'
      }
    ])

    const technologyOptions = ref([
      'Vue.js', 'React', 'Angular', 'Node.js', 'Express', 'FastAPI',
      'PostgreSQL', 'MongoDB', 'Docker', 'Kubernetes', 'AWS', 'Azure'
    ])

    // Methods
    const onSubmitTeam = () => {
      console.log('Saving team info:', teamForm)
      // Здесь будет API вызов для сохранения информации о команде
    }

    const showAddMemberDialog = () => {
      editingMember.value = false
      resetMemberForm()
      memberDialog.value = true
    }

    const editMember = (member) => {
      editingMember.value = true
      Object.assign(memberForm, member)
      memberDialog.value = true
    }

    const onSubmitMember = () => {
      if (editingMember.value) {
        console.log('Updating member:', memberForm)
        // API вызов для обновления участника
      } else {
        console.log('Adding new member:', memberForm)
        // API вызов для добавления участника
        const newMember = { ...memberForm, id: Date.now() }
        members.value.push(newMember)
      }
      memberDialog.value = false
      resetMemberForm()
    }

    const deleteMember = (id) => {
      members.value = members.value.filter(m => m.id !== id)
      console.log('Deleting member:', id)
    }

    const resetMemberForm = () => {
      Object.assign(memberForm, {
        fullName: '',
        email: '',
        role: '',
        bio: '',
        avatar: null,
        giteaUsername: ''
      })
    }

    const showAddContestDialog = () => {
      editingContest.value = false
      resetContestForm()
      contestDialog.value = true
    }

    const editContest = (contest) => {
      editingContest.value = true
      Object.assign(contestForm, contest)
      contestDialog.value = true
    }

    const onSubmitContest = () => {
      if (editingContest.value) {
        console.log('Updating contest:', contestForm)
      } else {
        console.log('Adding new contest:', contestForm)
        const newContest = { ...contestForm, id: Date.now() }
        contests.value.push(newContest)
      }
      contestDialog.value = false
      resetContestForm()
    }

    const deleteContest = (id) => {
      contests.value = contests.value.filter(c => c.id !== id)
      console.log('Deleting contest:', id)
    }

    const resetContestForm = () => {
      Object.assign(contestForm, {
        name: '',
        year: new Date().getFullYear(),
        description: '',
        image: null,
        websiteUrl: '',
        giteaRepo: '',
        participants: []
      })
    }

    const showAddProjectDialog = () => {
      editingProject.value = false
      resetProjectForm()
      projectDialog.value = true
    }

    const editProject = (project) => {
      editingProject.value = true
      Object.assign(projectForm, project)
      projectDialog.value = true
    }

    const onSubmitProject = () => {
      if (editingProject.value) {
        console.log('Updating project:', projectForm)
      } else {
        console.log('Adding new project:', projectForm)
        const newProject = { ...projectForm, id: Date.now() }
        projects.value.push(newProject)
      }
      projectDialog.value = false
      resetProjectForm()
    }

    const deleteProject = (id) => {
      projects.value = projects.value.filter(p => p.id !== id)
      console.log('Deleting project:', id)
    }

    const resetProjectForm = () => {
      Object.assign(projectForm, {
        name: '',
        description: '',
        technologies: [],
        giteaRepo: '',
        demoUrl: '',
        author: null
      })
    }

    const showAddAchievementDialog = () => {
      editingAchievement.value = false
      resetAchievementForm()
      achievementDialog.value = true
    }

    const editAchievement = (achievement) => {
      editingAchievement.value = true
      Object.assign(achievementForm, achievement)
      achievementDialog.value = true
    }

    const onSubmitAchievement = () => {
      if (editingAchievement.value) {
        console.log('Updating achievement:', achievementForm)
      } else {
        console.log('Adding new achievement:', achievementForm)
        const newAchievement = { ...achievementForm, id: Date.now() }
        achievements.value.push(newAchievement)
      }
      achievementDialog.value = false
      resetAchievementForm()
    }

    const deleteAchievement = (id) => {
      achievements.value = achievements.value.filter(a => a.id !== id)
      console.log('Deleting achievement:', id)
    }

    const resetAchievementForm = () => {
      Object.assign(achievementForm, {
        title: '',
        description: '',
        type: '',
        date: '',
        certificate: null,
        owner: null
      })
    }

    const createValue = (val, done) => {
      if (val.length > 0) {
        if (!technologyOptions.value.includes(val)) {
          technologyOptions.value.push(val)
        }
        done(val, 'toggle')
      }
    }

    return {
      activeTab,

      // Dialogs
      memberDialog,
      contestDialog,
      projectDialog,
      achievementDialog,

      // Editing states
      editingMember,
      editingContest,
      editingProject,
      editingAchievement,

      // Forms
      teamForm,
      memberForm,
      contestForm,
      projectForm,
      achievementForm,

      // Data
      members,
      contests,
      projects,
      achievements,
      technologyOptions,

      // Methods
      onSubmitTeam,
      showAddMemberDialog,
      editMember,
      onSubmitMember,
      deleteMember,
      showAddContestDialog,
      editContest,
      onSubmitContest,
      deleteContest,
      showAddProjectDialog,
      editProject,
      onSubmitProject,
      deleteProject,
      showAddAchievementDialog,
      editAchievement,
      onSubmitAchievement,
      deleteAchievement,
      createValue
    }
  }
}
</script>

<style scoped>
.q-tab-panel {
  padding: 16px 0;
}

.q-card {
  box-shadow: 0 1px 5px rgba(0,0,0,0.2), 0 2px 2px rgba(0,0,0,0.14), 0 3px 1px -2px rgba(0,0,0,0.12);
}

.q-item-section.side {
  padding-left: 16px;
}

.text-h4, .text-h5, .text-h6 {
  font-weight: 500;
}

.q-chip {
  margin-bottom: 4px;
}

@media (max-width: 600px) {
  .gt-xs {
    display: none;
  }
}
</style>