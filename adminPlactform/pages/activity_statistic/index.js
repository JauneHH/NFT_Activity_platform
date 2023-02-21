var app = new Vue({
  el: '#app',
  data: {
    show: true,
    showUser: false,
    cardShow: false,
    search: '',
    tableActivity: '[]',
    tableUser: '[]',
    static_url: 'http://localhost:63343/mq-admin-master(h5)/pages/demo/index.html?activity_id=',
    statistics_url: '',
  },

  methods: {
    cellStyle({ row, column, rowIndex, columnIndex }) {
      if (row.activity_status == '进行中') {
        if (columnIndex == 5) {
          return 'font-weight:bold;color:#E6A23C';
        }
      } else {
        if (columnIndex == 5) {
          return 'font-weight:bold;color:#67C23A';
        }
      }
    },
    tableRowClassName({ row, rowIndex }) {
      if (row.activity_status == '进行中') {
        return 'warning-row';
      } else if (row.status == '已结束') {
        return 'success-row';
      }
      return '';
    },
    handleEdit(index, row) {
      console.log(row['id']);
      console.log(index, row);
      this.cardShow = !this.cardShow;
      this.statistics_url = this.static_url + row['activity_id'];
      console.log(this.statistics_url);
    },
    handleDelete(index, row) {
      console.log(row['id']);
      console.log(index, row);
      this.cardShow = !this.cardShow;
      this.statistics_url = this.static_url + row['activity_id'];
      console.log(this.statistics_url);
    },
    handleSizeChange(val) {
      console.log(`每页 ${val} 条`);
    },
    handleCurrentChange(val) {
      console.log(`当前页: ${val}`);
    },
    hidden() {
      this.cardShow = !this.cardShow;
    },
    getActivityList() {
      let that = this;
      axios({
        method: 'post',
        url: 'http://127.0.0.1:5000/api/manager/activity_list',
        headers: { 'Content-Type': 'multipart/form-data' },
        onUploadProgress: function (progressEvent) {
          console.log(progressEvent);
        },
      })
        .then(function (ret) {
          console.log(ret.data['msg']);
          that.tableActivity = ret.data['msg'];
          console.log(that.tableActivity);
          for (let item in that.tableActivity) {
            if (that.tableActivity[item]['activity_status'] == false) {
              that.tableActivity[item]['activity_status'] = '进行中';
            } else {
              that.tableActivity[item]['activity_status'] = '已结束';
            }
          }
        })
        .catch(function (err) {
          console.log(err);
        });
    },
    get_activity_user(index, row) {
      this.user_activity_url = this.static_url + row['activity_id'];
      this.cardShow = !this.cardShow;
      let that = this;
      axios({
        method: 'post',
        url: 'http://127.0.0.1:5000/api/manager/activity_user_list',
        data: row['activity_id'],
        headers: { 'Content-Type': 'multipart/form-data' },
        onUploadProgress: function (progressEvent) {
          console.log(progressEvent);
        },
      })
        .then(function (ret) {
          console.log(ret);
        })
        .catch(function (err) {
          console.log(err);
        });
    },
  },
  mounted() {
    this.getActivityList();
  },
});
