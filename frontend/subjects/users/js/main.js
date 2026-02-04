const { createApp } = Vue

createApp({
  data() {
    return {
      result: [],
      users: [],
      ids: [],
      classes: [],
      sortedUniqueClasses: [],
      isVisible: false,
      loading: false
    }
  },
  mounted() {
    this.send();
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
      this.loading = true;
      try {
        // Выполняем запросы параллельно для скорости
        const result = await Promise.all([
            this.fetchData('/api/get-users', {
                method: 'GET',
                headers: { 'Content-Type': 'application/json' }
            })
        ]);

        users = result[0][0];
        ids = result[0][1];
        classes = result[0][2];
        sortedUniqueClasses = [...new Set(classes)].sort((a, b) => a - b);
        
        this.users = users;
        this.ids = ids;
        this.classes = classes;
        this.sortedUniqueClasses = sortedUniqueClasses;

        this.isVisible = true;
      } catch (e) {
        alert("Произошла ошибка при загрузке данных");
        console.error(e);this.send
      } finally {
        this.loading = false;
      }
    }
  }
}).mount('#app')