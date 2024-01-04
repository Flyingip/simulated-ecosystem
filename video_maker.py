import os
from moviepy.editor import ImageSequenceClip
from datetime import datetime

current_file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file_path)
os.chdir(current_dir)

# 图像帧的路径
folder_path = "snapshots"  # 替换为帧所在的文件夹路径
frame_files = []
number_of_frames = 0
for filename in os.listdir(folder_path):
    if filename.endswith(".jpg"):  # 根据文件扩展名过滤
        number_of_frames += 1

frame_files = [f"{folder_path}/frame_{i}.jpg" for i in range(number_of_frames)]
# 创建视频剪辑
clip = ImageSequenceClip(frame_files, fps=10)  # fps 设置为期望的帧率

# 写入视频文件
clip.write_videofile(
    f"videos/output {datetime.now().strftime('%H-%M-%S')}.mp4", codec="libx264"
)

# 删除原有图像
for filename in os.listdir(folder_path):
    try:
        if filename.endswith(".jpg"):  # 根据文件扩展名过滤
            file_path = os.path.join(folder_path, filename)
            os.remove(file_path)
    except Exception as e:
        print("Failed to delete %s. Reason: %s" % (file_path, e))
