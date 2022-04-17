const { description } = require('../../package')

module.exports = {
  /**
   * Ref：https://v1.vuepress.vuejs.org/config/#title
   */
  title: 'Python REST API Server 101',
  /**
   * Ref：https://v1.vuepress.vuejs.org/config/#description
   */
  description: description,

  /**
   * Extra tags to be injected to the page HTML `<head>`
   *
   * ref：https://v1.vuepress.vuejs.org/config/#head
   */
  head: [
    ['meta', { name: 'theme-color', content: '#009B8B' }],
    ['meta', { name: 'apple-mobile-web-app-capable', content: 'yes' }],
    ['meta', { name: 'apple-mobile-web-app-status-bar-style', content: 'black' }]
  ],

  /**
   * Theme configuration, here is the default theme configuration for VuePress.
   *
   * ref：https://v1.vuepress.vuejs.org/theme/default-theme-config.html
   */
  themeConfig: {
    repo: 'https://github.com/heumsi/python-rest-api-server-101',
    editLinks: false,
    docsDir: '',
    editLinkText: '',
    lastUpdated: true,
    sidebar: [
      {
        title: '시작하기',
        path: '/01-getting-started/',
        collapsable: true,
        children: [
          ['/01-getting-started/01-installation-python/', '파이썬 설치하기'],
          ['/01-getting-started/02-creating-project/', '프로젝트 생성하기'],
          ['/01-getting-started/03-implementation-db-models/', 'Database 모델 구현하기'],
          {
            title: 'REST API 구현하기',
            path: '/01-getting-started/04-implementation-rest-api/',
            collapsable: true,
            children: [
              ['/01-getting-started/04-implementation-rest-api/01-creating-fastapi-app/', 'FastAPI 인스턴스 만들기'],
              ['/01-getting-started/04-implementation-rest-api/02-implementation-healthcheck-endpoint/', '간단한 API 엔드포인트 만들고 확인하기'],
              {
                title: 'CRUD 엔드포인트 구현하기',
                path: '/01-getting-started/04-implementation-rest-api/03-implementation-crud-endpoint/',
                collapsable: false,
                children: [
                  ['/01-getting-started/04-implementation-rest-api/03-implementation-crud-endpoint/01-create-post/', '게시글 생성'],
                  ['/01-getting-started/04-implementation-rest-api/03-implementation-crud-endpoint/02-read-post/', '게시글 조회'],
                  ['/01-getting-started/04-implementation-rest-api/03-implementation-crud-endpoint/03-read-posts/', '게시글 목록 조회'],
                  ['/01-getting-started/04-implementation-rest-api/03-implementation-crud-endpoint/04-update-post/', '게시글 수정'],
                  ['/01-getting-started/04-implementation-rest-api/03-implementation-crud-endpoint/05-delete-post/', '게시글 삭제'],
                ]
              }
            ]
          },
          ['/01-getting-started/05-summary/', '정리하기'],
        ]
      },
    ]
  },
  markdown: {
    lineNumbers: true
  },
  /**
   * Apply plugins，ref：https://v1.vuepress.vuejs.org/zh/plugin/
   */
  plugins: [
    '@vuepress/plugin-back-to-top',
    '@vuepress/plugin-medium-zoom',
  ]
}
