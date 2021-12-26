# SIMPLE UI config.
SIMPLEUI_DEFAULT_THEME = 'orange.css'

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
    '所有账号': 'fas fa-address-book'
}
from . import _STATIC_URL

SIMPLEUI_LOGO = _STATIC_URL + 'img/logo-sdm.png'
SIMPLEUI_HOME_INFO = False  # 首页上的simpleUI的版本信息板块。
SIMPLEUI_ANALYSIS = False  # 收集信息（TODO：不太好，等正式上线后建议关闭；否则出现信息泄露）
