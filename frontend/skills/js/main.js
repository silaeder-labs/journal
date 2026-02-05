const { createApp } = Vue

createApp({
  data() {
    return {
      columns: [],
      skills: [],
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
        const [skillsRes, columnsRes] = await Promise.all([
            this.fetchData('/api/user-skills-by-user-id', {
                method: 'GET',
                headers: { 'Content-Type': 'application/json' }
            }),
            this.fetchData('/api/table-columns-by-table-name', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: "skills" })
            })
        ]);

        let skills = skillsRes.skills;
        let columns = columnsRes.columns;

        columns.shift();
        skills.shift();
        
        this.columns = columns;
        this.skills = skills;

        this.isVisible = true;
      } catch (e) {
        alert("Произошла ошибка при загрузке данных");
        console.error(e);
      } finally {
        this.loading = false;
      }
    }
  }
}).mount('#app')