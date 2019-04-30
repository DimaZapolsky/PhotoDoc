<template>
    <div id="app">

        <link href="https://fonts.googleapis.com/css?family=Roboto" rel="stylesheet">

        <b-navbar v-if="authenticated" toggleable="md" type="light" variant="light" class="navBar">

            <b-navbar-brand style="color: black; font-family: 'Roboto', sans-serif; font-size: 30px !important;">PHOTODOC</b-navbar-brand>

                <b-navbar-nav class="ml-auto">

                    <div class="iconDiv" v-on:click="logout" id="logoutDiv">
                        <div><img src="https://i.ibb.co/nLqCDNy/logout-512.png" class="iconImg"></div>
                        <span class="iconText">Выйти</span>
                    </div>

                </b-navbar-nav>
     
            </b-navbar>
   
        <div v-if="authenticated" class="greeting">
            <div style="margin-top: 70px !important"><img src="https://i.ibb.co/mcD9xj1/2.png" class="greetingImg"></div>
            <span style="margin-top: 30px; font-size: 32px !important;" class="greetingText">ЗДЕСЬ БУДЕТ САЙТ</span>
            </span>
        </div>
        <router-view @authenticated="setAuthenticated" ref="child"/>

    </div>
</template>

<script>
    import axios from 'axios';

    export default {
        name: 'App',
        data() {
            return {
                authenticated: false,
                token: undefined,
            }
        },
        components: {},
        watch: {},
        mounted() {
            var this_ = this;

            if (localStorage.hasOwnProperty('cnt')) {
                this.cnt = localStorage.cnt;
            }
            else {
                this.cnt = 0;
                localStorage.cnt = 0;
            }
            if (localStorage.hasOwnProperty('token')) {
                this.token = localStorage.token;
                this.authenticated = true;
            }
            if(!this.authenticated) {
                this.$router.replace({ name: "login" });
            }
            else {
                this.$router.replace({name: "secure"});
            }
        },
        methods: {
            updateToken () {
                document.getElementsByClassName('myUploadBox')[0].__vue__.$props.my_header = {Authorization: "Token " + localStorage.token};
            },
            setAuthenticated(status) {
                this.authenticated = status;
            },
            logout() {
                var this_ = this;
                axios.post('http://0.0.0.0:81/api/sign_out/', {Authorization: "Token " + String(localStorage.token)}).then(function () {
                    this_.authenticated = false;
                    this_.$router.replace({ name: "login" });
                    delete localStorage.token;
                });
            },
        },
    }
</script>

<style>
    body {
        background-color: #EEEEEE !important;
    }
    h1 {
        padding: 0;
        margin-top: 0;
    }

    .active {
        background-color: #4CAF50;
        color: white;
    }

    button:hover {
        opacity: 0.8;
    }

    .dropAreaDragging{
        background-color: #ccc;
    }

    .navBar {
        border-bottom: 2px solid #3A78DE;
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
    }

    
    #userImg {
        padding-bottom: 8px;
        height: 45px;
        width: auto;
    }

    .iconDiv {
        /*border: 1px solid grey;*/
        cursor: pointer;
        margin-top: 10px;
        margin-bottom: 10px;
        margin-left: 5px;
        margin-right: 30px;
        display: flex;
        flex-direction: row;
        text-align: center;
    }

    #logoutDiv {
        margin-right: 10px !important;
    }

    .iconDiv:hover {
        background-color: rgba(58, 120, 222, 0.05) !important;
    }

    .iconText {
        font-weight: 100;
        font-family: 'Roboto', sans-serif;
        font-size: 17px;
        margin-left: 10px;
        margin-right: 10px;
    }

    .iconImg {
        width: 20px;
        height: 15px;
        margin-left: 0px;
    }

    .userImg {
        width: 20px;
        height: 20px;
        margin-left: 5px;
        margin-right: 3px;
    }

    #dropUser:hover .dropdown-menu{
        margin-top: 0;
        display: block;
    }

    .greeting {
        display: flex;
        flex-direction: column;
        text-align: center;
    }

    .greetingImg {
        width: auto !important;
        max-width: 90vw;
        height: auto;
        max-height: 90vh;
    }

    .greetingText {
        font-weight: 100;
        font-family: 'Roboto', sans-serif;
        font-size: 19px;
    }

</style>