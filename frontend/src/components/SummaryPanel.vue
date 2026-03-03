<template>
  <div class="card" v-if="summaryText">
    <div class="result-section">
      <h3>摘要结果</h3>
      <textarea :value="summaryText" rows="10" readonly></textarea>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SummaryPanel',
  props: {
    summaryText: {
      type: String,
      default: ''
    }
  }
}
</script>

<style scoped src="../assets/styles/common.css"></style>
<style scoped src="../assets/styles/parse-demo.css"></style>