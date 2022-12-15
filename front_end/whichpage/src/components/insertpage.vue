<template>
    <div id="insert_page">
        <div class="search_part">
            <el-upload
                action=""
                :http-request="file_insert"
                :show-file-list="false"
            >
                <el-button plain>文件导入</el-button>
            </el-upload>
        </div>
        <div class="list">
            <el-table :data="insert_data" stripe>
                <el-table-column
                    prop="isbn"
                    label="论文编号"
                    width="100"
                    align="center"
                >
                </el-table-column>
                <el-table-column
                    prop="title"
                    label="论文题目"
                    width="280"
                    align="center"
                    show-overflow-tooltip
                >
                </el-table-column>
                <el-table-column
                    prop="link"
                    label="链接"
                    width="280"
                    align="center"
                    show-overflow-tooltip
                >
                </el-table-column>
                <el-table-column
                    prop="year"
                    label="年份"
                    width="280"
                    align="center"
                    show-overflow-tooltip
                >
                </el-table-column>
                <el-table-column align="center">
                    <template slot-scope="scope">
                        <el-button
                            class="insert_button"
                            plain
                            @click="insert_page(scope.row, $event)"
                            >导入</el-button
                        >
                    </template>
                </el-table-column>
            </el-table>
        </div>
    </div>
</template>

<script>
import xlsx from 'xlsx';

export default {
    name: "Insertpage",

    data() {
        return {
            page_name: "",
            insert_data: [],
        };
    },

    methods: {
        file_insert(obj) {
            const file_name = obj.file.name;
            if (!/\.(xls|xlsx)$/.test(file_name.toLowerCase())) {
                this.$message({
                    message: "请上传xls或者xlsx文件！",
                    type: "warning",
                });

                return;
            }

            const fileReader = new FileReader();
            fileReader.onload = (ev) => {
                const data = ev.target.result;
                const sheet = xlsx.read(data, {
                    type: 'binary',
                });

                const exlName = sheet.SheetNames[0];
                const exl = xlsx.utils.sheet_to_json(sheet.Sheets[exlName]);

                this.insert_data = exl;
                
            };
            fileReader.readAsBinaryString(obj.file);
        },

        insert_page(row, e) {
            let target = e.target;
            if (target.nodeName == "SPAN") {
                target = target.parentNode;
            }
            target.blur();

            const {isbn, title, link, year} = row;
            this.$axios({
                method: "POST",
                url: `/insert/add`,
                data: {
                    isbn,
                    title,
                    link,
                    year,
                }
            }).then((re) => {
                console.log(re);
                if (re.data.errno == 0) {
                    this.$message({
                        message: "导入成功",
                        type: "success",
                    });

                    this.insert_data.some((item, i) => {
                        if (item.isbn == isbn) {
                            this.insert_data.splice(i, 1);
                            return true;
                        }
                    });
                } else {
                    this.$message.error("论文库中已有该论文");
                }
            });
        },
    },
};
</script>

<style scoped>
#insert_page {
    height: 100%;
    width: 77%;
}

.search_part {
    /* border: 1px red solid;
    box-sizing: border-box; */
    display: flex;
    width: 90%;
    margin: 0 auto;
    margin-top: 5%;
    justify-content: flex-end;
    align-items: center;
}

.el-input {
    width: 30%;
    margin: 0 30px;
}

.search_part >>> .el-input__inner {
    border-color: #033;
    border-radius: 10px;
}

.el-button {
    /* border: 1px red solid;
    box-sizing: border-box; */
    margin: 0 15px;
    border-color: #033;
    border-radius: 10px;
    color: #033;
    font-weight: bold;
}

.el-button:hover {
    background-color: #033;
    color: #fcfdf5;
}

.list {
    width: 90%;
    margin: 0 auto;
    margin-top: 2%;
}

.insert_button {
    padding: 5% 10%;
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