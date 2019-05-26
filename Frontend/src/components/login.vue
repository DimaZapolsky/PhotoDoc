<template>
    <form id="login" v-on:submit.prevent="login" align="center">
        <h1>Вход</h1>
        <div class="inputFields">
            <span class="error" v-if="empty">*Все поля должны быть заполнены.</span>
            <span class="error" v-if="incorrect">*Логин или пароль введены не верно.</span>
            <div class="user-input-wrp">
                <br/>
                <input
                        type="text"
                        class="input"
                        id="loginField"
                        name="username"
                        ref="username"
                        v.model="input.username"
                        v-on:change="updateUsername"
                        autofocus
                        required>
                <span class="floating-label">Логин</span>
            </div>
            <div class="user-input-wrp">
                <br/>
                <input
                        type="password"
                        class="input"
                        id="passwordField"
                        name="password"
                        ref="password"
                        v.model="input.password"
                        v-on:change="updatePassword"
                        autocomplete="off"
                        required/>
                <span class="floating-label">Пароль</span>
            </div>
            <button class="button" id="loginButton" form="login" type="submit"><span>Вход</span></button>
        </div>
        <button class="button" id="registerButton" form="login" type="button" v-on:click="toRegisterPage()">Еще нет аккаунта? Зарегистрируйтесь!</button>
    </form>
</template>

<script>
    import axios from 'axios';
    export default {
        name: 'Login',
        data() {
            return {
                empty: true,
                incorrect: false,
                info: "",
                input: {
                    username: null,
                    password: null
                }
            }
        },
        methods: {
            login() {
                if (!(this.input.username && this.input.password)) {
                    if (!this.input.username) {
                        this.$refs.username.focus()
                    } else {
                        this.$refs.password.focus()
                    }
                } else {
                    var this_ = this;
                    axios.post('http://127.0.0.1:5000/api/sign_in/', {username: this.input.username,
                        password: this.input.password})
                        .then(function (response) {
                            localStorage.token = response.data.token;
                            this_.$emit("authenticated", true);
                            this_.$router.replace({ name: "secure" });
                        }).catch(function (error) {
                        console.log(error);
                        this_.incorrect = true;
                    });

                }
            },
            toRegisterPage() {
                this.$router.replace({ name: "register" });
            },
            updateUsername(event) {
                this.input.username = event.target.value;
                this.incorrect = false;
                if (this.input.username == "" || this.input.password == "") {
                    this.empty = true;
                }
                else {
                    this.empty = false;
                }
            },
            updatePassword(event) {
                this.input.password = event.target.value;
                this.incorrect = false;
                if (this.input.username == "" || this.input.password == "") {
                    this.empty = true;
                }
                else {
                    this.empty = false;
                }
            }
        }
    }
</script>

<style scoped>
    #login {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: space-around;
        width: 30%;
        min-width: 300px;
        border: 1px solid #CCCCCC;
        background-color: #FFFFFF;
        margin: auto;
        margin-top: 5vh;
        height: 80vh;
        min-height: 350px;
        padding: 20px;
        font-size: 20px;
        font-family: 'Roboto', sans-serif;
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
    }

    .input {
        font-size: 20px;
        font-family: 'Roboto', sans-serif;
        border-left: 0px;
        border-right: 0px;
        border-top: 0px;
        border-bottom: 1px solid #3A78DE;
    }

    .button {
        width: 75%;
        font-size: 20px;
        font-family: 'Roboto', sans-serif;
        color: #FFFFFF;
        background-color: #FFF;
        border-radius: 2px;
        margin-top: 10px;
        padding: 4px;
        border: 0px;
        margin: 10px;
        cursor: pointer;
        outline: none !important;
    }

    button:hover {
        opacity: 0.8;
    }

    button:focus {
        outline: none !important
    }

    #loginButton {
        width: 75%;
        background-color: #3A78DE;
        color: white;
        box-shadow: 0.1em 0.1em 5px rgba(122,122,122,0.5);
        transition: all 0.5s;
        cursor: pointer;
    }
    #loginButton span {
        cursor: pointer;
        display: inline-block;
        position: relative;
        transition: 0.5s;
    }

    #loginButton span:after {
        content: '\00bb';
        position: absolute;
        opacity: 0;
        top: 0;
        right: -20px;
        transition: 0.5s;
    }

    #loginButton:focus span,
    #loginButton:hover span {
        padding-right: 25px;
    }

    #loginButton:focus span:after,
    #loginButton:hover span:after {
        opacity: 1;
        right: 0;
    }

    #registerButton{
        margin-top: 10px;
        text-align: left;
        font-size: 15px;
        font-family: 'Roboto', sans-serif;
        color: #3A78DE;
    }

    input:focus {
        outline: none !important;
    }

    .inputFields {
        width: 100%;
        display: flex;
        align-items: center;
        flex-direction: column;
    }

    .user-input-wrp {
        font-size: 17px;
        font-family: 'Roboto', sans-serif;
        position: relative;
        width: 75%;
    }

    .user-input-wrp .input{
        width: 100%;
        outline: none;
        border:none;
        border-bottom: 1px solid #3A78DE;
    }

    .user-input-wrp .input:invalid {
        box-shadow: none !important;
        border-bottom: 1px solid red;
    }

    .user-input-wrp .input:focus{
        border-width: medium medium 2px;
    }

    .user-input-wrp .floating-label {
        position: absolute;
        pointer-events: none;
        top: 30px;
        left: 5px;
        transition: 0.2s ease all;
        color: #777;
    }

    .user-input-wrp input:focus ~ .floating-label,
    .user-input-wrp input:not(:focus):valid ~ .floating-label{
        top: 5px;
        left: 0px;
        font-size: 13px;
        font-family: 'Roboto', sans-serif;
        opacity: 1;
        color: #000;
    }

    .error {
        font-size: 10px !important;
        font-family: 'Roboto', sans-serif;
        width: 75%;
        color: red;
        text-align: left;
    }
</style>
