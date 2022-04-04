<script setup>
import DocumentationIcon from "./icons/IconDocumentation.vue";
import ToolingIcon from "./icons/IconTooling.vue";
import EcosystemIcon from "./icons/IconEcosystem.vue";
import CommunityIcon from "./icons/IconCommunity.vue";
import SupportIcon from "./icons/IconSupport.vue";
import axios from "axios";
</script>

<template>
  <span>{{ $route.params.coub_id }}</span>
  {{ currentRouteName }}

  <p>url:{{url}}</p>
    <form
        id="app"
        @submit.prevent="sumbitForm"
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
            <input type="submit" value="Отправить">
        </p>

        </form>


</template>
<script>
export default {
  beforeMount() {
    this.$router.isReady().then(() => {
      if (this.$route.name === 'Coub') {
        this.url = 'https://coub.com/view/' + this.$route.params.coub_id
        this.search()
      }
    });
  },
  data() {
    return {
      coub_data: {},
      shazam_data: {},
      errors: [],
      url: "",
      searchLoaing: "",
    };
  },
  methods: {
    // mounted(){
      // if (this.currentRouteName === 'Coub') {
      //   this.data = 'test'
      // }
    //   console.log('created()');
    // },
    async search() {
      if (!this.url || !this.valiUrl(this.url)) {
        this.$toast.error('Wrong url / Непраивльная ссылка');
        return;
      }

      this.searchLoaing = true;

        const resp = await axios.post('https://mcoub.com/api/search', { url: this.url })
          .then((response) => {
            console.log(response)
          }).catch((error) => {
              if( error.response ) {
                  console.log(error.response.data); // => the response payload 
                  this.$toast.error('');

              }
              });

      this.searchLoaing = false;

      // this.$router.push({name: 'Coub', params: this.$data})
    },
    sumbitForm () {
      this.search()
    },
    valiUrl: function (url) {
      var re = /^https:\/\/coub\.com\/view\/\w+$/;
      return re.test(url);
    },
  },
  computed: {
    currentRouteName() {
      return this.$route.name;
    },
  },
};
</script>