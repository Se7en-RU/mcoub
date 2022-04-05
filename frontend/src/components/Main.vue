<script setup>
import IconApple from "./icons/IconApple.vue";
import IconSpotify from "./icons/IconSpotify.vue";
import IconDeezer from "./icons/IconDeezer.vue";
import IconYoutube from "./icons/IconYoutube.vue";
import axios from "axios";
</script>

<template>
  <header></header>
  <main>
    <div class="welcome-block">
      <div class="bg-img" v-bind:style="coubImageBackground"></div>
      <div class="container">
        <img
          alt="mCoub logo"
          class="logo"
          src="../assets/logo.svg"
          width="125"
          height="125"
        />
        <div class="welcome-text">
          <h2>Музыка из COUB</h2>
          <h5>Распознать музыку с помощью Shazam</h5>
          <div class="welcome-search">
            <form
              id="app"
              @submit.prevent="sumbitForm"
              novalidate="true"
              class="form-inline"
            >
              <label for="url">Ссылка на Cob</label>
              <input
                id="url"
                v-model="url"
                type="text"
                name="url"
                autocomplete="off"
                autofocus
                placeholder="https://coub.com/view/1g2y7v"
                required
              />
              <button type="submit" disabled>Найти</button>
            </form>
          </div>
        </div>
      </div>
    </div>

    <div class="result-block">
      <div class="container">
        <div v-if="loading">Loading...</div>
        <div v-if="data.coub">
          <iframe
            :src="coubEmbedLink"
            allowfullscreen
            frameborder="0"
            width="640"
            height="360"
          ></iframe>
        </div>

        <div v-if="data.shazam">
          <a
            :href="AppleMusicLink"
            class="icon-link"
            v-if="AppleMusicLink"
            title="Open in Apple Music"
            target="_blank"
          >
            <i><IconApple /></i>
            Apple Music
          </a>
          <a
            :href="YouTubeLink"
            class="icon-link"
            v-if="YouTubeLink"
            title="Open in YouTube"
            target="_blank"
          >
            <i><IconYoutube /></i>
            YouTube
          </a>
          <template v-if="data.shazam.hub.providers">
            <a
              :href="provider.actions[0].uri"
              class="icon-link"
              v-for="provider in data.shazam.hub.providers"
              :key="provider.type"
              :title="provider.caption"
            >
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
      </div>
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
      if (
        !this.url ||
        (this.data.coub &&
          this.url === "https://coub.com/view/" + this.data.coub.permalink)
      ) {
        return;
      }

      if (!this.valiUrl(this.url)) {
        this.$toast.error("Непраивльная ссылка");
        return;
      }

      this.resetData();

      const resp = await axios
        .post("https://mcoub.com/api/search", { url: this.url })
        .then((response) => {
          console.log(response);
          this.data = response.data.data;
          if (this.data) {
            this.$router.push({
              name: "Coub",
              params: { coub_id: this.data.coub.permalink },
            });

            if (this.data.shazam) {
              this.data.shazam = this.data.shazam[0];
            }
          }
        })
        .catch((error) => {
          if (error.response && error.response.data.error) {
            this.$toast.error(error.response.data.error);
          }

          this.$toast.error("Coub не найден");
          this.$router.push({ name: "Home" });
        })
        .finally(() => {
          setTimeout(
            function () {
              this.loading = false;
            }.bind(this),
            500
          );
        });
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
    coubImageBackground() {
      let style = {};
      if (this.data.coub && this.data.coub.image_versions.template) {
        let image = this.data.coub.image_versions.template;
        image = image.replace("%{version}", "big");

        style = { 'background-image': "url(" + image + ")" };
      }

      return style;
    },
    coubEmbedLink() {
      return (
        "//coub.com/embed/" +
        this.data.coub.permalink +
        "?muted=false&autostart=false&originalSize=false&startWithHD=false"
      );
    },
    YouTubeLink() {
      let link;
      if (this.data.shazam) {
        if (this.data.shazam.urlparams["{tracktitle}"]) {
          link = this.data.shazam.urlparams["{tracktitle}"];
        }

        if (this.data.shazam.urlparams["{trackartist}"]) {
          link = this.data.shazam.urlparams["{trackartist}"] + "+" + link;
        }

        if (link) {
          link = "https://www.youtube.com/results?search_query=" + link;
        }
      }

      return link;
    },
    AppleMusicLink() {
      let link;

      if (
        this.data.shazam.myshazam &&
        this.data.shazam.myshazam.apple.actions[0].uri
      ) {
        link = this.data.shazam.myshazam.apple.actions[0].uri;
      }

      return link;
    },
  },
};
</script>

<style scoped>
.welcome-block {
  background: var(--color-background);
}

.welcome-text {
  text-align: center;
  position: relative;
  overflow: hidden;
}

.welcome-text h2 {
  font-size: 72px;
  color: var(--color-heading);
  display: block;
  line-height: 1.2;
}

.welcome-text h5 {
  padding-top: 1vh;
  font-size: 24px;
  color: var(--color-text);
}

.welcome-search {
  margin-top: 5vh;
  display: flex;
  align-items: center;
  flex-direction: column;
}

label {
  display: none;
}

.bg-img {
  height: 102%;
  width: 102%;
  position: absolute;

  filter: blur(8px);
  -webkit-filter: blur(8px);

  background-position: center center;
  background-size: cover;
  background-repeat: no-repeat;
  -webkit-background-size: cover;
  -moz-background-size: cover;
  -o-background-size: cover;
  background-size: cover;

  -webkit-animation: fadein 3s;
  animation: fadein 3s;
}

@-webkit-keyframes fadein {
  from {
    opacity: 0.2;
  }
  to {
    opacity: 1;
  }
}

@keyframes fadein {
  from {
    opacity: 0.2;
  }
  to {
    opacity: 1;
  }
}

/* main {
  display: flex;
  min-height: 50vh;
  flex-direction: column;
}

main {
  flex: 1;
} */

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
  text-transform: uppercase;
}

.form-inline button:hover {
  background-color: royalblue;
  cursor: pointer;
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