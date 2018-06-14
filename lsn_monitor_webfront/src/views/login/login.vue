
<template>
    <div>
        <div class="login-wrap" v-show="showLogin">
            <h3>登陆</h3>
            <p v-show="showTishi">{{tishi}}</p>
            <input type="text" placeholder="请输入用户名" v-model="username"/>
            <input type="password" placeholder="请输入密码" v-model="password"/>
            <button v-on:click="login">登入</button>
            <!--<span v-on:click="ToRegister">没有账号?马上注册</span>-->
        </div>
        <!--<div class='register-wrap' v-show="showRegister">
            <h3>注册</h3>
            <p v-show="showTishi">{{tishi}}</p>
            <input type="text" placeholder="请输入用户名" v-model="newUsername"/>
            <input type="text" placeholder="请输入密码" v-model="newPassword" />
            <button v-on:click="register">注册</button>
            <span v-on:click="ToLogin">已有账号?马上登入</span>
        </div>-->
    </div>
</template>

<script>
    import {setCookie,getCookie} from '../../assets/js/cookie.js'
    export default{
        data(){
            return{
                result: '',
                username: '',
                password: '',
                newUsername: '',
                newPassword: '',
                tishi: '',
                showTishi: false,
                showLogin: true,
                showRegister: false
            }
        },
        mounted(){
            if(getCookie("username")){
                this.$router.push('/home')
            }
        },
        methods:{
            login(){
                if(this.username==""||this.password==""){
                    alert("请输入用户名或者密码")
                }else{
                    // URLSearchParams对象是为了让参数以form data形式
                    let params = new URLSearchParams();
                    params.append('username', this.username);
                    params.append('password', this.password);
                    this.axios.post("http://199.188.206.242:8888/lsn/admin/login",params)
                    .then((res)=>{
                        var data = res.data
                        if(data.status == 1){
                            alert(data.message)
                            this.tishi = res.message
                            this.showTishi = true
                            setCookie("username",this.username,1000*60)
                            setTimeout(function(){
                                this.$router.push("/main")
                            }.bind(this),100)
                        }else{
                            alert(data.message)
                            this.tishi = res.message
                            this.showTishi = true
                            setTimeout(function(){
                                this.$router.push("/")
                            }.bind(this),100)
                        }
                    })
                }
            }
        }
    }
</script>

<style>
    .login-wrap{text-align:center;}
    input{display:block; width:250px; height:40px; line-height:40px; margin:0 auto; margin-bottom: 10px; outline:none; border:1px solid #888; padding:10px; box-sizing:border-box;}
    p{color:red;}
    button{display:block; width:250px; height:40px; line-height: 40px; margin:0 auto; border:none; background-color:#41b883; color:#fff; font-size:16px; margin-bottom:5px;}
    span{cursor:pointer;}
    span:hover{color:#41b883;}
</style>
