<template>
    <div style="display: flex; flex-direction: row; justify-content: space-around;">
    <div style="max-width: 700px; width: 100%;">
        <myUploader v-if="stage == 1" url="http://127.0.0.1:5000/api/upload_photo/" max-files="1" ref="myUploader"
                                        @upload-image-success="updateImagesOk" @fileDeleted="photoIdNow = -1" />
        
        <div v-if="stage == 2" class="box">
            <b-form-group label="Выберите разрешение">
                <b-form-radio-group
                    id="dpi-radios"
                    v-model="dpi"
                    :options="dpies"
                    buttons
                    button-variant="outline-primary"
                    size="lg"
                    name="radio-btn-outline"
                ></b-form-radio-group>
            </b-form-group>
            <b-form-group label="Выберите цвет фотографии">
                <b-form-radio-group
                    id="color-radios"
                    v-model="color"
                    :options="colors"
                    buttons
                    button-variant="outline-primary"
                    size="lg"
                    name="radio-btn-outline"
                ></b-form-radio-group>
            </b-form-group>
            <b-form-group label="Выберите размер фотографии">
                <b-form-radio-group
                    id="size-radios"
                    v-model="size"
                    :options="sizes"
                    buttons
                    button-variant="outline-primary"
                    size="lg"
                    name="radio-btn-outline"
                ></b-form-radio-group>
            </b-form-group>
            <b-form-group label="Выберите размер бумаги">
                <b-form-radio-group
                    id="paper-radios"
                    v-model="paper"
                    :options="papers"
                    buttons
                    button-variant="outline-primary"
                    size="lg"
                    name="radio-btn-outline"
                ></b-form-radio-group>
            </b-form-group>

            <label>Выберите количество фотографий</label>
            <div style="display: flex; flex-direction: row; justify-content: space-between;">
                <input type="number" v-model="count" min="1" v-bind:max="maxPhotos" />
                <input type="range" v-model="count" min="1" v-bind:max="maxPhotos" style="width: 100%; margin-left: 10px;" />
            </div>
        </div>

        <div v-if="stage == 3" style="display: flex; flex-direction: row; justify-content: space-around; width: 100%;">
            <croppa v-model="myCroppa" :initial-image="urlNow" :prevent-white-space="true"
            :show-remove-button="false" :width="CRwidth" :height="CRheight"></croppa>
        </div>

        <div v-if="stage == 4" style="display: flex; flex-direction: column; justify-content: space-between; margin-right: 35px; margin-left: 35px;">
            <div style="display: flex; flex-direction: row; justify-content: space-around;">
                <img :src="finalUrl" :height="CRheight + 'px'" :width="CRwidth + 'px'"></img>
            </div>
            <div style="display: flex; flex-direction: row; justify-content: space-around;">
                <button class="button" id="downloadBtn" :style="'width: ' + CRwidth + 'px !important;'" v-on:click="downloadItem(finalUrl)">Скачать</button>
            </div>
        </div>

        <div style="display: flex; flex-direction: row; justify-content: space-between;">
            <button v-bind:disabled="stage == 1" id="prevBtn" class="button" v-on:click="prevStage"><span>Предыдущий шаг</span></button>
            <button v-bind:disabled="stage == 4 || photoIdNow == -1" id="nextBtn" class="button" v-on:click="nextStage"><span>Следующий шаг</span></button>
        </div>
    </div>
    </div>
</template>

<script>
    import axios from 'axios';
    import myUploader from './myUploader.vue'
    import VueSlideBar from 'vue-slide-bar'

    export default {
        components: {
            myUploader,
            VueSlideBar,
        },
        name: 'Secure',
        props: [],
        data() {
            return {
                url: '/upload',
                paramName: 'file',
                urlNow: '',
                photoIdNow: -1,
                stage: 1,
                maxPhotos: 6,
                dpi: '300px',
                dpies: ['60px', '75px', '96px', '120px', '150px', '200px', '300px', '600px'],
                sizes: ['3см x 4 см', '4см x 6см'],
                papers: ['10см x 15см', 'A4', 'A5'],
                colors: ['Цветная', 'Черно-белая'],
                size: '3см x 4 см',
                paper: '10см x 15см',
                color: 'Цветная',
                count: 1,
                slider: {
                    lineHeight: 10,
                    processStyle: {
                        backgroundColor: 'red',
                    }
                },
                myCroppa: {},
                finalUrl: '',
                //finalUrl: 'https://i.ibb.co/6w39HX7/308321-879389.jpg',
            }
        },
        methods: {
            uploadDone(files) {
                console.log('Done');
                console.log(files);
            },
            getHeaders() {
                console.log(localStorage.token);
                return {Authorization: "Token " + localStorage.token};
            },
            updateImagesOk(response) {
                if (response.data.success) {
                    this.urlNow = response.data.url;
                    this.photoIdNow = response.data.id;
                    console.log("uploaded");
                    console.log(this.photoIdNow);
                }
                else {
                    console.log(response.data.error);
                }
            },
            nextStage() {
                this.stage++;
                if (this.stage == 4) {
                    this.uploadCroppedImage();
                }
            },
            uploadFinalUrl() {
                var this_ = this;
                axios.get('http://127.0.0.1:5000/api/get_final_photo/', {params: {photoId: this.photoIdNow, color: this.color, size: this.size, paper: this.paper, count: this.count, dpi: this.dpi }, headers: {Authorization: "Token " + localStorage.token } }).then(function(response) {
                        this_.finalUrl = response.data.url;
                    }).catch(function (error) {
                        console.log(error);
                    });
            },
            prevStage() {
                this.stage--;
            },
            uploadCroppedImage() {
                this.myCroppa.generateBlob((blob) => {
                    let data = new FormData();
                    data.append('images[]', blob);
                    data.append('caption', 'image');
                    var this_ = this;
             
                    axios.post('http://127.0.0.1:5000/api/upload_cropped_photo/', data, { headers: { 'content-type': 'multipart/form-data' , Authorization: "Token " + localStorage.token, 'photoId': this.photoIdNow} }).then(function (response) {
                        this_.uploadFinalUrl();
                    }).catch(function (error) {
                        console.log(error);
                    });
                }, 'image/jpeg', 1)
            },
            getOtnosheniye() {
                if (this.size == '3см x 4 см')
                    return 3 / 4.;
                if (this.size == '4см x 6см')
                    return 4 / 6.;
            },
            download(filename) {

                var downloading = browser.downloads.download({
                    url : filename,
                    filename : 'photodoc.png',
                    conflictAction : 'uniquify'
                });
            },
            downloadItem (url) {
                axios.get(url, { responseType: 'blob' })
                    .then(({ data }) => {
                        let blob = new Blob([data], { type: 'image/png' })
                        let link = document.createElement('a')
                        link.href = window.URL.createObjectURL(blob)
                        link.download = 'image.png'
                        link.click()
                    .catch(error => {
                        console.error(error)
                    })
                })
            }
        },
        computed: {
            CRheight: function() {
                var w = window.innerWidth;
                var h = window.innerHeight;
                this.size;
                var k = this.getOtnosheniye();
                return Math.min((w * 0.6) / k, h * 0.7);
            },
            CRwidth: function() {
                var w = window.innerWidth;
                var h = window.innerHeight;
                this.size;
                var k = this.getOtnosheniye();
                return Math.min(w * 0.6, (h * 0.7) * k);
            },
        }
    }
</script>

<style scoped>
    #upload {
        background-color: black !important;
        height: 100px !important;
        width: 100px !important;
    }

    .box {
        margin-top: 20px;
        margin-right: 35px;
        margin-left: 35px;
    }

    .button {
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

    button:enabled:hover {
        opacity: 0.8;
    }

    button:enabled:focus {
        outline: none !important
    }

    #prevBtn {
        width: 75%;
        margin-left: 35px;
        background-color: #337cf6;
        color: white;
        box-shadow: 0.1em 0.1em 5px rgba(122,122,122,0.5);
        transition: all 0.5s;
        cursor: pointer;
    }

    #prevBtn:enabled span {
        cursor: pointer;
        display: inline-block;
        position: relative;
        transition: 0.5s;
    }

    #prevBtn:enabled span:before {
        content: '\00ab';
        position: absolute;
        opacity: 0;
        top: 0;
        left: -20px;
        transition: 0.5s;
    }

    #prevBtn:enabled:focus span,
    #prevBtn:enabled:hover span {
        padding-left: 25px;
    }

    #prevBtn:enabled:focus span:before,
    #prevBtn:enabled:hover span:before {
        opacity: 1;
        left: 0;
    }

    #prevBtn:disabled {
        opacity: 0.5;
    }

    #nextBtn {
        width: 75%;
        background-color: #337cf6;
        color: white;
        margin-right: 35px;
        box-shadow: 0.1em 0.1em 5px rgba(122,122,122,0.5);
        transition: all 0.5s;
        cursor: pointer;
    }

    #nextBtn:enabled span {
        cursor: pointer;
        display: inline-block;
        position: relative;
        transition: 0.5s;
    }

    #nextBtn:enabled span:after {
        content: '\00bb';
        position: absolute;
        opacity: 0;
        top: 0;
        right: -20px;
        transition: 0.5s;
    }

    #nextBtn:enabled:focus span,
    #nextBtn:enabled:hover span {
        padding-right: 25px;
    }

    #nextBtn:enabled:focus span:after,
    #nextBtn:enabled:hover span:after {
        opacity: 1;
        right: 0;
    }

    #nextBtn:disabled {
        opacity: 0.5;
    }

    #downloadBtn {
        background-color: #337cf6;
        color: white;
        box-shadow: 0.1em 0.1em 5px rgba(122,122,122,0.5);
        transition: all 0.5s;
        cursor: pointer;
        margin-bottom: 0px !important;
    }
</style>
