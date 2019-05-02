import Vue from 'vue'
import Router from 'vue-router'
import FileUpload from '@/components/FileUpload'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'FileUpload',
      component: FileUpload
    }
  ]
})
