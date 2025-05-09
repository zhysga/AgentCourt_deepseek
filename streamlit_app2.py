# c:\workdir\CascadeProjects\windsurf-project\paper\AgentCourt-main\streamlit_app.py
from AgentCourt_main.main import CourtSimulation
import streamlit as st
import json
import logging
from tqdm import tqdm
from typing import Dict, Any

def show_simulation_progress(sim: CourtSimulation):
    # 创建选项卡布局
    tab1, tab2, tab3 = st.tabs(["📋 输入参数", "📜 执行日志", "📊 模拟结果"])
    
    with tab1:
        st.subheader("当前案例参数")
        st.json(sim.current_case)  # 假设sim有current_case属性
        
    with tab2:
        log_container = st.container(height=400)
        
        class StreamlitHandler(logging.Handler):
            def emit(self, record):
                log_container.write(f"```\n{record.levelname}: {record.msg}\n```")
        
        sim.logger.addHandler(StreamlitHandler())
    
    return tab3

def main():
    st.set_page_config(page_title="Agent Court 模拟器", layout="wide")
    
    # 侧边栏参数配置
    with st.sidebar.expander("⚙️ 高级设置", expanded=True):
        config_file = st.file_uploader("上传配置文件", type=["json"])
        case_path = st.text_input("案例路径", value="data/cases")
        log_level = st.selectbox("日志级别", ["DEBUG", "INFO", "WARNING", "ERROR"])
        dp_mode = st.radio("运行模式", ["API模式", "离线模式"], index=0)
    
    # 主界面
    if config_file:
        try:
            config = json.load(config_file)
            sim = CourtSimulation(
                config_path=config,
                case_path=case_path,
                log_level=log_level,
                dp=1 if dp_mode == "API模式" else 0
            )
            
            if st.button("🚀 开始完整模拟"):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # 步骤1：初始化
                with st.status("初始化模拟环境..."):
                    sim.initialize()
                    progress_bar.progress(25)
                
                # 步骤2：案例准备
                with st.status("加载案例文件..."):
                    sim.load_case()
                    progress_bar.progress(50)
                
                # 步骤3：执行模拟
                result_tab = show_simulation_progress(sim)
                with st.status("执行模拟流程..."):
                    for step in tqdm(range(10), desc="模拟进度"):
                        progress_bar.progress(60 + step*3)
                        result = sim.run_simulation()
                
                # 结果显示
                with result_tab:
                    st.subheader("最终判决结果")
                    st.json(result)
                    st.download_button(
                        label="📥 下载报告",
                        data=json.dumps(result, indent=2),
                        file_name="simulation_report.json",
                        mime="application/json"
                    )
                
                progress_bar.progress(100)
                st.success("✅ 模拟完成！")

        except Exception as e:
            st.error(f"❌ 发生错误：{str(e)}")
            st.exception(e)

if __name__ == "__main__":
    main()