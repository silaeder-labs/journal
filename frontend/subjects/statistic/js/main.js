const { createApp } = Vue

createApp({
  data() {
    return {
      text: '',
      result: [],
      db_columns: [],
      isVisible: false,
      loading: false
    }
  },
  methods: {
    async fetchData(url, options = {}) {
        const res = await fetch(url, options);
        if (!res.ok) throw new Error(`Ошибка: ${res.status}`);
        return await res.json();
    },

    async send() {
      this.loading = true;
      try {
        // Выполняем запросы параллельно для скорости
        const [marksRes, columnsRes] = await Promise.all([
            this.fetchData('/api/user_marks', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: this.text })
            }),
            this.fetchData('/api/columns')
        ]);

        // Обработка оценок
        let marks = marksRes.result[0];
        marks.shift();
        this.result = marks;

        // Обработка колонок
        columnsRes.shift();
        this.db_columns = columnsRes;

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