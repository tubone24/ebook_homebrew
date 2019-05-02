<template>
  <div id="FileUpload">
    <div>
      <select v-model="selected" @change="onFileFormatChange">
        <option disabled value="">Please select one</option>
        <option>image/png</option>
        <option>image/jpeg</option>
        <option>image/gif</option>
      </select>
      <span>Image Format: {{ selected }}</span>
    </div>
    <div v-if="!image">
      <h2>Select images</h2>
      <input type="file" @change="onFileChange" multiple="multiple" accept="image/*">
    </div>
    <div v-else>
      <img :src="image"/>
      <button @click="removeImage">Remove images</button>
      <div v-if="selected && images">
        <button @click="postImage">Post images</button>
      </div>
    </div>
  </div>
</template>

<script>
  /* eslint-disable */
  import axios from 'axios'
  import mixins from '../mixins/const'

  const backendURL = mixins.data().backendURL;

  export default {
    name: 'FileUpload',
    data() {
      return {
        image: '',
        images: [],
        selected: ''
      }
    },
    methods: {
      async onFileChange(e) {
        console.log(e);
        let vm = this;
        const files = e.target.files || e.dataTransfer.files;
        if (!files.length)
          return;
        await this.callCreateImage(files);
        vm.ready = true;
      },
      async callCreateImage(files){
        for (let i = 0; i < files.length; i++) {
          await this.createImage(files[i]);
        }
      },
      async createImage(file) {
        const image = new Image();
        const reader = new FileReader();
        let vm = this;

        reader.onload = (e) => {
          vm.image = e.target.result;
          vm.images.push(e.target.result);
        };
        return new Promise(function (resolve, reject) {
          reader.readAsDataURL(file);
          return resolve();
        });
      },
      removeImage: function (e) {
        this.image = '';
      },
      postImage: function (e) {
        let vm = this;
        console.log(this.images);
        console.log(backendURL);
        axios.post(backendURL, {
          contentType: vm.selected,
          images: vm.images
        });
      },
      onFileFormatChange(e) {
        console.log(e)
      }
    }
  }
</script>

<style scoped>
  #app {
    text-align: center;
  }

  img {
    width: 30%;
    margin: auto;
    display: block;
    margin-bottom: 10px;
  }

  button {

  }
</style>
