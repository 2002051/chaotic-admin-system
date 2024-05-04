import {createRouter, createWebHistory} from 'vue-router'
import HomeView from '../views/HomeView.vue'
import {userInfoStore} from "@/stores/counter.js";
import {useCookies} from 'vue3-cookies'// 导入vue3使用cookies

const {cookies} = useCookies()

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: '',
            // component:
            redirect: "/home/overview"
        },
        {
            path: '/login',
            name: 'login',
            component: () => import('../views/LoginView.vue')
        },
        {
            path: '/home',
            name: 'home',
            component: () => import('../views/HomeView.vue'),
            children: [
                {
                    path: 'overview',
                    name: 'overview',
                    component: () => import('../views/OverView.vue')
                },
                {
                    path: 'book',
                    name: 'book',
                    component: () => import('../views/BookView.vue')
                },
                {
                    path: 'campus',
                    name: 'campus',
                    component: () => import('../views/CampusView.vue')
                },
                {
                    path: 'user',
                    name: 'user',
                    component: () => import('../views/user/UserView.vue')
                }, {
                    path: 'biographical',
                    name: 'biographical',
                    component: () => import('../views/user/BiographicalView.vue')
                },
                {
                    path: 'student',
                    name: 'student',
                    component: () => import('../views/user/StudentView.vue')
                },
                {
                    path: 'media',
                    name: 'media',
                    component: () => import('../views/user/MediaView.vue')
                },
                {
                    path: 'video',
                    name: 'video',
                    component: () => import('../views/user/VideoView.vue')
                },
                {
                    path: 'test',
                    name: 'test',
                    component: () => import('../views/TestView.vue')
                },
            ]
        }
    ]
})

router.beforeEach(function (to, from, next) {
    if (to.name === "login") {
        next()
        return;
    }
    let store = userInfoStore()
    if (!store.token) {
        console.log("未登录", cookies.get("info"))
        // next({name: "login"})
        router.push({name: "login"})
    } else {
        next();
    }
})

export default router
