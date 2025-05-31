import {createApp} from 'vue'
import App from './App.vue'
import router from './router'

import {
    Quasar,
    Notify,
    Dialog,
    Loading,
    QInput,
    QBtn,
    QForm,
    QCard,
    QCardSection,
    QLayout,
    QPageContainer,
    QPage,
    QTabs,
    QTab,
    QTabPanels,
    QTabPanel,
    QHeader,
    QTable,
    QSeparator,
    QCardActions,
    QDialog,
    QIcon
} from 'quasar'


import '@quasar/extras/material-icons/material-icons.css'


import 'quasar/src/css/index.sass'

const app = createApp(App)

app.use(Quasar, {
    plugins: {Notify, Dialog, Loading},
    components: {
        QInput, QBtn, QForm, QCard, QCardSection,
        QLayout, QPageContainer, QPage,
        QTabs, QTab, QTabPanels, QTabPanel, QHeader,QTable,
        QSeparator, QCardActions, QDialog, QIcon
    }
})

app.use(router)
app.mount('#app')
