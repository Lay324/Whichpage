<template>
    <div id="list_page">
        <div id="search_bar">
            <el-input
                class="search_part"
                placeholder="请输入论文编号"
                v-model="page_isbn"
                clearable
            >
            </el-input>
            <el-input
                class="search_part"
                placeholder="请输入论文名"
                v-model="page_name"
                clearable
            >
            </el-input>
            <el-input
                class="search_part"
                placeholder="请输入关键词"
                v-model="page_tag"
                clearable
            >
            </el-input>
            <el-button @click.native="search_page" plain>搜索</el-button>
            <el-upload
                action=""
                :http-request="search_image"
                :show-file-list="false"
            >
                <el-button id="img_scan" plain>图片识别</el-button>
            </el-upload>
        </div>

        <div id="table_part">
            <el-table
                :data="page_data"
                v-loading="loading"
                element-loading-text="图片识别中，请勿操作..."
                stripe
            >
                <el-table-column
                    prop="isbn"
                    label="论文编号"
                    width="100"
                    align="center"
                ></el-table-column>
                <el-table-column
                    prop="title"
                    label="论文名"
                    width="280"
                    align="center"
                    show-overflow-tooltip
                ></el-table-column>
                <el-table-column
                    prop="tag"
                    label="关键词"
                    width="280"
                    align="center"
                    show-overflow-tooltip
                ></el-table-column>
                <el-table-column
                    prop="favorite_num"
                    label="收藏数"
                    align="center"
                    show-overflow-tooltip
                    sortable="custom"
                >
                </el-table-column
                >
                <el-table-column align="center">
                    <template slot-scope="scope">
                        <div class="op_list">
                            <i
                                class="iconfont icon-detail"
                                title="详细"
                                @click="go_detail(scope.row.isbn)"
                            ></i>
                            <i
                                class="el-icon-star-off icon-favorite"
                                title="收藏"
                                v-if="user_id !== null && user_id !== undefined"
                                @click="go_favorite(scope.row.isbn)"
                            ></i>
                        </div>
                    </template>
                </el-table-column>
            </el-table>
        </div>

        <div id="page_part">
            <el-button :class="{ show_btn: !isShowPre }" plain @click="go_pre"
                >上一页</el-button
            >
            <span>当前第{{ now_page }}页 / 共{{ total_page }}页</span>
            <el-button :class="{ show_btn: !isShowNext }" plain @click="go_next"
                >下一页</el-button
            >
        </div>
    </div>
</template>

<script>
import { createWorker } from "tesseract.js";

export default {
    name: "Listpage",

    data() {
        return {
            user_id: localStorage.getItem("userId"),
            now_page: 1,
            total_page: 1,
            isShowPre: true,
            isShowNext: true,
            page_isbn: "",
            page_name: "",
            page_tag: "",
            page_data: [],
            loading: false,
        };
    },

    created() {
        if (localStorage.getItem("now_page")) {
            this.now_page = localStorage.getItem("now_page");
            localStorage.removeItem("now_page");
        }

        if (localStorage.getItem("tag")) {
            this.page_tag = localStorage.getItem("tag");
            this.search_page();
            localStorage.removeItem("tag");
        } else {
            this.show_page();
        }
    },

    watch: {
        now_page: {
            handler(newValue) {
                if (newValue == 1) {
                    this.isShowPre = false;
                } else {
                    this.isShowPre = true;
                }

                if (newValue == this.total_page) {
                    this.isShowNext = false;
                } else {
                    this.isShowNext = true;
                }
            },

            immediate: true,
        },
    },

    methods: {
        search_page() {
            // let target = e.target;
            // if (target.nodeName == "SPAN") {
            //     target = target.parentNode;
            // }
            // target.blur();
            this.show_page();
        },

        go_detail(isbn) {
            // console.log(isbn);
            localStorage.setItem("now_page", this.now_page);
            this.$router.push({ name: "detailpage", params: { isbn } });
        },

        go_favorite(isbn) {
            // console.log(isbn);
            this.$axios({
                method: "POST",
                url: `/favorite/${this.user_id}/${isbn}`,
            }).then((re) => {
                if (re.data.errno === 0) {
                    this.$message({
                        message: "收藏成功！",
                        type: "success",
                    });
                } else {
                    this.$message.error("您已收藏该论文");
                }
            });
        },

        go_pre(e) {
            let target = e.target;
            if (target.nodeName == "SPAN") {
                target = target.parentNode;
            }
            target.blur();

            this.now_page--;

            this.show_page();
        },

        go_next(e) {
            let target = e.target;
            if (target.nodeName == "SPAN") {
                target = target.parentNode;
            }
            target.blur();

            this.now_page++;

            this.show_page();
        },

        show_page() {
            // if (this.isbn.length < 10) {

            // }

            let data = {
                isbn: this.page_isbn,
                title: this.page_name,
                tag: this.page_tag,
            };

            this.$axios({
                method: "post",
                url: `/page/search/${this.now_page}`,
                data: data,
            }).then((re) => {
                console.log(re);
                if (re.data.errno == 0) {
                    let { data } = re.data;
                    this.page_data = data.pages;
                    this.total_page = data.total_num;

                    if (this.total_page == 0 || this.total_page == 1) {
                        this.total_page = 1;
                        this.isShowNext = false;
                    } else if (this.total_page == this.now_page) {
                        this.isShowNext = false;
                    } else {
                        this.isShowNext = true;
                    }
                }
            });
        },

        async search_image(obj) {
            this.loading = true;
            const worker = createWorker();
            const image = obj.file;

            await worker.load();
            await worker.loadLanguage("eng");
            await worker.initialize("eng");

            const {
                data: { text },
            } = await worker.recognize(image);
            await worker.terminate();

            const image_num = text.replace(/[^0-9]/gi, "");
            this.page_isbn = image_num;
            this.loading = false;
            this.show_page();
        },
    },
};
</script>

<style scoped>
#list_page {
    /* border: 1px red solid;
    box-sizing: border-box; */
    height: 100%;
    width: 77%;
}

#search_bar {
    /* border: 1px red solid;
    box-sizing: border-box; */
    display: flex;
    justify-content: center;
    width: 80%;
    height: 12%;
    margin: 0 auto;
    margin-top: 4%;
}

#img_scan {
    margin-left: 10px;
}

.el-input {
    width: 20%;
    margin-right: 5%;
}

.search_part >>> .el-input__suffix {
    height: 40px;
}

.search_part >>> .el-input__inner {
    border-color: #033;
    border-radius: 10px;
}

.el-button {
    border-color: #033;
    color: #033;
    font-weight: bold;
    border-radius: 10px;
    height: 40px;
}

.el-button:hover {
    color: #fcfdf5;
    background-color: #033;
}

#table_part {
    /* border: 1px red solid;
    box-sizing: border-box; */
    width: 70%;
    margin: 0 auto;
}

.op_list {
    display: flex;
    justify-content: center;
    align-items: center;
}

.iconfont {
    font-size: 24px;
    margin: 0 4%;
    color: #033;
}

.icon-favorite {
    font-size: 20px;
    margin: 0 4%;
    color: #033;
}

.iconfont:hover {
    cursor: pointer;
}

.icon-detail:hover {
    color: #fe7419;
}

.icon-favorite:hover {
    color: #d237d0;
    cursor: pointer;
}

.icon-delete:hover {
    color: #dd2b1e;
}

#page_part {
    /* border: 1px red solid;
    box-sizing: border-box; */
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 40%;
    margin: 0 auto;
    margin-top: 3%;
    color: #033;
}

.show_btn {
    visibility: hidden;
}
</style>

<style>
.el-table th,
.el-table tr {
    color: #033;
    background-color: #9ecca4;
}

.el-table__empty-block {
    background-color: #fcfdf5;
}

.el-table--striped .el-table__body tr.el-table__row--striped td {
    background-color: #9ecca4;
}

.el-table td,
.el-table th.is-leaf {
    border-bottom: 1px #033 solid;
}

.el-table__header-wrapper {
    background-color: #9ecca4;
}

.el-table {
    color: #033;
}

.el-table__row {
    background-color: #fcfdf5 !important;
}

.el-table__row:hover > td {
    background-color: #fcfdf5 !important;
}

.el-table__row--striped:hover > td {
    background-color: #9ecca4 !important;
}

.el-table .cell {
    white-space: nowrap;
}
</style>