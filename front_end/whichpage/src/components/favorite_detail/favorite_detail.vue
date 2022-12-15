<template>
    <div id="detail_page">
        <div id="detail_btn">
            <div id="back">
                <el-button plain @click="go_home">
                    <i class="iconfont icon-back"></i>
                    返回
                </el-button>
            </div>

            <div id="edit" v-if="user_id !== null && user_id !== undefined">
                <el-button plain @click="go_edit">
                    <i class="iconfont icon-edit"></i>
                    编辑
                </el-button>
            </div>
        </div>

        <div id="detail_part">
            <div class="detail_item">
                <div class="first_color list_title">论文题目</div>
                <div class="message_part first_color">{{ page_name }}</div>
            </div>
            <div class="detail_item">
                <div class="second_color list_title">论文年份</div>
                <div class="message_part second_color">{{ page_time }}</div>
            </div>
            <div class="detail_item">
                <div class="first_color list_title">原文链接</div>
                <div class="message_part first_color">
                    <a :href="page_link" target="_blank">{{ page_link }}</a>
                </div>
            </div>
            <div class="detail_item page_abstract">
                <div class="second_color list_title">关键词组</div>
                <div class="message_part second_color">{{ page_tag }}</div>
            </div>
            <div class="detail_item page_abstract">
                <div class="first_color list_title">内容摘要</div>
                <div class="message_part first_color">{{ page_abstract }}</div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "FavoriteDetail",

    data() {
        return {
            user_id: localStorage.getItem("userId"),
            isbn: this.$route.params.isbn,
            page_name: "",
            page_time: "",
            page_link: "",
            page_tag: "",
            page_abstract: "",
        };
    },

    created() {
        this.$axios({
            method: "GET",
            url: `/page/detail/${this.user_id}/${this.isbn}`,
        }).then((re) => {
            console.log(re);
            if (re.data.errno == 0) {
                let { data } = re.data;
                this.page_abstract = data.abstract;
                this.page_tag = data.tag;
                this.page_link = data.link;
                this.page_name = data.title;
                this.page_time = data.year;
            }
        });
    },

    methods: {
        go_home() {
            this.$router.push({ name: "favorite" });
        },

        go_edit() {
            this.$router.push({
                name: "editpage",
                params: { isbn: this.isbn },
            });
        },
    },
};
</script>

<style scoped>
#detail_page {
    /* border: 1px red solid;
    box-sizing: border-box; */
    width: 100%;
}

#detail_btn {
    margin: 2% 0 0 10%;
    width: 80%;
    display: flex;
    justify-content: space-between;
}

#back > .el-button {
    border-bottom: 1px #033 solid;
    padding: 12px 20px 12px 10px;
    /* background-color: white; */
    color: #033;
    font-weight: bold;
}

#edit > .el-button {
    /* border: 1px red solid;
    box-sizing: border-box; */
    /* margin-left: 77%; */
    padding: 12px 20px 12px 10px;
    color: #033;
    font-weight: bold;
}

.iconfont {
    margin-right: 20%;
}

#detail_part {
    width: 80%;
    /* height: 60%;
    overflow: auto; */
    color: #033;
    font-weight: bold;
    margin: 0 auto;
}

.detail_item {
    display: flex;
    justify-content: space-between;
    height: 50px;
}

.list_title {
    border: 1px #033 solid;
    box-sizing: border-box;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #033;
    font-size: 18px;
    font-weight: bold;
    width: 15%;
}

.message_part {
    border: 1px #033 solid;
    box-sizing: border-box;
    display: flex;
    justify-content: center;
    padding: 1%;
    width: 85%;
    font-size: 16px;
    color: #033;
    overflow: auto;
    white-space: normal;
    word-break: break-all;
}

.first_color {
    background-color: #9ecca4;
}

.second_color {
    background-color: #fcfdf5;
}

.page_abstract {
    height: 48%;
}

.page_abstract > .message_part {
    justify-content: flex-start;
    text-align: left;
    height: 200px;
}

.el-button {
    background-color: #fcfdf5;
    border: 1px #fcfdf5 solid;
    border-radius: 0;
}

.el-button:hover {
    border-color: #033;
    border-radius: 10px;
}
</style>