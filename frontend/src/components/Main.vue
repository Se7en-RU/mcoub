<script setup>
import DocumentationIcon from './icons/IconDocumentation.vue'
import ToolingIcon from './icons/IconTooling.vue'
import EcosystemIcon from './icons/IconEcosystem.vue'
import CommunityIcon from './icons/IconCommunity.vue'
import SupportIcon from './icons/IconSupport.vue'
import axios from 'axios';
</script>

<template>
  <span>{{ $route.params.coub_id }}</span>
  {{ currentRouteName }}

    <form
        id="app"
        @submit="searchCoub"
        method="post"
        novalidate="true"
        >

        <p v-if="errors.length">
            <b>Пожалуйста исправьте указанные ошибки:</b>
            <ul>
            <li v-for="error in errors">{{ error }}</li>
            </ul>
        </p>

        <p>
            <label for="url">Имя</label>
            <input
                id="url"
                v-model="url"
                type="text"
                name="url"
                placeholder="https://coub.com/view/1g2y7v"
                required
            >
        </p>

        <p>
            <input
            type="submit"
            value="Отправить"
            >
        </p>

        </form>


</template>
<script>
export default {
  data() {
    return {
        coub_data: {},
        shazam_data: {},
        errors: [],
        url: '',
    }
  },
  methods: {
      // mounted(){
      //   if (this.currentRouteName === 'Coub') {
      //     this.data = 'test'
      //   }
      //   console.log('created()');
      // },
      async search() {
          try {
                // const api = '/api/search'
                const api = 'https://mcoub.com/api/search'
                const resp = await axios.post(api, {url: this.url});
                console.log(resp.data);
            } catch (err) {
                // Handle Error Here
                console.error(err);
            }

            // this.$router.push({name: 'Coub', params: this.$data})

        },
        searchCoub: function (e) {
            e.preventDefault()
            this.errors = [];

            if (!this.url || !this.valiUrl(this.url)) {
                this.errors.push('Wrong url');
            }

            if (!this.errors.length) {
                this.search()
            }
        },
        valiUrl: function (url) {
            var re = /^https:\/\/coub\.com\/view\/\w+$/;
            return re.test(url);
        }
  },
  computed: {
    // a computed getter
    publishedBooksMessage() {
      // `this` points to the component instance
      return 'Yes'
    },
    currentRouteName() {
        return this.$route.name;
    }
  }
}
</script>