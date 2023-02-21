var vm = new Vue({
el: '#app',
delimiters:['[[', ']]'],
  methods: {
      toggleSelection() {
          alert("hahaha")
      }
    },
    data: {
        name: '可爱的按钮'
    }
})