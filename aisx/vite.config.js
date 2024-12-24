import { defineConfig,loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import { AntDesignVueResolver,ElementPlusResolver  } from 'unplugin-vue-components/resolvers'
import viteCompression from 'vite-plugin-compression'
import ElementPlus from 'unplugin-element-plus/vite'
import {resolve} from 'path'
import VueSetupExtend from 'vite-plugin-vue-setup-extend'
export default defineConfig(({ command, mode }) => {
  // 环境变量
  const env = loadEnv(mode, process.cwd())
    // 生产环境判断
  const isEnvProduction = mode === 'production'
  return {
    plugins: [vue(),VueSetupExtend(),ElementPlus({}),
    AutoImport({
      resolvers: [AntDesignVueResolver(),ElementPlusResolver()],
    }),
    Components({
      resolvers: [ElementPlusResolver({
        importStyle: 'sass',//添加
      }),AntDesignVueResolver({
        importStyle: false, // css in js
      })],
    }),
    viteCompression({
      //生成压缩包gz
      verbose: true,
      disable: false,
      threshold: 10240,
      algorithm: 'gzip',
      ext: '.gz',
    }),
     
    ],
    define: {
      'process.env': {}
    },
    base: "/",
    publicDir: 'public',
    // 生产环境是否生成 sourceMap 文件
    // productionSourceMap: false,
    server: {
      host: '0.0.0.0',
      port: 19915,
      // 是否自动在浏览器打开
      open: true,
      // 是否开启 https
      https: false,
      //反向代理
      proxy: {
        '/api': {
          // target: 'http://192.168.101.150:8090/',
          target: 'http://127.0.0.1:5000/',
          changeOrigin: true,
          rewrite: (pathStr) => pathStr.replace(new RegExp('^/api'), '')
        },
      },
    },
    resolve: {
      alias: {
        //路径别名
        "@": resolve(__dirname, "./src"),
        "@assets": resolve(__dirname, "./src/assets"),
        "public": resolve(__dirname, "./public"),
      },
    },
    css: {
      preprocessorOptions: {
        scss: {
          api: 'modern-compiler',
          quietDeps:true,
          additionalData: `@use "@/assets/css/style.scss" as *;@use "@/assets/css/elementplus.scss" as *;`,

        }
      }
    }, build: {
      // 打包路径
      assetsDir: "./static",
      // 压缩
      // Terser 相对较慢，但大多数情况下构建后的文件体积更小。ESbuild 最小化混淆更快但构建后的文件相对更大。
      //启用/禁用 CSS 代码拆分
      cssCodeSplit: true,
      minify: !isEnvProduction ? 'esbuild' : 'terser',
      terserOptions: {
        compress: {
          // 生产环境去除console
          drop_console: isEnvProduction,
          drop_debugger: isEnvProduction
        },
        output: {
          // 去掉注释内容
          comments: true,
        },
      },
      // 取消计算文件大小，加快打包速度
      brotliSize: false,
      sourcemap: false,
      outDir: 'dist',
      rollupOptions: {
        input: {
          // 入口文件
          main: resolve(__dirname, "index.html"),
          // 其他入口
          // nested: resolve(__dirname, 'xxxx.html')
        },
        output: {
          // chunkFileNames: 'static/js/[name]-[hash].js',
          // entryFileNames: 'static/js/[name]-[hash].js',
          // assetFileNames: 'static/[ext]/[name]-[hash].[ext]',
          manualChunks(id) { //静态资源分拆打包
            if (id.includes('node_modules')) {
              return id.toString().split('node_modules/')[1].split('/')[0].toString();
            }
          }
        },
      },
    },
  }
})
