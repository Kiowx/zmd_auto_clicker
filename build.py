import os
import shutil
import subprocess
import Cython
import paddleocr
import paddle  # 🟢 引入 paddle 库来定位 DLL 位置

# --- 配置区 ---
APP_NAME = "终末地抢单小助手"
SPEC_FILE = "auto_clicker.spec"
DIST_INTERNAL = os.path.join("dist", APP_NAME, "_internal")

def build():
    print("🚀 第一阶段：开始 PyInstaller 基础打包...")
    result = subprocess.run(["pyinstaller", "--noconfirm", "--clean", SPEC_FILE], shell=True)
    
    if result.returncode == 0:
        print("\n✅ 基础打包完成，准备执行 [物理补丁] 注入...")
        
        # 1. 注入 Cython 模板
        cython_src = os.path.join(os.path.dirname(Cython.__file__), "Utility")
        cython_dst = os.path.join(DIST_INTERNAL, "Cython", "Utility")
        try:
            shutil.copytree(cython_src, cython_dst, dirs_exist_ok=True)
            print(f"✨ Cython 补丁注入成功！")
        except Exception as e:
            print(f"⚠️ Cython 补丁注入失败: {e}")

        # 2. 注入 PaddleOCR 核心工具包
        paddleocr_src = os.path.dirname(paddleocr.__file__)
        paddleocr_dst = os.path.join(DIST_INTERNAL, "paddleocr")
        try:
            shutil.copytree(paddleocr_src, paddleocr_dst, dirs_exist_ok=True)
            print(f"✨ PaddleOCR 核心工具包注入成功！")
        except Exception as e:
            print(f"⚠️ PaddleOCR 补丁注入失败: {e}")

        # 3. 🟢 新增：注入 Paddle 底层 DLL 库 (解决 mklml.dll 报错)
        paddle_src = os.path.dirname(paddle.__file__)
        paddle_libs_src = os.path.join(paddle_src, "libs")
        paddle_libs_dst = os.path.join(DIST_INTERNAL, "paddle", "libs")
        try:
            if os.path.exists(paddle_libs_src):
                shutil.copytree(paddle_libs_src, paddle_libs_dst, dirs_exist_ok=True)
                print(f"✨ Paddle 底层 DLL 库 (mklml.dll等) 注入成功！")
            else:
                # 针对某些不同版本的 paddle 结构
                print(f"⚠️ 未找到 paddle/libs 文件夹，请确认 paddle 安装状态。")
        except Exception as e:
            print(f"⚠️ Paddle DLL 注入失败: {e}")

        print(f"\n🎉 终极打包完成！请去 dist/{APP_NAME} 目录下双击 {APP_NAME}.exe 运行吧！")
    else:
        print("❌ 打包过程出错，请检查上方日志。")

if __name__ == "__main__":
    build()