<template>
    <div id="navbar">
        <div id="logo">
            <img id="nav_logo" src="../assets/logo.png" alt="" />
        </div>
        <div>
            <div id="nav_button">
                <div class="nav_button_item" @click="go_home">
                    <i class="iconfont icon-home"></i>
                    <span>首页</span>
                </div>
                <div class="nav_button_item" @click="go_insert">
                    <i class="iconfont icon-insert"></i>
                    <span>论文导入</span>
                </div>
                <div class="nav_button_item" @click="go_hot">
                    <i class="iconfont icon-data"></i>
                    <span>本站聚焦</span>
                </div>
                <div
                    v-if="avatar === undefined || avatar === null"
                    class="login_button"
                    @click="go_login"
                >
                    <el-avatar icon="el-icon-user-solid" title="点击登录" />
                </div>
                <div v-else>
                    <el-dropdown>
                        <div class="login_button">
                            <el-avatar :src="avatar" />
                        </div>
                        <el-dropdown-menu slot="dropdown">
                            <el-dropdown-item @click.native="go_favorite"
                                >收藏夹</el-dropdown-item
                            >
                            <el-dropdown-item @click.native="go_logout"
                                >退出登录</el-dropdown-item
                            >
                        </el-dropdown-menu>
                    </el-dropdown>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "Navbar",

    data() {
        return {
            isLogin: false,
            avatar: localStorage.getItem("avatar"),
            client_id: "6264afefd02db33be831",
        };
    },

    mounted() {
        const search = window.location.search;
        const code = search.split("=")[1];

        if (code !== undefined) {
            this.isLogin = true;
        }

        if (this.isLogin) {
            this.get_token(code);
        }
    },

    methods: {
        get_token(code) {
            this.$axios({
                method: "POST",
                url: "/login",
                data: {
                    code,
                },
            }).then((re) => {
                const { avatar, user_id } = re.data.data;
                localStorage.setItem("avatar", avatar);
                localStorage.setItem("userId", user_id);
                this.avatar = avatar;
                const url = localStorage.getItem('url');
                window.location.href = url;
            });
        },

        go_home() {
            this.$router.push({ name: "listpage" });
        },

        go_insert() {
            this.$router.push({ name: "insertpage" });
        },

        go_hot() {
            this.$router.push({ name: "hotpage" });
        },

        go_login() {
            localStorage.setItem("url", window.location.href);
            window.location.href = `https://github.com/login/oauth/authorize?client_id=${this.client_id}`;
        },

        go_logout() {
            localStorage.clear();
            window.location.reload();
        },

        go_favorite() {
            this.$router.push({ name: "favorite" });
        },
    },
};
</script>

<style scoped>
#navbar {
    display: flex;
    justify-content: space-between;
    width: 100%;
    height: 10%;
    background-color: #cee6b4;
}

#nav_logo {
    /* border: 1px red solid; */
    width: 80px;
    margin-left: 200px;
}

#nav_button {
    display: flex;
    height: 100%;
    align-items: center;
}

.nav_button_item,
.login_button {
    display: flex;
    /* border: 1px red solid; */
    height: 100%;
    color: #003333;
    font-size: 24px;
    font-weight: bold;
    margin: 0 20px;
    padding: 0 30px;
    justify-content: center;
    align-items: center;
}

.nav_button_item:hover {
    background-color: #fcfdf5;
    cursor: pointer;
}

.login_button:hover {
    cursor: pointer;
}

.iconfont {
    /* border: 1px red solid; */
    font-size: 24px;
    margin-right: 5px;
}
</style>