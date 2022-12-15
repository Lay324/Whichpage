<template>
    <div id="hot_page">
        <div id="chart_part">
            <div id="pie_chart" ref="pie"></div>
            <div id="radar_chart" ref="radar"></div>
        </div>
        <div id="line_chart" ref="line"></div>
    </div>
</template>

<script>
export default {
    name: "Hotpage",

    data() {
        return {
            hot_word: "",
            year: [],
            cv_data: [],
            ic_data: [],
            ec_data: [],
            pie_data: [],
            radar_tag: [],
            radar_data: [],
        };
    },

    mounted() {
        this.$axios({
            method: "GET",
            url: `/tag/pie`,
        }).then((re) => {
            console.log(re);
            if (re.data.errno == 0) {
                let { data } = re.data;
                this.pie_data = data.pie_data;
                this.radar_tag = data.radar_data;
                this.draw_pie();
            }
        });

        this.$axios({
            method: "GET",
            url: `/tag/line`,
        }).then((re) => {
            console.log(re);
            if (re.data.errno == 0) {
                let { ic_data, cv_data, hot_word, ec_data, year } =
                    re.data.data;
                this.ic_data = ic_data;
                this.cv_data = cv_data;
                this.hot_word = hot_word;
                this.ec_data = ec_data;
                this.year = year;
                this.draw_line();
            }
        });

        this.$axios({
            method: "GET",
            url: `/tag/radar`,
        }).then((re) => {
            console.log(re);
            if (re.data.errno == 0) {
                this.radar_data = re.data.data;
                this.draw_radar();
            }
        });
    },

    methods: {
        draw_pie() {
            let pie = this.$echarts.init(this.$refs.pie);
            pie.setOption({
                color: ["#879AD7", "#B1DB9E", "#FAC858", "#F29292", "#9CD3E8"],
                title: {
                    text: "总TOP5热词占比",
                    left: "4%",
                    top: "5%",
                    textStyle: {
                        color: "#033",
                    },
                },
                tooltip: {
                    trigger: "item",
                    show: true,
                    transitionDuration: 0,
                },
                legend: {
                    orient: "vertical",
                    left: "80%",
                    top: "10%",
                },
                series: [
                    {
                        type: "pie",
                        radius: "65%",
                        center: ["48%", "55%"],
                        data: this.pie_data,
                        emphasis: {
                            itemStyle: {
                                shadowBlur: 10,
                                shadowOffsetX: 0,
                                shadowColor: "rgba(0, 0, 0, 0.5)",
                            },
                        },
                    },
                ],
            });
        },

        draw_radar() {
            let radar = this.$echarts.init(this.$refs.radar);
            radar.setOption({
                color: ["#F7AE42", "#CA33A8", "#7570C7"],
                title: {
                    text: "本年三大顶会总TOP5热度对比",
                    top: "5%",
                    textStyle: {
                        color: "#033",
                    },
                },
                tooltip: {
                    confine: true,
                    enterable: true,
                    show: true,
                    transitionDuration: 0,
                },
                legend: {
                    orient: "vertical",
                    data: ["CVPR", "ICCV", "ECCV"],
                    right: "4%",
                    top: "4%",
                },
                radar: {
                    name: {
                        textStyle: {
                            color: "#FCFDF5",
                            backgroundColor: "#9ECCA4",
                            borderRadius: 3,
                            padding: [3, 5],
                        },
                    },
                    center: ["50%", "55%"],
                    indicator: this.radar_tag,
                },
                series: [
                    {
                        type: "radar",
                        data: this.radar_data,
                    },
                ],
            });
        },

        draw_line() {
            let line = this.$echarts.init(this.$refs.line);
            line.setOption({
                color: ["#3AA1FE", "#4ECB72", "#FADA57"],
                title: {
                    text: `近十年热词${this.hot_word}走势对比`,
                    left: "center",
                    top: "4%",
                    textStyle: {
                        color: "#033",
                    },
                },
                tooltip: {
                    trigger: "axis",
                    show: true,
                    transitionDuration: 0,
                },
                legend: {
                    data: ["CVPR", "ICCV", "ECCV"],
                    right: "4%",
                    top: "4%",
                },
                grid: {
                    left: "10%",
                    right: "10%",
                    bottom: "10%",
                    containLabel: true,
                },
                xAxis: {
                    type: "category",
                    data: this.year,
                },
                yAxis: {
                    type: "value",
                },
                series: [
                    {
                        name: "CVPR",
                        type: "line",
                        smooth: true,
                        stack: "1",
                        data: this.cv_data,
                    },
                    {
                        name: "ICCV",
                        type: "line",
                        smooth: true,
                        stack: "1",
                        data: this.ic_data,
                    },
                    {
                        name: "ECCV",
                        type: "line",
                        smooth: true,
                        stack: "1",
                        data: this.ec_data,
                    },
                ],
            });
        },
    },
};
</script>

<style scoped>
#hot_page {
    /* border: 1px red solid;
    box-sizing: border-box; */
    width: 100%;
    height: 90%;
    overflow: hidden;
}

#chart_part {
    /* border: 1px green solid;
    box-sizing: border-box; */
    display: flex;
    justify-content: space-between;
    width: 100%;
    height: 50%;
}

#pie_chart {
    /* border: 1px red solid;
    box-sizing: border-box; */
    width: 50%;
    height: 100%;
}

#radar_chart {
    /* border: 1px blue solid;
    box-sizing: border-box; */
    width: 50%;
    height: 100%;
}

#line_chart {
    /* border: 1px purple solid;
    box-sizing: border-box; */
    width: 100%;
    height: 50%;
}
</style>