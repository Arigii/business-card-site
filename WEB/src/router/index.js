import {createRouter, createWebHistory} from 'vue-router'
// import DashboardPage from '@/pages/DashboardPage.vue'
import LoginPage from "../pages/LoginPage.vue";
import HomePage from "../pages/HomePage.vue"; // пример

const routes = [
    {
        path: '/', component: HomePage,
        meta: {requiresAuth: true}
    },

    {path: '/login', component: LoginPage},
    // {
    //     path: '/dashboard',
    //     component: DashboardPage,
    //     meta: { requiresAuth: true } // требовать авторизацию
    // }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

// Навешиваем перехватчик навигации
router.beforeEach((to, from, next) => {
    const isAuthenticated = !!localStorage.getItem('access_token')

    if (to.meta.requiresAuth && !isAuthenticated) {
        next('/login')
    } else if (to.path === '/login' && isAuthenticated) {
        next('/dashboard')
    } else {
        next()
    }
})

export default router
