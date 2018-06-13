<template>
	<div>
		<h3>所有注册用户</h3>
		<ul>
			<li v-for="item in list">
				{{item.username}}
			</li>
		</ul>
		<a href="/" v-on:click="quit">注销登入</a>
	</div>
</template>

<script>
	export default{
		data(){
			return{
				list:""
			}
		},
		mounted(){
			this.axios.get("http://127.0.0.1:5000/main").then(
				(res)=>{
					this.list = res.data
					console.log(res)
					console.log(res.data)
				}
			)
		},
		methods:{
			quit(){
				delCookie("username")
			}
		}
	}
</script>

<style>
	ul{padding: 0;}
	ul li{list-style: none;}
</style>