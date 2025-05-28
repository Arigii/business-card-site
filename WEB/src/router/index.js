import {createRouter, createWebHistory} from 'vue-router'
import LoginPage from "../pages/LoginPage.vue"
import HomePage from "../pages/HomePage.vue"
import AdminPage from "../pages/AdminPage.vue"
import { isAuthenticated, getUserRole } from "../utils/auth.js"

const routes = [
    {
        path: '/',
        component: HomePage
    },
    {
        path: '/login',
        component: LoginPage
    },
    {
        path: '/admin',
        component: AdminPage,
        meta: { requiresAuth: true, requiresAdmin: true }
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

router.beforeEach((to, from, next) => {
    const authenticated = isAuthenticated()

    // Если переходим на страницу логина и уже авторизованы
    if (to.path === '/login' && authenticated) {
        next('/')
        return
    }

    // Проверка доступа к админ-панели
    if (to.meta.requiresAdmin) {
        if (!authenticated) {
            next('/login')
            return
        }

        const userRole = getUserRole()
        if (userRole !== 'admin') {
            // Редирект на главную, если не админ
            next('/')
            return
        }
    }

    next()
})

export default router