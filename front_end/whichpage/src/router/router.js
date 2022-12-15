import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

// 引入组件
const home = () => import('../components/home.vue')
const hotpage = () => import('../components/hotpage.vue')
const favorite = () => import('../components/favorite_detail/favorite.vue')
const favorite_detail = () => import('../components/favorite_detail/favorite_detail.vue')
const insertpage = () => import('../components/insertpage.vue')
const listpage = () => import('../components/home_detail/listpage.vue')
const detailpage = () => import('../components/home_detail/detailpage.vue')
const editpage = () => import('../components/favorite_detail/editpage.vue')

const router = new VueRouter({
    mode: 'history',
    base: '',
    routes: [
        {
            path: '/',
            redirect: { name: 'home' },
        },
        {
            path: '/home',
            component: home,
            name: 'home',
            redirect: { name: 'listpage' },
            children: [
                {
                    path: 'listpage',
                    component: listpage,
                    name: 'listpage',
                },
                {
                    path: 'insertpage',
                    component: insertpage,
                    name: 'insertpage',
                },
                {
                    path: 'detailpage/:isbn',
                    component: detailpage,
                    name: 'detailpage',
                },
            ]
        },
        {
            path: '/hotpage',
            component: hotpage,
            name: 'hotpage',
        },
        {
            path: '/favorite',
            component: favorite,
            name: 'favorite',
        },
        {
            path: '/favorite/:isbn',
            component: favorite_detail,
            name: 'favorite_detail',
        },
        {
            path: '/favorite/:isbn/edit',
            component: editpage,
            name: 'editpage',
        }
    ]
})

export default router