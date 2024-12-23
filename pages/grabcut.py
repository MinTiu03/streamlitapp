from PIL import Image
import streamlit as st
from streamlit_drawable_canvas import st_canvas, CanvasResult

from components.grabcut import (
    display_form_draw,
    display_guide,
    display_st_canvas,
    init_session_state,
    process_grabcut,
)
from services.grabcut.ultis import get_object_from_st_canvas

def init_session_state():
    keys = ["final_mask", "result_grabcut"]
    for key in keys:
        if key not in st.session_state:
            st.session_state[key] = None
def display_st_canvas(raw_image: Image.Image, drawing_mode: str, stroke_width: int):
    w, h = raw_image.size
    width = min(w, 475)
    height = width * h // w

    mode = "rect"
    stroke_color = "rgb(0, 0, 0)"

    if drawing_mode == "sure_bg":
        mode = "freedraw"
        stroke_color = "rgb(0, 255, 0)"
    elif drawing_mode == "sure_fg":
        mode = "freedraw"
        stroke_color = "rgb(255, 0, 0)"

    canvas_result = st_canvas(
        background_image=raw_image,
        drawing_mode=mode,
        fill_color="rgba(0, 0, 0, 0)",
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        width=width + 1,
        height=height + 1,
        key="full_app",
    )

    return canvas_result
st.set_page_config(
    page_title="Tách nền bằng thuật toán Grabcut",
    page_icon=Image.open("./logo.png"),
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Tách nền bằng thuật toán GrabCut")

with st.container(border=True):
    st.markdown(
        """
        #### :material/search: Hướng dẫn sử dụng
        1. Chọn ảnh cần tách nền.
        2. Chọn **chế độ vẽ** và **độ dày nét vẽ**.
        3. Vẽ hình chữ nhật lên ảnh để chọn vùng cần tách nền.
        4. Chọn **chế độ vẽ** và vẽ lên ảnh để chỉ định vùng cần giữ lại hoặc loại bỏ.
        5. Ấn nút `Tách nền` để xem kết quả.
        """
    )

with st.container(border=True):
    uploaded_image = st.file_uploader(
        ":material/image: Chọn ảnh", type=["jpg", "jpeg", "png"]
    )

if uploaded_image is not None:
    with st.container(border=True):
        drawing_mode, stroke_width = display_form_draw()

    with st.container(border=True):
        cols = st.columns(2, gap="large")
        raw_image = Image.open(uploaded_image)

        with cols[0]:
            canvas_result = display_st_canvas(raw_image, drawing_mode, stroke_width)
            rects, true_fgs, true_bgs = get_object_from_st_canvas(canvas_result)

        if len(rects) < 1:
            st.session_state["result_grabcut"] = None
            st.session_state["final_mask"] = None
        elif len(rects) > 1:
            st.warning("Chỉ được chọn một vùng cần tách nền")
        else:
            with cols[0]:
                submit_btn = st.button(
                    ":material/settings_timelapse: Tách nền",
                )

            if submit_btn:
                with st.spinner("Đang xử lý..."):
                    result = process_grabcut(
                        raw_image, canvas_result, rects, true_fgs, true_bgs
                    )
                    cols[1].image(result, channels="BGR", caption="Ảnh kết quả")
            elif st.session_state["result_grabcut"] is not None:
                cols[1].image(
                    st.session_state["result_grabcut"],
                    channels="BGR",
                    caption="Ảnh kết quả",
                )
