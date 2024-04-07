from . import _STATIC_URL
# SIMPLE UI config.
SIMPLEUI_DEFAULT_THEME = 'x-green.css'

SIMPLEUI_ICON = {
    '所有手机号': 'fas fa-phone-square',
    '房屋交易系统': 'fas fa-warehouse',
    'Web3Da': 'fas fa-cubes',
    '债务管理及分析系统': 'fas fa-wallet',
    '影院': 'fas fa-film',
    '账号管理系统': 'fas fa-tasks',
    '所有密码': 'fas fa-key',
    'Maps': 'fas fa-map',
    '所有图片': 'fas fa-images',
    '所有电子邮箱': 'fas fa-at',
    '所有语言': 'fas fa-language',
    '用户': 'fas fa-user-shield',
    '所有Film': 'fas fa-film',
    '所有视频': 'fab fa-youtube',
    'Static filess': 'fas fa-folder-open',
    'Settingss': 'fas fa-cogs',
    '所有国家': 'fas fa-globe-asia',
    '所有债务': 'fas fa-money-bill-wave',
    '所有账号类型': 'fab fa-accusoft',
    '所有账号': 'fas fa-address-book',
    '所有宝塔': 'fab fa-fort-awesome',
    '所有服务器': 'fas fa-server',
    '所有服务器用户': 'fas fa-user-astronaut',
    'Elastic searchs': 'el-icon-s-data',
    'House price types': 'fas fa-file-invoice-dollar',
    'Phone numbers': 'fas fa-phone-square',
    '万能堡垒': 'fab fa-fort-awesome',
    'SSH服务': 'fas fa-terminal',
    'SSH账号': 'fas fa-users'
}
SIMPLEUI_CONFIG = {
    # 在自定义菜单的基础上保留系统模块
    'system_keep': True,
    'dynamic': False,
    'menus': [
        {
            'name': '万能堡垒',
            'icon': 'fab fa-fort-awesome',
            'codename': 'jump-server',
            'models': [
                {
                    'name': '设备管理',
                    'codename': 'devices-management',
                    'icon': 'fas fa-server',
                    'models': [
                        {
                            'name': '服务管理',
                            'icon': 'fas fa-server',
                            'url': 'https://haoke98.github.io/DjangoAsyncAdmin/'
                        },
                        {
                            'name': '路由器管理',
                            'icon': 'fas fa-wifi',
                            'url': 'https://github.com/Haoke98/DjangoAsyncAdmin'
                        },
                        {
                            'name': '交换机管理',
                            'icon': 'fas fa-random',
                            'url': 'https://github.com/Haoke98/DjangoAsyncAdmin'
                        }

                    ]
                }, {
                    'name': '服务管理',
                    'url': 'https://github.com/newpanjing/simpleui',
                    'icon': 'fas fa-poll-h',
                    'codename': 'service-management',
                    'models': [
                        {
                            'name': 'SSH服务',
                            'icon': "fas fa-terminal",
                            'url': 'https://haoke98.github.io/DjangoAsyncAdmin/'
                        }, {
                            'name': '数据服务',
                            'url': 'https://github.com/Haoke98/DjangoAsyncAdmin'
                        }
                    ]
                }, {
                    'name': '网段管理',
                    'url': 'https://convert.72wo.com',
                    'icon': 'fas fa-network-wired',
                    'codename': 'convert'
                }, {
                    'name': '穿透管理',
                    'url': 'https://github.com/sea-team/gofound',
                    'icon': 'fab fa-hive',
                    'codename': 'gofound'
                }
            ]
        },
        {
            'name': 'GitHub',
            'icon': 'fas fa-code',
            'url': 'https://haoke98.github.io/AllKeeper/',
            'codename': 'community'
        },
        {
            'name': 'Bug反馈',
            'icon': 'fas fa-bug',
            'url': 'https://github.com/Haoke98/AllKeeper/issues',
            'codename': 'bug_trace',
            'newTab': True
        },
        {
            'name': '依赖',
            'icon': 'fas fa-project-diagram',
            'codename': 'product',
            'models': [
                {
                    'name': 'DjangoAsyncAdmin',
                    'codename': 'django_async_admin',
                    'icon': 'fas fa-bug',
                    'models': [
                        {
                            'name': '文档',
                            'url': 'https://haoke98.github.io/DjangoAsyncAdmin/'
                        }, {
                            'name': 'Github',
                            'url': 'https://github.com/Haoke98/DjangoAsyncAdmin'
                        }
                    ]
                }, {
                    'name': '图标',
                    'url': 'https://fontawesome.com/',  # TODO：后期把这个改成一个单独的页面，里面渲染出所有能够调用的图标，外加图标检索功能
                    'icon': 'fas fa-icons',
                    'codename': 'icon',
                    'newTab': True
                }, {
                    'name': '图片转换器',
                    'url': 'https://convert.72wo.com',
                    'icon': 'fab fa-github',
                    'codename': 'convert',
                    'newTab': True
                }, {
                    'name': '全文检索',
                    'url': 'https://github.com/sea-team/gofound',
                    'icon': 'fab fa-github',
                    'codename': 'gofound',
                    'newTab': True
                }
            ]
        }
    ]
}

SIMPLEUI_LOGO = _STATIC_URL + 'img/LOGO.png'
SIMPLEUI_HOME_INFO = False  # 首页上的simpleUI的版本信息板块。
SIMPLEUI_ANALYSIS = False  # 收集信息（TODO：不太好，等正式上线后建议关闭；否则出现信息泄露）
