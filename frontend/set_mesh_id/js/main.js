const { createApp } = Vue

createApp({
  data() {
    return {
      text: '',
      loading: false,
      result: ''
    }
  },
  methods: {
    async fetchData(url, options = {}) {
        const token = localStorage.getItem('token');
        if (!options.headers) options.headers = {};
        if (token) options.headers['Authorization'] = `Bearer ${token}`;
        const res = await fetch(url, options);
        if (!res.ok) throw new Error(`Ошибка: ${res.status}`);
        return await res.json();
    },

    async send() {
        try {
            this.loading = true;
            this.fetchData('/api/set-mesh-id', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: this.text })
            })
            this.result = "Ваш МЭШ id успешно обновлен!";
            this.loading = false;
        } catch (e) {
            this.result = "Произошла ошибка!";
            console.error(e);
        }
    }
  }
}).mount('#app')