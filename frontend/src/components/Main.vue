<script setup>
import IconApple from "./icons/IconApple.vue";
import axios from "axios";
</script>

<template>
  <header>Header</header>
  <div class="bg-image"></div>
  <main>
    <div class="block">
      search form
    </div>
    <i>
      <IconApple />
    </i>
  <form
      id="app"
      @submit.prevent="sumbitForm"
      novalidate="true"
    >
      <p>
          <label for="url">Имя</label>
          <input
              id="url"
              v-model="url"
              type="text"
              name="url"
              autocomplete="off"
              autofocus
              placeholder="https://coub.com/view/1g2y7v"
              required
          >
      </p>

      <p>
          <input type="submit" value="Отправить">
      </p>

      </form>

      <div v-if=loading>
        Loading...
      </div>
      {{ data }}
      <div v-if=data.coub>
        <iframe :src="coubEmbedLink" allowfullscreen frameborder="0" width="640" height="360" allow="autoplay"></iframe>
      </div>
  </main>

<footer>Github 2022 (c)</footer>
</template>
<script>
export default {
  beforeMount() {
    this.$router.isReady().then(() => {
      if (this.$route.name === "Coub") {
        this.url = "https://coub.com/view/" + this.$route.params.coub_id;
        this.search();
      }
    });
  },
  data() {
    return {
      data: {},
      url: "",
      loading: false,
    };
  },
  methods: {
    async search() {
      if (!this.url || !this.valiUrl(this.url)) {
        this.$toast.error("Wrong url / Непраивльная ссылка");
        return;
      }

      if (this.url === 'https:://coub.com' + this.data.coub.permalink) {
        return;
      }

      this.resetData();

      const resp = await axios
        .post("https://mcoub.com/api/search", { url: this.url })
        .then((response) => {
          console.log(response)
          this.data = response.data.data;
          if (this.data) {
            this.$router.push({name: 'Coub', params: {'coub_id': this.data.coub.permalink}})
          }

        })
        .catch((error) => {
          if (error.response && error.response.data.error) {
            this.$toast.error(error.response.data.error);
          }

          this.$toast.error("Coub not found / Coub не найден");
          this.$router.push({name: 'Home'});
        });

      this.loading = false;
    },
    resetData() {
      this.data = {};
      this.loading = true;
    },
    sumbitForm() {
      this.search();
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
    coubEmbedLink() {
      return '//coub.com/embed/' + this.data.coub.permalink + '?muted=false&autostart=false&originalSize=false&startWithHD=false'
    }
  },
};
</script>

<style scoped>

i {
  display: flex;
  place-items: center;
  place-content: center;
  width: 32px;
  height: 32px;
}

@media (min-width: 1024px) {
  i {
    top: calc(50% - 25px);
    border-radius: 8px;
    width: 50px;
    height: 50px;
  }
}
</style>