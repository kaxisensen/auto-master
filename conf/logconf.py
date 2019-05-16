LOGGING_CONFIG = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'simpleFormatter'
        },
        'fileinfo': {
            'class': "logging.handlers.RotatingFileHandler",
            'level': 'INFO',
            'formatter': 'simpleFormatter',
            "filename": '../logs/leboauto.log',
            'mode': 'w+',
            "maxBytes": 1024 * 1024 * 5,
            "backupCount": 20,
            "encoding": "utf8"
        }
    },
    'formatters': {
        'simpleFormatter': {
            'format': '   %(asctime)s %(name)s %(levelname)s 文件名:%(filename)s 模块名:%(module)s 函数名:%(funcName)s 第%(lineno)d行 %(message)s'
        }
    },
    'loggers': {
        'terminal_record': {
            'level': 'INFO',
            'handlers': ['console']
        },
        'file_record': {
            'level': 'INFO',
            'handlers': ['fileinfo']
        }
    }
}

# 日志格式
#--------------------------------------------------
# %(asctime)s 年-月-日 时-分-秒,毫秒
# %(filename)s 文件名，不含目录
# %(pathname)s 目录名，完整路径
# %(funcName)s 函数名
# %(levelname)s 级别名
# %(lineno)d 行号
# %(module)s 模块名
# %(message)s 消息体
# %(name)s 日志模块名
# %(process)d 进程id
# %(processName)s 进程名
# %(thread)d 线程id
# %(threadName)s 线程名
