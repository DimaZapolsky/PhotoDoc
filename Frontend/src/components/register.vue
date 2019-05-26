<template>
    <form id="register" v-on:submit.prevent="register" align="center">
        <h1>Регистрация</h1>
        <div class="inputFields">
            <span v-if="empty" class="error">*Все поля должны быть заполнены.</span>
            <span v-if="!passwords_are_equal" class="error">*Введенные пароли должны совпадать.</span>
            <span v-if="incorrect" class="error">*Такой пользователь уже существует.</span>
            <div class="user-input-wrp">
                <br/>
                <input
                        type="text"
                        class="input"
                        id="loginField"
                        name="username"
                        reg="username"
                        v.model="input.username"
                        v-on:change="updateUsername"
                        v-on:keyup.enter="register"
                        autofocus
                        align="center"
                        required/>
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
                        v-on:keyup.enter="register"
                        autocomplete="off"
                        required/>
                <span class="floating-label">Пароль</span>
            </div>
            <div class="user-input-wrp">
                <br/>
                <input
                        type="password"
                        class="input" id="confirmPasswordField"
                        name="confirm_password"
                        ref="confirm_password"
                        v.model="input.confirm_password"
                        v-on:change="updateConfirmPassword"
                        v-on:keyup.enter="register"
                        autocomplete="off"
                        required/>
                <span class="floating-label">Подтвердите пароль</span>
            </div>
            <div class="user-input-wrp">
                <br/>
                <input
                        type="text"
                        class="input"
                        id="emailField"
                        name="email"
                        ref="email"
                        v.model="input.email"
                        v-on:change="updateEmail"
                        v-on:keyup.enter="register"
                        required/>
                <span class="floating-label">Электронная почта</span>
            </div>
            <button class="button" id="registerButton" form="register" type="button" v-on:click="register()"><span>Регистрация</span></button>
        </div>
        <button class="button" id="loginButton" form="register" type="button" v-on:click="toLoginPage()">Уже есть аккаунт? Войти.</button>
    </form>
</template>

<script>
    import axios from 'axios';
    export default {
        name: 'Register',
        data() {
            return {
                empty: true,
                correct: true,
                incorrect: false,
                passwords_are_equal: true,
                input: {
                    username: "",
                    password: "",
                    confirm_password: "",
                    email: ""
                }
            }
        },
        methods: {
            register() {
                if (!(this.input.username != "" && this.input.password != "" &&
                    this.input.confirm_password && this.input.email != "")) {
                    if (!this.input.username) {
                        this.$refs.username.focus()
                    } else if (!this.input.password) {
                        this.$refs.password.focus()
                    } else if (!this.input.confirm_password) {
                        this.$refs.confirm_password.focus()
                    } else if (!this.input.emal) {
                        this.$refs.email.focus()
                    }
                } else {
                    var this_ = this;
                    if(!this.empty) {
                        if (this.input.password != this.input.confirm_password) {
                            this.passwords_are_equal = false;
                        } else {
                            axios.post('http://127.0.0.1:5000/api/sign_up/', {username: this.input.username, password: this.input.password, email: this.input.email}).then(function (response) {
                                localStorage.clear();
                                localStorage.token = response.data.token;
                                this_.$emit("authenticated", true);
                                this_.$router.replace({ name: "secure" });
                            }).catch(function (error) {
                                console.log(error);
                                this_.incorrect = true;
                            })
                        }
                    }
                }

            },
            toLoginPage() {
                this.$router.replace({ name: "login" });
            },
            updateUsername(event) {
                this.input.username = event.target.value;
                this.incorrect = false;
                if (!(this.input.username != "" && this.input.password != "" &&
                                                    this.input.confirm_password && this.input.email != "")) {
                    this.empty = true;
                }
                else {
                    this.empty = false;
                }
            },
            updatePassword(event) {
                this.input.password = event.target.value;
                this.incorrect = false;
                if (!(this.input.username != "" && this.input.password != "" &&
                                                    this.input.confirm_password && this.input.email != "")) {
                    this.empty = true;
                }
                else {
                    this.empty = false;
                }

                if (this.input.password != this.input.confirm_password && this.input.password
                                                                        && this.input.confirm_password) {
                    this.passwords_are_equal = false;
                } else {
                    this.passwords_are_equal = true;
                }
            },
            updateConfirmPassword(event) {
                this.input.confirm_password = event.target.value;
                this.incorrect = false;
                if (!(this.input.username != "" && this.input.password != "" &&
                                                    this.input.confirm_password && this.input.email != "")) {
                    this.empty = true;
                }
                else {
                    this.empty = false;
                }

                if (this.input.password != this.input.confirm_password && this.input.password
                                                                        && this.input.confirm_password) {
                    this.passwords_are_equal = false;
                } else {
                    this.passwords_are_equal = true;
                }
            },
            updateEmail(event) {
                this.input.email = event.target.value;
                this.incorrect = false;
                if (!(this.input.username != "" && this.input.password != "" &&
                                                    this.input.confirm_password && this.input.email != "")) {
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
    #register {
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
        min-height: 450px;
        height: 80vh;
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

    #registerButton {
        width: 75%;
        background-color: #3A78DE;
        color: white;
        box-shadow: 0.1em 0.1em 5px rgba(122,122,122,0.5);
        transition: all 0.5s;
        cursor: pointer;
    }
    #registerButton span {
        cursor: pointer;
        display: inline-block;
        position: relative;
        transition: 0.5s;
    }

    #registerButton span:after {
        content: '\00bb';
        position: absolute;
        opacity: 0;
        top: 0;
        right: -20px;
        transition: 0.5s;
    }

    #registerButton:focus span,
    #registerButton:hover span {
        padding-right: 25px;
    }

    #registerButton:focus span:after,
    #registerButton:hover span:after {
        opacity: 1;
        right: 0;
    }

    #loginButton{
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
