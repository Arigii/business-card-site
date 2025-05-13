import {createRouter, createWebHistory} from 'vue-router'
import LoginPage from "../pages/LoginPage.vue"
import HomePage from "../pages/HomePage.vue"

const routes = [
    {
        path: '/',
        component: HomePage
    },
    {path: '/login', component: LoginPage}
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

router.beforeEach((to, from, next) => {
    const isAuthenticated = !!localStorage.getItem('access_token')

    if (to.path === '/login' && isAuthenticated) {
        next('/')  // теперь редирект на главную страницу
    } else {
        next()
    }
})

export default router
