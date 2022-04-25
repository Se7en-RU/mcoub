<script setup>
import IconApple from "./icons/IconApple.vue";
import IconSpotify from "./icons/IconSpotify.vue";
import IconDeezer from "./icons/IconDeezer.vue";
import IconYoutube from "./icons/IconYoutube.vue";
import IconSad from "./icons/IconSad.vue";
import IconGithub from "./icons/IconGithub.vue";
import axios from "axios";
import NProgress from "nprogress";
</script>

<template>
  <main>
    <div class="welcome-block">
      <Transition name="fade">
        <div
          class="bg-img"
          v-bind:style="coubImageBackground"
          v-if="data.coub"
        ></div>
      </Transition>
      <div class="bg-fade"></div>
      <div class="container">
        <router-link to="/">
          <img
            alt="mCoub logo"
            class="logo"
            src="../assets/logo.svg"
            width="125"
            height="125"
          />
        </router-link>
        <div class="welcome-text">
          <h1>Музыка из COUB</h1>
          <h5>Распознать музыку с помощью Shazam</h5>
          <div class="welcome-search">
            <form
              id="app"
              @submit.prevent="sumbitForm"
              novalidate="true"
              class="form-inline"
            >
              <label for="url">Ссылка на Coub</label>
              <input
                id="url"
                v-model="form.url"
                type="text"
                name="url"
                autocomplete="off"
                autofocus
                placeholder="https://coub.com/view/1g2y7v"
                required
              />
              <button type="submit">Найти</button>
            </form>
          </div>
        </div>
      </div>
    </div>
    <Transition name="fade">
      <div class="result-block" v-if="data.shazam">
        <div class="container">
          <div class="music-container">
            <div class="album" v-if="shazamTrackImage">
              <img :alt="shazamTrackName" :src="shazamTrackImage" />
            </div>
            <div class="content">
              <div class="meta">
                <span>{{ shazamMetaData }}</span>
              </div>
              <h2>{{ shazamTrackTitle }}</h2>
              <p>{{ shazamTrackSubtitle }}</p>

              <div class="links">
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
        </div>
      </div>
    </Transition>
    <Transition name="fade">
      <div class="no-result-block" v-if="data.coub && !data.shazam">
        <div class="container">
          <i><IconSad /></i>
          Мы не смогли найти музыку из этого Coub, но вы можете
          <a
            :href="coubTrackUrl"
            title="cкачать оригинал"
            download
            target="_blank"
            >скачать оригинал ({{ coubTrackSize }})</a
          >
        </div>
      </div>
    </Transition>
    <div class="github-link">
      <a href="https://github.com/Se7en-RU/coub_music_searcher" target="_blank">
        <i><IconGithub /></i> 
      </a>
    </div>
  </main>
</template>
<script>
export default {
  watch: {
    "$route.params.coub_id"(value) {
      this.loadPage();
    },
  },
  beforeMount() {
    this.$router.isReady().then(() => {
      this.loadPage();
    });
  },
  data() {
    return {
      data: {},
      form: {
        url: "",
      },
    };
  },
  methods: {
    async search() {
      if (
        this.data.coub &&
        this.form.url === "https://coub.com/view/" + this.data.coub.permalink
      ) {
        return;
      }

      if (!this.valiUrl(this.form.url)) {
        this.$toast.error("Неправильная ссылка");
        return;
      }

      const newRoute = {
        name: "Coub",
        params: {
          coub_id: this.form.url.replace("https://coub.com/view/", ""),
        },
      };

      this.$router.push(newRoute);
      if (!this.$route.params.coub_id) {
        return;
      }

      NProgress.start();
      this.resetData();

      const resp = await axios
        .post("https://mcoub.com/api/search", { url: this.form.url })
        .then((response) => {
          this.data = response.data.data;
        })
        .catch((error) => {
          // if (error.response && error.response.data.error) {
          //   this.$toast.error(error.response.data.error);
          // }

          this.$toast.error("Coub не найден");
          this.$router.push({ name: "Home" });
        })
        .finally(() => {
          NProgress.done();
        });
    },
    resetData() {
      this.data = {};
    },
    sumbitForm() {
      this.search();
    },
    valiUrl: function (url) {
      var re = /^https:\/\/coub\.com\/view\/\w+$/;
      return re.test(url);
    },
    loadPage() {
      if (this.$route.name === "Coub") {
        let url = "https://coub.com/view/" + this.$route.params.coub_id;
        if (this.form.url !== url) {
          this.form.url = url;
          this.search();
        }
      }
    },
    copyClipboadName() {
      if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(this.shazamTrackName);
      } else {
        let textArea = document.createElement("textarea");
        textArea.value = this.shazamTrackName;
        textArea.style.position = "fixed";
        textArea.style.left = "-999999px";
        textArea.style.top = "-999999px";
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();

        try {
          document.execCommand("copy");
        } catch (err) {
          this.$toast.error("Не удалось скопировать название");
          return;
        }
      }

      this.$toast.success("Название скопировано");
    },
  },
  computed: {
    coubImageBackground() {
      let style = { "background-image": "none" };
      if (this.data.coub && this.data.coub.image_versions.template) {
        let image = this.data.coub.image_versions.template;
        image = image.replace("%{version}", "big");

        style = { "background-image": "url(" + image + ")" };
      }

      return style;
    },

    coubTrackUrl() {
      let url;
      if (this.data.coub) {
        url = this.data.coub.file_versions.html5.audio.high.url;
      }

      return url;
    },
    coubTrackSize() {
      let bytes;
      if (this.data.coub) {
        bytes = this.data.coub.file_versions.html5.audio.high.size;
      } else {
        return bytes;
      }

      const sizes = ["Bytes", "KB", "MB", "GB", "TB"];
      if (bytes == 0) return "0 Byte";
      const i = parseInt(Math.floor(Math.log(bytes) / Math.log(1024)));
      return Math.round(bytes / Math.pow(1024, i), 2) + " " + sizes[i];
    },
    shazamTrackName() {
      let name;
      if (this.data.shazam) {
        name = `${this.data.shazam.subtitle} - ${this.data.shazam.title}`;
      }

      return name;
    },
    shazamTrackTitle() {
      let name;
      if (this.data.shazam) {
        name = this.data.shazam.title;
      }

      return name;
    },
    shazamTrackSubtitle() {
      let name;
      if (this.data.shazam) {
        name = this.data.shazam.subtitle;
      }

      return name;
    },
    shazamTrackImage() {
      let url;
      if (this.data.shazam) {
        url = this.data.shazam.share.image;
      }

      return url;
    },
    shazamMetaData() {
      let meta;

      const a = Array.from(this.data.shazam.sections[0].metadata);

      a.forEach(function (item, index, array) {
        if (meta) {
          meta = meta + " • " + item.text;
        } else {
          meta = item.text;
        }
      });

      return meta;
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
.no-result-block {
  margin-top: 5vh;
  font-size: 30px;
  text-align: center;
}

.no-result-block i {
  display: flex;
  margin: 0 auto;
  padding-bottom: 2vh;
  fill: var(--color-text);
  width: 20vh;
  height: 20vh;
}

.no-result-block a {
  color: var(--color-pink);
}

.music-container {
  display: flex;
  align-items: center;
  flex-direction: row;
  background: var(--color-background-inverse);
}

.music-container .album img {
  display: flex;
  width: 100%;
  max-width: 285px;
  max-height: 285px;
}

.music-container .content {
  padding: 20px;
  flex-grow: 1;
}

.music-container .content .meta {
  justify-content: space-between;
  display: flex;
  text-transform: uppercase;
  letter-spacing: 1px;
  font-weight: 600;
}

.music-container .content .meta span {
  color: var(--color-pink);
}

.music-container .content .meta a {
  color: #666;
}

.music-container .content p {
  color: #666;
  font-size: 18px;
}

.music-container .content h2 {
  font-size: 36px;
  color: var(--color-text-inverse);
  line-height: 1.4;
  font-weight: 400;
  margin-top: 10px;
}

.music-container .content .links {
  margin-top: 20px;
  flex-wrap: wrap;
  display: flex;
}

.music-container .content .links a {
  color: var(--color-text-inverse);
  flex: 50%;
  margin-top: 10px;
}

.music-container .content .links a:hover {
  opacity: 0.8;
}

.music-container .content .links i {
  display: flex;
  place-items: center;
  place-content: center;
  width: 45px;
  height: 45px;
}

.welcome-block {
  background: var(--color-background);
  overflow: hidden;
  margin: 0 auto;
}

.welcome-text {
  text-align: center;
  position: relative;
}

.welcome-text h1 {
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
  align-items: stretch;
}

.form-inline label {
  margin: 5px 10px 5px 0;
}

.form-inline input {
  min-width: 30vh;
  vertical-align: middle;
  padding: 10px 20px;
  background-color: #fff;
  border: 1px solid #ddd;
  border-top-left-radius: 30px;
  border-bottom-left-radius: 30px;
  font-size: 20px;
  text-align: center;
}

.form-inline input:focus {
  outline: none;
  border-color: #ddd;
}

.form-inline button {
  min-width: 110px;
  font-size: 14px;
  font-weight: 600;
  display: inline-block;
  text-align: center;
  text-transform: uppercase;
  letter-spacing: 1px;
  padding: 9px 15px;
  background-color: var(--color-pink);
  color: white;
  border: 0;
  border-top-right-radius: 30px;
  border-bottom-right-radius: 30px;
}

.form-inline button:hover {
  opacity: 0.8;
  cursor: pointer;
}

.bg-img {
  display: block;
  background-position: center center;
  background-size: cover;
  background-repeat: no-repeat;
  -webkit-background-size: cover;
  background-size: cover;
}

.bg-img::before {
  content: "";
  position: absolute;
  width: 100%;
  height: 100%;
  backdrop-filter: blur(8px);
}

.bg-fade {
  display: block;
  opacity: 0.5;
  background: var(--color-background);
}

.bg-img,
.bg-fade {
  height: 100%;
  width: 100%;
  position: absolute;
}

.github-link {
  display: flex;
  align-items: center;
  justify-content: center;
}

.github-link i {
  position: fixed;
  bottom: 0;
  width: 45px;
  height: 45px;
  margin: 2vh 0;
  fill: var(--color-text);
}

@media only screen and (max-width: 400px) {
  .music-container .content .links a {
    flex: 100%;
  }
}

@media only screen and (max-width: 767px) {
  /* .bg-img, .bg-fade {
    display: none;
  } */

  .welcome-search {
    width: 80%;
    margin: 0 auto;
  }

  .form-inline input {
    width: 100%;
    margin-top: 5vh;
    border-top-right-radius: 30px;
    border-bottom-right-radius: 30px;
  }

  .form-inline button {
    width: 100%;
    margin-top: 3vh;
    padding: 14px 15px;
    border-top-left-radius: 30px;
    border-bottom-left-radius: 30px;
  }
  .music-container {
    flex-direction: column;
    align-items: stretch;
  }

  .music-container .album img {
    max-width: 100%;
    max-height: 100%;
  }
}

@media (min-width: 1024px) {
}
</style>