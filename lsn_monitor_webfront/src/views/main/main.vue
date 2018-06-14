<template>
  <div style="margin-top: 40px;">
    <div>
    <p>
        <h3>请选择时间范围</h3>
        开始时间<input type="date" :max="this.endTime" value="" v-model="startTime" id="startTime" />
        结束时间<input type="date" :min="startTime" :max="this.maxTime" v-model="endTime"  id="endTime"/>
     </p>
        <button v-on:click="monitor_info">查询状态</button>
    </div>
    <p v-show="showTishi">{{tishi}}</p>
    <div>
        <h3>在线节点数：</h3>
        <span class="col-md-10">{{ node_online }}</span>
        <h3>新增节点数：</h3>
        <span class="col-md-10">{{ node_new }}</span>
        <h3>线路连接数：</h3>
        <span class="col-md-10">{{ connection_count }}</span>
        <h3>最大转发级数：</h3>
        <span class="col-md-10">{{ maximum_forwarding_series }}</span>
        <h3>切换等待时延：</h3>
        <span class="col-md-10">{{ switched_wait_delay }}</span>

    </div>
  </div>
</template>

<script>
    import {setCookie,getCookie} from '../../assets/js/cookie.js'
    export default{
        data(){
            return{
                node_online: '0',
                node_new: '0',
                connection_count: '0',
                maximum_forwarding_series: '0',
                switched_wait_delay: '0',
                showTishi: false,
                tishi: ""
            }
        },
        mounted(){
          this.monitor_info()
        },
        methods:{
            monitor_info(){
                // URLSearchParams对象是为了让参数以form data形式
                let params = new URLSearchParams();
                params.append('startTime', this.startTime);
                params.append('endTime', this.endTime);
                this.axios.post("http://199.188.206.242:8888/lsn/monitor/monitor_info",params)
                .then((res)=>{
                    var data = res.data.data
                    if(res.data.code == 200){
                        this.showTishi = true
                        this.tishi = res.data.message
                        this.node_online = data.node_online
                        this.node_new = data.node_new
                        this.connection_count = data.connection_count
                        this.maximum_forwarding_series = data.maximum_forwarding_series
                        this.switched_wait_delay = data.switched_wait_delay
                        setTimeout(function(){
                            this.$router.push("/main")
                        }.bind(this),100)
                    }else if(res.data.code == 201){
                        this.tishi = res.data.message
                        this.showTishi = true
                        setTimeout(function(){
                            this.$router.push("/main")
                        }.bind(this),100)
                    }
                })
            }
        }

    }
</script>

<style>
    .login-wrap{text-align:center;}
    input{display:block; width:250px; height:40px; line-height:40px; margin:0 auto; margin-bottom: 10px; outline:none; border:1px solid #888; padding:10px; box-sizing:border-box;}
    p{color:red; white-space:nowrap; }
    button{display:block; width:250px; height:40px; line-height: 40px; margin:0 auto; border:none; background-color:#41b883; color:#fff; font-size:16px; margin-bottom:5px;}
    span{cursor:pointer;}
    span:hover{color:#41b883;}
</style>
