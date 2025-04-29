import { createApp } from 'vue'
import App from './App.vue'
import { Quasar, Notify, Dialog, Loading, QInput, QBtn, QForm, QCard, QCardSection } from 'quasar'
import router from './router'

import '@quasar/extras/material-icons/material-icons.css'


import 'quasar/src/css/index.sass'

const app = createApp(App)

app.use(Quasar, {
    plugins: { Notify, Dialog, Loading }, // уведомления, диалоги, загрузка
    components: { QInput, QBtn, QForm, QCard, QCardSection } // обязательно указать используемые компоненты
})

app.use(router)
app.mount('#app')
