import easyocr
import cv2
import time

# 耗时测试
def calculate_execution_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"\n方法 {func.__name__} 执行时间: {end_time - start_time} 秒\n")
        return result
    return wrapper

# 通过image获取图片上面的文字 
# image: 图片路径 or numpy-array or 字节流；
# gpu: 是否使用gpu，默认True
#
# 参数说明
# 图片路径："test.jpg"
# numpy-array：cv2.imread("test.jpg")
# 字节流: 
# with open("test.jpg", "rb") as f: 
# img = f.read()
@calculate_execution_time
def readTextFromImage(image, gpu=True):
    reader = easyocr.Reader(['ch_sim','en'], gpu=gpu)
    result = reader.readtext(image, batch_size=5, paragraph=True, detail=0, text_threshold=0.8)
    return result

if __name__ == "__main__":
    # 使用示例
    res = readTextFromImage("images/BossHi-2158de32-d7fa-4aab-8ee3-5726dcde145a.png")
    print(res)


# 返回结果示例 res
# ['BOSS 直聘', '15:318', '56 64', '三 +', 'i0S 移动开发工程。', '推荐 精逸15最新', '筛选', '北京', '一键发布校招职位 检测当前职位接受应届生, 可使用一键同步再发 一个校招职位; 吸引更多应届牛人', '去发布', '成杰 刚刚活跃 4年 |硕士 2.5-2.6万元', '联想集团 Android', '内存管理 点击后 应用列表 Ui开发', 'Retroft', '主要负责联想平板的核心工具应用研发工作: 1.负责维 护日历 天气。计算器应用。独立完成U1开发实现。', '张释方 刚刚活跃 4年 本科 面议', '小米通讯技术: Java 明策智数科技: Android 最近关注: iOS', '50库 功能开发 Android开发', 'RXJava 业务', '小米软件开发工程师, 多次参加公司内部比赛频频获 奖; 工作能力强。主从 Android及 AR 方向;综合能. 义', '在线', 'SnOWer', '牛人', '搜索', '我的', '消息']