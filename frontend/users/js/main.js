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
        const [result] = await Promise.all([
            this.fetchData('/api/all-users-info', {
                method: 'GET',
                headers: { 'Content-Type': 'application/json' }
            })
        ]);
        
        let users_info = (result.users_info);

        let classes = [];
        let ids = [];
        let users = [];

        for(let i = 0; i < users_info.length; i++) {
          classes.push(users_info[i][0]);
          ids.push(users_info[i][1]);
          users.push(`${users_info[i][2]} ${users_info[i][3]} ${users_info[i][4]}`);
        }
        
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