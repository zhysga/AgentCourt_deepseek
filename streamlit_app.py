# c:\workdir\CascadeProjects\windsurf-project\paper\AgentCourt-main\AgentCourt-main\streamlit_app.py
from AgentCourt_main.main import CourtSimulation
import streamlit as st
from main import CourtSimulation
import json

def main():
    # 设置页面配置
    st.set_page_config(page_title="Agent Court 模拟器", layout="wide")
    
    # 在侧边栏设置模拟参数
    with st.sidebar:
        st.header("⚖️ 模拟参数")
        config_file = st.file_uploader("上传配置文件", type=["json"])
        case_path = st.text_input("案例路径", value="data/cases")
        log_level = st.selectbox("日志级别", ["DEBUG", "INFO", "WARNING", "ERROR"])
        dp_mode = st.radio("运行模式", ["API模式", "离线模式"], index=0)
    
    # 如果上传了配置文件
    if config_file:
        # 加载配置文件
        config = json.load(config_file)
        # 创建模拟对象
        sim = CourtSimulation(
            config_path=config,
            case_path=case_path,
            log_level=log_level,
            dp=1 if dp_mode == "API模式" else 0
        )
        
        # 如果点击了开始模拟按钮
        if st.button("开始模拟"):
            # 创建进度条和日志容器
            progress_bar = st.progress(0)
            log_container = st.container()
            
            # 重定向日志到Streamlit
            class StreamlitHandler(logging.Handler):
                def emit(self, record):
                    log_container.write(f"{record.levelname}: {record.msg}")
            
            sim.logger.addHandler(StreamlitHandler())
            
            # 运行模拟
            for i in trange(10):  # 示例进度
                progress_bar.progress((i+1)/10)
                # 调用原模拟逻辑
                result = sim.run_simulation()  
                
            st.json(result)  # 显示最终结果

if __name__ == "__main__":
    main()