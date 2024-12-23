import cv2
import numpy as np
from PIL import Image
import streamlit as st
from streamlit_drawable_canvas import st_canvas

st.set_page_config(
    page_title="Ứng dụng xử lý ảnh",
    page_icon=Image.open("./logo.png"),
    layout="wide",
    initial_sidebar_state="expanded",
)


def display_flip_section(image: np.ndarray):
    with st.form(key="flip_form"):
        flip_options = ["Lật ngang", "Lật dọc", "Cả hai"]
        flip_option = st.selectbox("Chọn hướng flip", flip_options)
        submit = st.form_submit_button("Xử lý")

    cols = st.columns(2)
    cols[0].image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), "Ảnh gốc", use_container_width=True)

    if submit:
        flip_image = image.copy()
        if flip_option == "Lật dọc":
            flip_image = cv2.flip(flip_image, 0)
        elif flip_option == "Lật ngang":
            flip_image = cv2.flip(flip_image, 1)
        else:
            flip_image = cv2.flip(flip_image, -1)

        cols[1].image(cv2.cvtColor(flip_image, cv2.COLOR_BGR2RGB), "Ảnh sau khi flip", use_container_width=True)

def display_st_canvas(raw_image: np.ndarray):
    h, w = raw_image.shape[:2]
    width = min(w, 475)
    height = width * h // w
    ratio = width / w

    stroke_color = st.color_picker("Chọn màu vẽ:", "#FFFFFF")
    stroke_width = st.slider("Chọn độ rộng bút vẽ:", 1, 10, 2)

    canvas_result = st_canvas(
        background_image=Image.fromarray(cv2.cvtColor(raw_image, cv2.COLOR_BGR2RGB)),
        drawing_mode="rect",
        fill_color="rgba(0, 0, 0, 0)",
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        width=width + 1,
        height=height + 1,
        key="rect_canvas",
    )

    return canvas_result, ratio

def display_cropping_section(image: np.ndarray):
    cols = st.columns(2)
    with cols[0]:
        canvas_result, ratio = display_st_canvas(image)

    objects = canvas_result.json_data["objects"]

    if objects is None or len(objects) == 0:
        st.warning("Chọn vùng cần cropping")
    elif len(objects) > 1:
        st.warning("Chỉ chọn một vùng cần cropping")
    else:
        obj = objects[0]
        left = int(obj["left"] / ratio)
        top = int(obj["top"] / ratio)
        width = int(obj["width"] / ratio)
        height = int(obj["height"] / ratio)
        cropped_image = image.copy()
        cropped_image = cropped_image[top:top + height, left:left + width]
        cols[1].image(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB), "Ảnh sau khi cắt", use_container_width=True)

def display_colorspace_section(image: np.ndarray):
    with st.form(key="colorspace_form"):
        colorspace = st.selectbox("Chọn không gian màu", ["RGB", "HSV", "GRAY","CrCb"])
        submit = st.form_submit_button("Xử lý")

    cols = st.columns(2)
    cols[0].image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), "Ảnh gốc (RGB)", use_container_width=True)

    if submit:
        colorspace_image = image.copy()
        if colorspace == "RGB":
            colorspace_image = cv2.cvtColor(colorspace_image, cv2.COLOR_BGR2RGB)
        elif colorspace == "HSV":
            colorspace_image = cv2.cvtColor(colorspace_image, cv2.COLOR_BGR2HSV)
        elif colorspace == "GRAY":
            colorspace_image = cv2.cvtColor(colorspace_image, cv2.COLOR_BGR2GRAY)
        elif colorspace == "CrCb":
            colorspace_image = cv2.cvtColor(colorspace_image, cv2.COLOR_BGR2YCrCb)

        cols[1].image(colorspace_image, "Ảnh sau khi biến đổi colorspace", use_container_width=True)

def display_translation_section(image: np.ndarray):
    with st.form(key="translation_form"):
        tx = st.slider("Chọn tịnh tiến theo trục x",-image.shape[0], image.shape[0], 0)
        ty = st.slider("Chọn tịnh tiến theo trục y", -image.shape[1], image.shape[1], 0)
        submit = st.form_submit_button("Xử lý")

    cols = st.columns(2)
    cols[0].image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), "Ảnh gốc", use_container_width=True)

    if submit:
        translation_image = image.copy()
        # ma trận chuyển dịch
        translation_matrix = np.float32([[1, 0, tx], [0, 1, ty]])
        #ma trận tịch tiến
        translation_image = cv2.warpAffine(translation_image, translation_matrix, (image.shape[1], image.shape[0]))

        cols[1].image(cv2.cvtColor(translation_image, cv2.COLOR_BGR2RGB), "Ảnh sau khi tịnh tiến",use_container_width=True)

def display_rotation_section(image: np.ndarray):
    with st.form(key="roration_form"):
        angle = st.slider("Góc quay", -180, 180, 0)
        submit = st.form_submit_button("Xử lý")

    cols = st.columns(2)
    cols[0].image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), "Ảnh gốc", use_container_width=True)

    if submit:
        rotation_image = image.copy()
        h, w = rotation_image.shape[:2]
        center = (w // 2, h // 2)
        rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotation_image = cv2.warpAffine(rotation_image, rotation_matrix, (w, h))

        cols[1].image(cv2.cvtColor(rotation_image, cv2.COLOR_BGR2RGB), "Ảnh sau khi rotation", use_container_width=True)
def display_app():
    st.write(
        """
        - Ứng dụng dụng sử lý ảnh bao gồm: "Colorspace","Cropping","Rotation","Translation","Flip"
        """
    )
    with st.container(border=True):
        technique = st.selectbox("Chọn kỹ thuật cần thực hiện",
                                 ["Colorspace","Cropping","Rotation","Translation","Flip"])
        uploaded_file = st.file_uploader("Chọn một ảnh cần xử lý", type=["jpg", "png"], accept_multiple_files=False)

    if uploaded_file is not None:
        switcher = {
            "Flip": display_flip_section,
            "Rotation": display_rotation_section,
            "Colorspace": display_colorspace_section,
            "Translation": display_translation_section,
            "Cropping": display_cropping_section
        }
        image_pil = Image.open(uploaded_file)
        image = np.array(image_pil)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if technique == "Flip":
            display_flip_section(image)
        elif technique == "Rotation":
            display_rotation_section(image)
        elif technique == "Colorspace":
            display_colorspace_section(image)
        elif technique == "Translation":
            display_translation_section(image)
        elif technique == "Cropping":
            display_cropping_section(image)
        else:
            st.write("Tính năng đang phát triển")

st.title("Ứng dụng xử lý ảnh")
display_app()