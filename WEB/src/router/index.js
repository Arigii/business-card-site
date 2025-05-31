import { createRouter, createWebHistory } from 'vue-router'
import LoginPage from "../pages/LoginPage.vue"
import HomePage from "../pages/HomePage.vue"
import AdminPage from "../pages/AdminPage.vue"

const routes = [
    { path: '/', component: HomePage },
    { path: '/login', component: LoginPage },
    { path: '/admin', component: AdminPage }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

router.beforeEach((to, from, next) => {
    const isAuthenticated = !!localStorage.getItem('access_token')
    const userId = localStorage.getItem('user_id')

    if (to.path === '/login' && isAuthenticated) {
        next('/')
    } else if (to.path === '/admin') {
        if (isAuthenticated && userId === '1') {
            next()
        } else {
            next('/')
        }
    } else {
        next()
    }
})

export default router
