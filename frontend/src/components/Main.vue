<script setup>
import IconApple from "./icons/IconApple.vue";
import IconSpotify from "./icons/IconSpotify.vue";
import IconDeezer from "./icons/IconDeezer.vue";
import axios from "axios";
</script>

<template>
  <header>Header</header>
  <div class="bg-image"></div>
  <main>
    <div class="block">
      <form
        id="app"
        @submit.prevent="sumbitForm"
        novalidate="true"
        class="form-inline"
      >
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
        <button type="submit">🔍</button>
      </form>
    </div>
      <div v-if=loading>
        Loading...
      </div>
      <div v-if=data.coub>
        <iframe :src="coubEmbedLink" allowfullscreen frameborder="0" width="640" height="360"></iframe>
      </div>

      <div v-if=data.shazam>
      <a :href="data.shazam.myshazam.apple.actions[0].uri" class="icon-link" v-if="data.shazam.myshazam.apple.actions[0].uri" title="Open in Apple Music" target="_blank">
            <i><IconApple /></i>
            Apple Music
        </a>
        <template v-if="data.shazam.hub.providers">
        <a :href="provider.actions[0].uri" class="icon-link" v-for="provider in data.shazam.hub.providers" :key=provider.type :title="provider.caption" target="_blank">
           <template v-if="provider.type === 'SPOTIFY'">
            <i><IconSpotify /></i>
            Spotify
           </template>
           <template v-if="provider.type === 'DEEZER'">
            <i><IconDeezer /></i>
            Deezer
           </template>

        </a>
        </template>
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
      if (!this.url || this.data.coub && this.url === 'https://coub.com/view/' + this.data.coub.permalink) {
        return;
      }

      if (!this.valiUrl(this.url)) {
        this.$toast.error("Wrong url / Непраивльная ссылка");
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

            if(this.data.shazam)  {
              this.data.shazam = this.data.shazam[0]
            }
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

.icon-link {
  display: flex;
  align-items: center;
}

.icon-link i {
  padding-right: 10px;
}

.form-inline {
  display: flex;
  flex-flow: row wrap;
  align-items: center;
}

.form-inline label {
  margin: 5px 10px 5px 0;
}

.form-inline input {
  width: 40vh;
  vertical-align: middle;
  /* margin: 5px 10px 5px 0; */
  padding: 10px;
  background-color: #fff;
  border: 1px solid #ddd;
  border-top-left-radius: 10px;
  border-bottom-left-radius: 10px;
  font-size: 20px;
}

.form-inline input:focus {
  outline: none;
  border-color: #ddd;
}

.form-inline button {
  padding: 9px 15px;
  background-color: dodgerblue;
  border: 0;
  color: white;
  border: 0;
  border-top-right-radius: 10px;
  border-bottom-right-radius: 10px;
  font-size: 20px;

}

.form-inline button:hover {
  background-color: royalblue;
}

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