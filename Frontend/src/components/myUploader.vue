<template>
    <div class="myUploadBox">
        <div  class="vue_component__upload--image" v-bind:class="{ 'dragover': onDragover  }">
            <span style="font-family: 'Roboto', sans-serif;" class="error" v-if="total>max_files"> Вы не можете загрузить больше {{max_files}} фотографий</span>
            <form style="height: auto; min-height: 65vh; cursor: pointer; display: flex; flex-direction: column; justify-content: space-around; align-content: center;" v-bind:id="'upload_image_form--' + input_id" enctype="multipart/form-data">
                    <div style="height: auto; width: auto;">
                        <div  v-if="total==0" class="image"></div>
                            <span style="font-family: 'Roboto', sans-serif;font-size: 20px !important; color: black !important; height: 50px;" v-if="total == 0" id="id">
                                                                                Переместите сюда ваши фото или просто нажмите</span>
                   

                        <div class="upload_image_form__thumbnails">
                            <div style="height: 20px;" v-for="(value, key) in files" class="upload_image_form__thumbnail" v-on:click="fileView($event, key)"
                                 v-bind:class="{ 'uploaded': value.uploaded, 'bad-size': value.bad_size }" >
                                <span id="id1" v-on:click="fileDelete($event, key)">
                                &#x2716;
                                </span>
                                <img v-bind:src="image[key]" v-bind:class="{ 'show': image[key]}">
                            </div>
                        </div>
                        <input type="file" v-bind:id="'upload_image_form__input--' + input_id" hidden multiple />
                    </div>
                
            </form>
            <!-- <div id="buttons">
                <button style="width: 110px; height: 40px; margin-right: 25px; background-color: #4b82d7; color: white" type="submit"
                        v-bind:class="button_class"
                        v-on:click="submit"
                        v-bind:disabled="onUploading"
                        v-html="button_ok"></button>
                <button style="width: 110px; height: 40px; margin-right: 10px; background-color: grey; color: white" type="submit"
                        v-bind:class="button_class"
                        v-bind:disabled="onUploading"
                        v-on:click="close"
                        v-html="button_cansel"></button>
            </div> -->
        </div>
    </div>
</template>

<script>
    import axios from 'axios';

    export default {
        name: 'upload-image',
        props: {
            my_header: {
                type: [Object],
                default: () => {return {Authorization: "Token " + localStorage.token};}
            },
            input_id: {
                type: String,
                required: false,
                default: "default"
            },
            url: {
                type: String,
                required: true,
                default: null
            },
            name: {
                type: String,
                required: false,
                default: 'images[]'
            },
            max_batch: {
                type: Number,
                required: false,
                default: 0
            },
            max_files: {
                type: Number,
                required: false,
                default: 1000
            },
            max_filesize: {
                type: Number,
                required: false,
                default: 8000
            },
            resize_enabled: {
                type: Boolean,
                required: false,
                default: false
            },
            resize_max_width: {
                type: Number,
                required: false,
                default: 800
            },
            resize_max_height: {
                type: Number,
                required: false,
                default: 600
            },
            button_cansel: {
                type: String,
                required: false,
                default: 'Отмена'
            },
            button_ok: {
                type: String,
                required: false,
                default: 'Загрузить'
            },
            button_class: {
                type: String,
                required: false,
                default: 'btn btn-primary'
            }
        },
        data: function(){
            return {
                form: null,
                input: null,
                index: 0,
                total: 0,
                files: {},
                image: {},
                batch: {},
                onDragover: false,
                onUploading: false
            }
        },
        mounted: function(){
            this.form = document.getElementById('upload_image_form--' + this.input_id);
            this.input = document.getElementById('upload_image_form__input--' + this.input_id);
            ['drag', 'dragstart', 'dragend',
                'dragover', 'dragenter', 'dragleave', 'drop'].forEach(event => this.form.addEventListener(event, (e) => {
                e.preventDefault(); e.stopPropagation();
            }));
            ['dragover', 'dragenter']
                .forEach(event => this.form.addEventListener(event, this.dragEnter));
            ['dragleave', 'dragend', 'drop']
                .forEach(event => this.form.addEventListener(event, this.dragLeave));
            ['drop']
                .forEach(event => this.form.addEventListener(event, this.fileDrop));
            ['change']
                .forEach(event => this.input.addEventListener(event, this.fileDrop));
            this.form.addEventListener('click', (e) => {
                this.input.click();
            });
        },
        methods: {
            _can_xhr(){
                if(this.total > this.max_files){
                    return false;
                }
                return true;
            },
            _can_upload_file(key){
                let file = this.files[key];
                if(file.attempted || file.bad_size){
                    return false;
                }
                return true;
            },
            _xhr: function(formData, keys, callback){
                const this_ = this;
                this.onUploading = true;
                this.$emit('upload-image-attempt');
                keys.forEach((key) => {
                    this.$set(this.files[key], 'attempted', true);
                });
                axios({method: 'post', url:this.url, data:formData, headers:this.my_header}).then((response) => {
                    keys.forEach((key) => {
                        this.$set(this.files[key], 'uploaded', true);
                    });
                    this.$emit('upload-image-success', response);
                }, (response) => {
                    this.$emit('upload-image-failure', [formData, response]);
                }).then((response) => {
                    this.onUploading = false;
                    callback();
                });
            },
            upload: function(){
                if(!this._can_xhr()) {
                    return false;
                }
                this.$emit('set-files-num', Object.keys(this.files).length);
                for (let key in this.files) {
                    if(!this._can_upload_file(key)) continue;
                    let formData = new FormData();
                    formData.append(this.name, this.files[key].file, this.files[key].name);
                    this._xhr(formData, [key], this.upload);
                    return true;
                }
                this.$emit('upload-image-finish');

            },
            upload_batch: function(){
                if(!this._can_xhr()) return false;
                for (let key in this.batch) {
                    this._xhr(this.batch[key].form, this.batch[key].keys, this.upload_batch);
                    delete this.batch[key];
                    return true;
                }
            },
            create_batch: function(){
                let index = 0;
                let count = 0;
                this.batch = {};
                for (let key in this.files) {
                    if(!this._can_upload_file(key)) continue;
                    if(this.batch[index] == null || count == this.max_batch){
                        index++;
                        count = 0;
                        this.batch[index] = {form:new FormData(), keys:[]};
                    }
                    count++;
                    this.batch[index]['keys'].push(key);
                    this.batch[index]['form'].append(this.name, this.files[key].file, this.files[key].name);
                }
            },
            submit: function(e){
                this.$emit('start-upload');
                e.preventDefault(); e.stopPropagation();
                if(!this.onUploading){
                    if(this.max_batch > 1){
                        this.create_batch();
                        return this.upload_batch();
                    }
                    this.upload();
                    this.$emit('closeModal');
                    this.$emit('upload-image-finish');
                }
            },
            dragEnter: function(e){
                e.preventDefault();
                this.onDragover = true;
            },
            dragLeave: function(e){
                e.preventDefault();
                this.onDragover = false;
            },
            fileDrop: function(e){
                e.preventDefault();
                var prev = this.total;
                let newFiles = e.target.files || e.dataTransfer.files;
                for(let i = 0; i < newFiles.length && this.total < 1; i++){
                    this.$set(this.files, this.index, newFiles[i]);
                    if (newFiles[i].type.match(/image.*/)) {
                        this.fileInit(this.index);
                        this.fileRead(this.index);
                        this.index++;
                        this.total++;
                    };
                }
                e.target.value = '';
                if (this.total == 1 && prev == 0) {
                    this.submit(e);
                }
            },
            fileInit: function(key){
                let file = this.files[key];
                this.files[key] = {
                    name: this.files[key].name,
                    file: this.files[key]
                };
                if((file.size * 0.001) > this.max_filesize){
                    this.$set(this.files[key], 'bad_size', true);
                }
            },
            fileRead: function(key){
                let reader = new FileReader();
                reader.addEventListener("load", (e) => {
                    this.$set(this.image, key, reader.result);
                    if(this.resize_enabled) {
                        let imager = new Image();
                        imager.onload = () => {
                            let width = imager.width;
                            let height = imager.height;
                            if(width > this.resize_max_width || height > this.resize_max_height) {
                                if ((height / width) - (this.resize_max_height / this.resize_max_width) > 0) {
                                    width = this.resize_max_height / height * width;
                                    height = this.resize_max_height;
                                } else {
                                    height = this.resize_max_width / width * height;
                                    width = this.resize_max_width;
                                }
                            }
                            let canvas = document.createElement("canvas");
                            canvas.width = width;
                            canvas.height = height;
                            let ctx = canvas.getContext("2d");
                            ctx.drawImage(imager, 0, 0, width, height);
                            let newImageData = canvas.toDataURL("image/png");
                            this.$set(this.image, key, newImageData);
                            //
                            let img = atob(newImageData.split(',')[1]);
                            let img_buffer = [];
                            let i = 0;
                            while (i < img.length) {
                                img_buffer.push(img.charCodeAt(i));
                                i++;
                            }
                            let u8Image = new Uint8Array(img_buffer);
                            this.$set(this.files, key, {name:this.files[key].name ,file: new Blob([ u8Image ], {filename:this.files[key].name})});
                        };
                        imager.src = reader.result;
                    }
                });
                reader.readAsDataURL(this.files[key].file);
            },
            fileDelete: function(e, key){
                this.total--;
                this.$emit('fileDeleted');
                this.$delete(this.files, key);
                this.$delete(this.image, key);
            },
            fileView: function(e, key){
                e.preventDefault(); e.stopPropagation();
            },
            close: function(e) {
                e.preventDefault(); e.stopPropagation();
                this.$emit('closeModal');
            },
            resetUploader() {
                this.index = 0;
                this.total = 0;
                this.files = {};
                this.image = {};
                this.batch = {};
                this.onDragover = false;
                this.onUploading = false;
                //this.$emit('closeModal');
            }

        }
    }
</script>

<style lang="css" scoped>
    .vue_component__upload--image{
        padding: 5px;
        min-height: 80px;
        border-radius: 5px;
        background-color: #EEE;
        border-top: black;
    }

    .vue_component__upload--image.dragover{}
    .vue_component__upload--image form > div{
        text-align: center;
    }
    .vue_component__upload--image .upload_image_form__thumbnails{
        margin-bottom: 1em;
    }
    .vue_component__upload--image .upload_image_form__thumbnail{
        border-radius: 2.5px;
        position:relative;
        width:30%;
        padding:30% 0 0;
        overflow: hidden;
        margin:5px;
        display:inline-block;
    }
    .upload_image_form__thumbnail span {
        display: none;
    }
    .upload_image_form__thumbnail:hover span {
        display: block;
    }
    .vue_component__upload--image .upload_image_form__thumbnail img{
        position: absolute;
        top:50%;
        left: 50%;
        min-width: 100%;
        min-height: 100%;
        max-height: 150%;
        opacity: 0;
        transform: translateX(-50%) translateY(-50%);
        transition: 1s opacity;
    }
    .vue_component__upload--image .upload_image_form__thumbnail img.show{
        opacity: 1;
    }
    .vue_component__upload--image .upload_image_form__thumbnail img:hover{
        filter: blur(2px);

    }
    .vue_component__upload--image .upload_image_form__thumbnail.bad-size img{
        filter: grayscale(100%);
    }
    .vue_component__upload--image .upload_image_form__thumbnail.uploaded img{
        opacity: 1;
    }
    .vue_component__upload--image .upload_image_form__thumbnail span{
        position: absolute;
        top: -2px;
        left: 0px;
        z-index: 100;
        padding: 0px 1px;
        border-radius: 2px;
        background-color: grey;
    }

    form {
        background-color: #EEE;
        text-align: center;
        display: flex;
        flex-flow: column;
        height: 100%;
        margin-top: 30px;
        margin-left: 30px;
        margin-right: 30px;
        margin-bottom: 5px;
        border: 4px dashed #4b82d7 !important;
    }
    div.image:before {
        content:url(https://i.ibb.co/Z81HczQ/Webp-net-resizeimage-3.png);
    }
    #headerUpload {
        display: flex;
        flex-direction: row;
        align-content: center;
        justify-content: space-between;
        margin-bottom: 5px;
        font-size: 25px;
        font-family: 'Roboto', sans-serif;
    }
    #buttons {
        margin-right: 10px;
        display: flex;
        flex-direction: row-reverse;
    }
    .error {
        font-size: 15px;
        font-family: 'Roboto', sans-serif;
        width: 75%;
        color: red;
        text-align: left;
    }
</style>
