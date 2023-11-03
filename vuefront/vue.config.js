const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  outputDir: '../server/static',
  publicPath: process.env.NODE_ENV === 'production' ? '/static/' : '/'
})
